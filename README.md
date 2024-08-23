# clipboard_paster
A Python script for Nuke that allows users to paste images or sequences from the clipboard directly into the project. It automatically detects image sequences and handles multiple file types efficiently.

![clipboardpaster](https://github.com/user-attachments/assets/4971e81f-a3d6-4368-ab78-b42d6fe8d54f)

## Installation and Usage Instructions

This script requires the PySide2 library. To install it, run the following command:
bash
**pip install PySide2**

Download or clone the clipboard_paster.py script
It is recommended to add this script to your .nuke/menu.py file for automatic loading. You can do this by adding the following line in **.nuke/menu.py**:

**nuke.pluginAddPath('path_to_script_directory')**
Replace path_to_script_directory with the actual path where clipboard_paster.py is located.

After setting up, restart Nuke.
The script adds a new menu command to Nuke under Edit > Paste Image from Clipboard.
*You can also set the shortcut. By default Ctrl+Alt+V to quickly paste images or sequences from the clipboard into your Nuke project.*

[![Watch the video](https://img.youtube.com/vi/ObUX7_2kuj8/maxresdefault.jpg)](https://youtu.be/ObUX7_2kuj8)

If this script saved you some time or you just love what it does, consider buying me a cup of coffee (or ~~tea~~ dry white wine)!

I hope this script helps you out! If you have any ideas for improvement or run into any issues, feel free to share your thoughts

Cheers :) 
