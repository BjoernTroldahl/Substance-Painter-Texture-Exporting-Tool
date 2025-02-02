# Substance-Painter-Texture-Exporting-Tool
Scripts for a custom texture exporting tool, meant for use in a larger scale game production. It only allows export of texture sets from Substance Painter that validate specified naming conventions and texture budgets for selected asset types.

If naming conventions or texture resolutions do not pass the validation checks for a given texture set, exporting will be disabled for that texture set, until it meets the validation requirements.

The tool can automatically change the texture resolution to meet the texture budget, and allows lower resolution as long as the texture don't exceed the maximum allowed budget per asset type texture.

Will only export to a specified folder, based on the selected asset name, and has a selectable shader type that controls the export presets.

Hot-keys and documentation are included. 


