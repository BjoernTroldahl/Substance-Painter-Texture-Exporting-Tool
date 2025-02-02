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

<ins>*For future work I plan to extend upon the project and add at least some of the following features:*</ins>

- Integrating version control system support for the exported textures
- Adding support for exporting textures that are using UV Tile workflow (UDIms)
- Automating renaming of the textures to be within naming conventions
- Extending resolution validation for non-square sizes (width != height)
- Adding support for textures that use material layering

## How to install and use:

1. Download this GitHub repository as a ZIP-file under the Code tab and unzip it into a folder.

2. 
