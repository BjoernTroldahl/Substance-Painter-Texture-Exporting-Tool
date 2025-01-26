# Painter API import 
import substance_painter
import substance_painter_plugins

# 3rd party UI library import
from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QComboBox, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem
from PySide6 import QtCore

#Custom exporter modules
import module_export
import module_validation_name

#Default Utils imports
import importlib

is_user_dev = True
if is_user_dev:
    importlib.reload(module_export)
    importlib.reload(module_validation_name)

#Global variable
custom_expo = None

class CustomExporter:
    #Initializing the custom exporter
    def __init__(self):
        self.initialization()
    
    def initialization(self):
        self.init_widget_window()
        self.connect_widget_events()
        self.connect_substance_painter_events()
        self.show_ui_widget()

        #Code for running the debugger - currently doesn't work because of weird Python non-compatbility reasons, might fix later
        is_debugging = False
        if is_debugging:
            import debugpy
            port = 3000
            debugpy.listen(("localhost", port))
            substance_painter.logging.log(substance_painter.logging.WARNING, "Custom Exporter", f"Waiting for debugger to attach in VS Code in port {port}")

    def init_widget_window(self):
        self.asset_types = ["Weapons", "Characters", "Props"] #list of asset types
        self.shader_types = ["Basic", "Armament", "Morph"] #list of shader types
        self.widget = QWidget()
        self.widget.setObjectName("Custom Exporter")
        self.widget.setWindowTitle("Custom Exporter")

        # Add a layout and content to make the widget visible
        self.main_layout = QGridLayout(self.widget)

        #Label
        self.label = QLabel("Asset Type:")
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

        #Personal checkbox
        self.personal_checkbox = QCheckBox("Personal Export")
        self.main_layout.addWidget(self.personal_checkbox)

        #Asset Type Combobox/Dropdown menu
        self.asset_combobox = QComboBox()
        self.asset_combobox.addItems(self.asset_types)
        self.main_layout.addWidget(self.asset_combobox)

        #Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.main_layout.addWidget(self.refresh_button)

        #Table widget
        self.table_widget = QTableWidget()
        self.table_widget.setMinimumSize(730,250)
        self.init_rows_and_cols_table()
        #self.fill_table()
        self.main_layout.addWidget(self.table_widget)

        #Export button
        #module_export.exporting()
        self.export_button = QPushButton("Export")
        self.main_layout.addWidget(self.export_button)

        if substance_painter.project.is_open():
            self.fill_texture_table()
            self.on_refresh_requested()

    def connect_widget_events(self):
        #Buttons
        self.refresh_button.clicked.connect(self.on_refresh_requested)
        self.export_button.clicked.connect(self.on_export_requested)
        #Personal Export checkbox
        self.personal_checkbox.stateChanged.connect(self.on_refresh_requested)
        #Asset type combo box
        self.asset_combobox.currentIndexChanged.connect(self.on_refresh_requested)

    def connect_substance_painter_events(self):
        #Use a dicionary for looking up the substance painter events
        substance_painter_connections = {
            substance_painter.event.ProjectOpened : self.on_project_opened,
            substance_painter.event.ProjectCreated : self.on_project_created,
        }

        #Use a for loop to iterate through each event and corresponding callback that we need from the dictionary
        for event, callback in substance_painter_connections.items():
            substance_painter.event.DISPATCHER.connect(event, callback)
    
        
    def show_ui_widget(self):
        plugin = substance_painter_plugins.plugins.get("Custom Exporter", None) #If the custom exporter already exists upon launch, we want to delete it and then initialize again to avoid duplication
        if plugin is not None:
            #Refresh the widget
            self.delete_widget()
            self.init_widget_window()
           
        # Add the widget to the Painter UI
        substance_painter.ui.add_dock_widget(self.widget)
        self.widget.show()
    
    #Deleting/hiding the custom exporter if it's unchecked from the menu
    def delete_widget(self):
        if self.widget is not None:
            # Remove the widget from the Painter UI if it currently exists
            substance_painter.ui.delete_ui_element(self.widget)

    def init_rows_and_cols_table(self):
        num_columns = 5
        num_rows = 1
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_columns) #Make scalable, so use a varaible for number of textures instead

        labelHeaders=["Export", "Texture Set Name", "Shader Type", "Resolution", "Export Path"]
        self.table_widget.setHorizontalHeaderLabels(labelHeaders)

        self.table_widget.verticalHeader().setVisible(False) #Hides the visible numbers of vertical headers

        self.table_widget.setColumnWidth(0,40)
        self.table_widget.setColumnWidth(3,70)
        self.table_widget.setColumnWidth(4,370)
    
    def fill_texture_table(self):
        self.all_texture_sets = substance_painter.textureset.all_texture_sets() #We assign this value to SELF so it's not only local and other parts of the class can also use it
        self.table_widget.setRowCount(len(self.all_texture_sets)) #Automatically sets the number of rows to be equal to the number of texture sets used in the project

        #Texture names and resolutions are added with for loop, for scalability  
        for i, texture_set in enumerate(self.all_texture_sets):
            #Personal Export checkbox is added to the "Export" column
            check_box = QCheckBox()
            check_box.setChecked(True)
            check_box.stateChanged.connect(self.gray_out_unchecked_rows)
            self.table_widget.setCellWidget(i,0,check_box) #assigns checkboxes to each row in the first column, with a default state of CHECKED

            #Names of textures column
            self.table_widget.setItem(i,1,QTableWidgetItem(texture_set.name()))

            #Shader type combobox is added to the "Shader Type" column
            combo_box = QComboBox()
            combo_box.addItems(self.shader_types)
            combo_box.currentIndexChanged.connect(self.on_refresh_requested)
            self.table_widget.setCellWidget(i,2,combo_box)

            #Texture resolutions column
            resolution = texture_set.get_resolution()
            width = resolution.width
            height = resolution.height
            self.table_widget.setItem(i,3,QTableWidgetItem(f"{width} x {height}"))

    #The code that unchecks all adjacent rows to the checkbox, if it becomes unchecked. 
    def gray_out_unchecked_rows(self):
        for i in range(self.table_widget.rowCount()): #First, we are iterating over each row of the texture set table
            check_box_item = self.table_widget.cellWidget(i, 0) #Then we are accessing the checkbox of the given row
            if check_box_item.isChecked(): #we check if the given checkbox is checked
                for j in range(1, self.table_widget.columnCount()): #If it IS checked, then we proceed from here. We iterate through everything again, but now starting from the 2nd row since we don't want to gray out the checkbox itself
                    item = self.table_widget.item(i, j) #First we try to access it as a text item 
                    if item is not None: #If it is not none, we proceed
                        item.setFlags(item.flags() | QtCore.Qt.ItemIsEnabled) #We then set a flag to mark that this text is enabled
                    else: #If it is NOT a text, we proceed from here
                        cell_widget = self.table_widget.cellWidget(i, j) #We then access it as a widget, since that's the only other possibility
                        if cell_widget is not None: #If it is not none, we proceed
                            cell_widget.setEnabled(True) #We then set a flag to mark that this widget is enabled
            else: #If the checkbox is NOT checked, then we proceed from here
                for j in range(1, self.table_widget.columnCount()): #Exactly the same as the above, but instead of enabling we instead DISABLE to gray everything out
                    item = self.table_widget.item(i, j)
                    if item is not None:
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    else:
                        cell_widget = self.table_widget.cellWidget(i, j)
                        if cell_widget is not None:
                            cell_widget.setDisabled(True)
    
    #Function that's triggered when clicking the "Refresh" button
    def on_refresh_requested(self):
        #substance_painter.logging.log(substance_painter.logging.INFO, "Custom Exporter", "The refresh button was clicked")
        export_path_root = self.build_root_export_path()
        if self.all_texture_sets is not None:
            for i, texture_set in enumerate(self.all_texture_sets):

                #Names of textures column
                self.table_widget.setItem(i,1,QTableWidgetItem(texture_set.name()))

                #Texture resolutions column
                resolution = texture_set.get_resolution()
                width = resolution.width
                height = resolution.height
                self.table_widget.setItem(i,3,QTableWidgetItem(f"{width} x {height}"))

                #Export path column - all the variables updates the path whenever you change them from the menu and they call the refresh function
                self.table_widget.setItem(i,4,QTableWidgetItem(f"{export_path_root}/{self.asset_combobox.currentText()}/{texture_set.name()}_{self.table_widget.cellWidget(i,2).currentText()}/"))
            
            self.set_column_read_only(1) #Name of textures column
            self.set_column_read_only(3) #Resolution of textures column
            self.set_column_read_only(4) #Export path column
    
    #Makes sure that the user can't edit the text, and it's set to read-only
    def set_column_read_only(self, column_index):
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row,column_index)
            if item is not None:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

    #Builds the start of the texture export path as a string, based on the current state of the Personal Export checkbox
    def build_root_export_path(self):
        if self.personal_checkbox.isChecked():
            root = "C:/ProjectName/Personal"
        else:
            root = "C:/ProjectName/Assets/Textures"
        return root

    #Function that's triggered when the "Export" button is clicked
    def on_export_requested(self):
        if self.all_texture_sets != None: #Safety check, to make sure that the current project contains textures before we proceed
            asset_type = self.asset_combobox.currentText()
            for i in range(len(self.all_texture_sets)):
                should_export = self.table_widget.cellWidget(i,0).isChecked() #Making that the checkbox is checked as well, before we can export
                if not should_export: #If it's not checked, then we exit this whole function
                    continue

                textset_name = self.table_widget.item(i,1).text()
                name_is_valid = module_validation_name.validate_name(asset_type, textset_name)

                if not name_is_valid: #If the name is not valid, we skip the export
                    substance_painter.logging.log(substance_painter.logging.ERROR, "Custom Exporter", f"Name is not valid for texture set # {i+1}. Skipping this texture set.")
                    continue
                
                #If it IS checked, we retrieve the text data from each of the rows to then use in our module_export function
                shader_type = self.table_widget.cellWidget(i,2).currentText()
                export_path = self.table_widget.item(i,4).text()

                module_export.exporting(textset_name, shader_type, export_path)
    
    #Function that's triggered when an exisisting project is opened in Substance Painter
    def on_project_opened(self, e):
        substance_painter.logging.log(substance_painter.logging.INFO, "Custom Exporter", f"Project {substance_painter.project.name()} was opened")
        self.fill_texture_table()
        self.on_refresh_requested()

    #Function that's triggered when a new project is created in Substance Painter
    def on_project_created(self, e):
        substance_painter.logging.log(substance_painter.logging.INFO, "Custom Exporter", "New project was created")
        self.fill_texture_table()
        self.on_refresh_requested()

def start_plugin(): #Needs to have this exact name, because of Substance Painter built-in functions
    global custom_expo
    custom_expo = CustomExporter()


def close_plugin(): #Needs to have this exact name, because of Substance Painter built-in functions
    global custom_expo
    if custom_expo is not None: #Delete the custom exporter if it curently exists
        custom_expo.delete_widget()

if __name__ == "__main__": #Safety measure, to make sure that the script can only be initialized by Substance Painter directly and no external interference occurs
    start_plugin()