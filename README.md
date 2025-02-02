# Substance-Painter-Texture-Exporting-Tool

<img width="1134" alt="CustomExporter" src="https://github.com/user-attachments/assets/2ecccbb3-951d-4ad1-9b31-276cc7adf27d" />

## Description

Scripts for a custom texture exporting tool, meant for use in a larger scale game production. It only allows export of texture sets from Substance Painter that validate specified naming conventions and texture budgets for dropdown-selectable asset types.

If naming conventions or texture resolutions do not pass the validation checks for a given texture set, exporting will be disabled for that texture set, until it meets the validation requirements.

The tool can automatically change the texture resolution to meet the texture budget, and allows lower resolution as long as the texture don't exceed the maximum allowed budget per asset type texture.

It will only export to a specified folder, based on the selected asset name, and a dropdown-selectable shader type controls the export presets.

Hot-keys and documentation are included. 

This project was made possible because of Viacheslav Makhynko and the knowledge-sharing from his Udemy course in Python automation in Substance Painter. 
I built the tool by following his course and updated it to work with the PySide6 module and, as of the writing of this .README file, the latest stable version of Python (3.13.1) and Substance Painter (10.1.2).

<ins>*For future work, I plan to extend upon the project and add at least some of the following features:*</ins>

- Integrating version control system support for the exported textures
- Adding support for exporting textures that are using UV Tile workflow (UDIms)
- Automating renaming of the textures to be within naming conventions
- Extending resolution validation for non-square sizes (width != height)
- Adding support for textures that use material layering

## How to install and use:

1. Download this GitHub repository as a ZIP-file under the Code tab and unzip it into a folder.
2. Navigate to the Python folder of your Substance Painter installation. By default it is: *C:\Users\YOUR_USER_NAME\Documents\Adobe\Adobe Substance 3D Painter\python*
3. Copy and paste the *.vscode, modules, plugins* and *startup* folders here, from your unzipped folder.
4. Open Substance Painter.
5. You should now be able to access the Custom Exporter tool. Make sure that *Python -> custom_exporter* and *Window -> Views -> Custom Exporter* are ENABLED from the top left menu options.
6. The Custom Exporter tool should now appear as a widget window in the middle of your screen, that you can dock anywhere you want inside the Substance Painter editor. It behaves like any other widget windows.
7. You can now open any Substance Painter project and utilize the Custom Exporter for streamlining texture exports. Click on the tool's blue help icon to get started, all information on how to use it is written there.
8. For dev work on the tool, you need to open the Python modules in Visual Studio Code (or another IDE of choice with Python support, but VS Code is what I used).
9. Then add  *"python.analysis.extraPaths": ["C:/Program Files/Adobe/Adobe Substance 3D Painter/resources/python/modules"]* under the default interpreter path in the *settings.json* file.
