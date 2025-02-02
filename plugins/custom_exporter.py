# Painter API import 
import substance_painter
import substance_painter_plugins

# 3rd party UI library import
from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox
from PySide6 import QtCore, QtGui
from PySide6.QtGui import QAction

#Custom exporter modules
import module_export
import module_validation_name
import module_validation_resolution

#Default Utils imports
import importlib
import os 

is_user_dev = True
if is_user_dev:
    importlib.reload(module_export)
    importlib.reload(module_validation_name)
    importlib.reload(module_validation_resolution)

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

        #Code for running the debugger - currently it only works for older versions of Substance Painter, but I plan to update it in the future
        is_debugging = False
        if is_debugging:
            import debugpy
            port = 3000
            debugpy.listen(("localhost", port))
            substance_painter.logging.log(substance_painter.logging.WARNING, "Custom Exporter", f"Waiting for debugger to attach in VS Code in port {port}")

    def init_widget_window(self):
        self.asset_types = ["Props", "Weapons", "Characters"] #list of asset types
        self.shader_types = ["Basic", "Armament", "Morph"] #list of shader types
        self.textsets_with_overbudget_res = [] #list of texture sets with overbudget resolution, empty by default on startup
        self.widget = QWidget()
        self.widget.setObjectName("Custom Exporter")
        self.widget.setWindowTitle("Custom Exporter")

        self.file_dir = os.path.dirname(__file__)

        self.icons_path = os.path.join(self.file_dir, "icons")

        self.icon_main_window = QtGui.QIcon(os.path.join(self.icons_path, "main_window_icon.png"))
        self.icon_validation_ok = QtGui.QIcon(os.path.join(self.icons_path, "validation_ok.png"))
        self.icon_validation_fail = QtGui.QIcon(os.path.join(self.icons_path, "validation_fail.png"))
        self.pixmap_help = QtGui.QPixmap(os.path.join(self.icons_path, "help.png"))
        self.widget.setWindowIcon(self.icon_main_window)

        # Add a layout and content to make the widget visible
        self.main_layout = QVBoxLayout(self.widget)

        # Help Icon
        help_layout = QHBoxLayout()
        help_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        help_label = QLabel()
        scaled_pixmap = self.pixmap_help.scaled(32, 32) #Scaling the help icon to 32x32 pixels
        help_label.setPixmap(scaled_pixmap)
        help_label.setFixedSize(scaled_pixmap.size())
        help_label.mousePressEvent = self.show_help #When the help icon is clicked, it will trigger the show_help function
        help_label.setToolTip("Click here to open the help documentation \nHotkey: Alt + F1")
        help_layout.addWidget(help_label)
        self.main_layout.addLayout(help_layout)

        # Help Action
        self.help_action = QAction("show Help", self.widget)
        self.help_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT | QtCore.Qt.Key_F1))
        self.widget.addAction(self.help_action)

        #Label
        self.label = QLabel("Asset Type:")
        self.main_layout.addWidget(self.label)

        #Personal checkbox
        self.personal_checkbox = QCheckBox("Personal Export")
        self.personal_checkbox.setToolTip("Specify desired project root export path: Personal or Official")
        self.main_layout.addWidget(self.personal_checkbox)

        #Asset Type Combobox/Dropdown menu
        self.asset_combobox = QComboBox()
        self.asset_combobox.addItems(self.asset_types)
        self.asset_combobox.setToolTip("Select the type of asset - it will affect the export path generation and texture set validations")
        self.main_layout.addWidget(self.asset_combobox)

        #Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setToolTip("Refresh data in the table below \nHotkey: Alt + R")
        self.refresh_button.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT | QtCore.Qt.Key_R))
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
        self.export_button.setToolTip("Trigger export of all checked texture sets \nHotkey: Alt + E")
        self.export_button.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT | QtCore.Qt.Key_E))
        self.main_layout.addWidget(self.export_button)

        if substance_painter.project.is_open():
            self.fill_texture_table()
            settings = QtCore.QSettings()
            settings.setValue("dialog_window_checkbox_state", QtCore.Qt.CheckState.Unchecked)  

    def connect_widget_events(self):
        #Buttons
        self.refresh_button.clicked.connect(self.on_refresh_requested)
        self.export_button.clicked.connect(self.on_export_requested)
        #Personal Export checkbox
        self.personal_checkbox.stateChanged.connect(self.on_refresh_requested)
        #Asset type combo box
        self.asset_combobox.currentIndexChanged.connect(self.on_refresh_requested)
        #Hot key trigger for help
        self.help_action.triggered.connect(self.show_help)

    def connect_substance_painter_events(self):
        #Use a dicionary for looking up the substance painter events
        substance_painter_connections = {
            substance_painter.event.ProjectOpened : self.on_project_opened,
            substance_painter.event.ProjectCreated : self.on_project_created,
            substance_painter.event.ProjectAboutToClose : self.on_project_about_to_close,
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
    
    def show_help(self, event):
        help_doc_path = os.path.join(self.file_dir, "Custom_Exporter_Help.pdf")
        help_url = QtCore.QUrl.fromLocalFile(help_doc_path)
        QtGui.QDesktopServices.openUrl(help_url)
    
    #Deleting/hiding the custom exporter if it's unchecked from the menu
    def delete_widget(self):
        if self.widget is not None:
            # Remove the widget from the Painter UI if it currently exists
            substance_painter.ui.delete_ui_element(self.widget)

    def init_rows_and_cols_table(self):
        labelHeaders=["Export", "Texture Set Name", "Shader Type", "Resolution", "Export Path", "Validation"]
        num_columns = len(labelHeaders)
        num_rows = 0

        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_columns) #Make scalable, so use a varaible for number of textures instead

        self.table_widget.setHorizontalHeaderLabels(labelHeaders)

        self.table_widget.verticalHeader().setVisible(False) #Hides the visible numbers of vertical headers

        self.table_widget.setColumnWidth(0,40)
        self.table_widget.setColumnWidth(3,70)
        self.table_widget.setColumnWidth(4,370)
        self.table_widget.setColumnWidth(5,60)
    
    def validate_texture_sets(self): #Visual representation of the validation with icons
        asset_type = self.asset_combobox.currentText()
        self.textsets_with_overbudget_res = []
        for i, texture_set in enumerate(self.all_texture_sets):
            res_is_valid, res_validation_details = module_validation_resolution.validate_res(asset_type, texture_set.get_resolution())
            validation_item = QTableWidgetItem() #Changes the icon based on the name validation - the icon automatically scales to the size of the cell
            export_checkbox = self.table_widget.cellWidget(i,0)
            if res_is_valid:
                name_is_valid, name_validation_details = module_validation_name.validate_name(asset_type, texture_set.name())
                if name_is_valid:
                    validation_item.setIcon(self.icon_validation_ok)
                    validation_item.setToolTip(f"Texture set validations are OK for texture set {i+1} \
                                                \n{texture_set.name()} \
                                                \nGood job!")
                    export_checkbox.setToolTip(f"Specify if Texture Set {i+1}: {texture_set.name()} \
                                               should be processed during the export or skipped.")
                else:
                    validation_item.setIcon(self.icon_validation_fail)
                    validation_item.setToolTip(f"Texture set Name validation is FAILED for texture set {i+1} \
                                                \n{texture_set.name()} \
                                                \nReason: {name_validation_details} \
                                                \nExport of this texture set is forcibly disabled until validation is OK.")
                    export_checkbox.setToolTip(f"Texture set Name validation is FAILED for texture set {i+1} \
                                                \n{texture_set.name()} \
                                                \nReason: {name_validation_details} \
                                                \nExport of this texture set is forcibly disabled until validation is OK.")
            else:
                validation_item.setIcon(self.icon_validation_fail)
                validation_item.setToolTip(f"Texture set Resolution validation is FAILED for texture set {i+1} \
                                            \n{texture_set.name()} \
                                            \nReason: {res_validation_details} \
                                            \nExport of this texture set is forcibly disabled until validation is OK.")
                export_checkbox.setToolTip(f"Texture set Resolution validation is FAILED for texture set {i+1} \
                                            \n{texture_set.name()} \
                                            \nReason: {res_validation_details} \
                                            \nExport of this texture set is forcibly disabled until validation is OK.")
                self.textsets_with_overbudget_res.append(texture_set)
            
            export_checkbox.setChecked(res_is_valid and name_is_valid) #Python is smart enough to know that if the first one is false, it won't even bother checking the second one
            export_checkbox.setEnabled(res_is_valid and name_is_valid)
            self.table_widget.setItem(i,5,validation_item)

        if len(self.textsets_with_overbudget_res) > 0:
            self.open_dialog_res_confirmation()

    def open_dialog_res_confirmation(self):   
        settings = QtCore.QSettings()
        if settings.value("dialog_window_checkbox_state", QtCore.Qt.CheckState.Unchecked) == QtCore.Qt.CheckState.Unchecked:
            dialog = DialogWindow(self.icon_main_window)
            if dialog.exec_() == QDialog.DialogCode.Accepted:
                self.apply_required_res()
                self.on_refresh_requested()
                
            else:
                substance_painter.logging.log(severity=substance_painter.logging.WARNING, 
                                              channel="Custom Exporter", 
                                              message="Remember to manually fix the resolution in the texture set settings. Validation error will prevent export.")
        else:
            substance_painter.logging.log(severity=substance_painter.logging.INFO, 
                                          channel="Custom Exporter", 
                                          message="Dialog for Resolution Validation autofix was not triggered as per user settings.")
    
    def apply_required_res(self):
        required_width, required_height = module_validation_resolution.get_required_res_from_asset_type(self.asset_combobox.currentText())
        required_res = substance_painter.textureset.Resolution(required_width, required_height)
        for texture_set in self.textsets_with_overbudget_res:
            original_res = texture_set.get_resolution()
            texture_set.set_resolution(required_res)
            substance_painter.logging.log(severity=substance_painter.logging.INFO,
                                          channel="Custom Exporter",
                                          message=f"Applied required resolution for texture set {texture_set.name()} \
                                                    \nWas: {original_res}; Now: {required_res}")

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
            combo_box.setToolTip("Specify the type of export preset to be used during the export process")
            self.table_widget.setCellWidget(i,2,combo_box)

            #Texture resolutions column
            resolution = texture_set.get_resolution()
            width = resolution.width
            height = resolution.height
            self.table_widget.setItem(i,3,QTableWidgetItem(f"{width} x {height}"))
        self.on_refresh_requested()

    #The code that unchecks all adjacent rows to the checkbox, if it becomes unchecked. 
    def gray_out_unchecked_rows(self):
        for i in range(self.table_widget.rowCount()): #First, we are iterating over each row of the texture set table
            check_box_item = self.table_widget.cellWidget(i, 0) #Then we are accessing the checkbox of the given row
            if check_box_item.isChecked(): #we check if the given checkbox is checked
                for j in range(1, self.table_widget.columnCount()-1): #If it IS checked, then we proceed from here. We iterate through everything again, but now starting from the 2nd row since we don't want to gray out the checkbox itself. -1 is to make sure we don't gray out the icon.
                    item = self.table_widget.item(i, j) #We then access the item as a text
                    if item is not None: #If it is not none, we proceed
                        item.setFlags(item.flags() | QtCore.Qt.ItemIsEnabled) #We then set a flag to mark that this text is enabled
                    else: #If it is NOT a text, we proceed from here
                        cell_widget = self.table_widget.cellWidget(i, j) #We then access it as a widget, since that's the only other possibility
                        if cell_widget is not None: #If it is not none, we proceed
                            cell_widget.setEnabled(True) #We then set a flag to mark that this widget is enabled
            else: #If the checkbox is NOT checked, then we proceed from here
                for j in range(1, self.table_widget.columnCount()-1): #Exactly the same as the above, but instead of enabling we instead DISABLE to gray everything out
                    item = self.table_widget.item(i, j)
                    if item is not None:
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    else:
                        cell_widget = self.table_widget.cellWidget(i, j)
                        if cell_widget is not None:
                            cell_widget.setDisabled(True)
    
    #Function that's triggered when clicking the "Refresh" button
    def on_refresh_requested(self):
        if substance_painter.project.is_open():
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

                self.validate_texture_sets()
                self.gray_out_unchecked_rows()

                self.set_column_read_only(1) #Name of textures column
                self.set_column_read_only(3) #Resolution of textures column
                self.set_column_read_only(4) #Export path column
                self.set_column_read_only(5) #Validation column
    
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
        if substance_painter.project.is_open():
            if self.all_texture_sets != None: #Safety check, to make sure that the current project contains textures before we proceed
                for i in range(len(self.all_texture_sets)):
                    should_export = self.table_widget.cellWidget(i,0).isChecked() #Making that the checkbox is checked as well, before we can export
                    if not should_export: #If it's not checked, then we exit this whole function
                        continue

                    textset_name = self.table_widget.item(i,1).text()
                    #If it IS checked, we retrieve the text data from each of the rows to then use in our module_export function
                    shader_type = self.table_widget.cellWidget(i,2).currentText()
                    export_path = self.table_widget.item(i,4).text()
                    module_export.exporting(textset_name, shader_type, export_path)
    
    #Function that's triggered when an exisisting project is opened in Substance Painter
    def on_project_opened(self, e):
        self.fill_texture_table()

    #Function that's triggered when a new project is created in Substance Painter
    def on_project_created(self, e):
        self.fill_texture_table()

    #Function that's triggered when a new project is about to close in Substance Painter
    def on_project_about_to_close(self, e):
        self.init_rows_and_cols_table()

class DialogWindow(QDialog):
    def __init__(self, icon):
        super().__init__()
        self.setWindowTitle("Texture Set Resolution is over budget")
        self.setWindowIcon(icon)
        self.setFixedSize(600, 160)

        layout = QVBoxLayout(self)

        text_label = QLabel("There is a validation error in the Resolution Check step. \nBut no worries, the tool can automatically adjust the resolution of all texture sets that do not meet the requirements. \nDo you want to proceed?")
        layout.addWidget(text_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No) #CHECK IF THIS GIVES AN ERROR
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Yes).setText("Yes, apply the required resolution for all texture sets.")
        buttons.button(QDialogButtonBox.No).setText("No, I'll modify the resolution manually.")
        layout.addWidget(buttons)

        checkbox = QCheckBox("Do not show this message again.")
        checkbox.setChecked(False)
        checkbox.stateChanged.connect(self.save_checkbox_state)
        layout.addWidget(checkbox)

    def save_checkbox_state(self, state):
        settings = QtCore.QSettings()
        settings.setValue("dialog_window_checkbox_state", state)

def start_plugin(): #Needs to have this exact name, because of Substance Painter built-in functions
    global custom_expo
    custom_expo = CustomExporter()

def close_plugin(): #Needs to have this exact name, because of Substance Painter built-in functions
    global custom_expo
    if custom_expo is not None: #Delete the custom exporter if it curently exists
        custom_expo.delete_widget()

if __name__ == "__main__": #Safety measure, to make sure that the script can only be initialized by Substance Painter directly and no external interference occurs
    start_plugin()