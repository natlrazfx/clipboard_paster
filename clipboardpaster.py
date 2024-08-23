# Natalia Raz
# Clipboard paster Nuke

import nuke
import os
import glob
import re
from collections import defaultdict
from PySide2.QtGui import QGuiApplication, QPixmap
from datetime import datetime

def paste_image_from_clipboard():
    clipboard = QGuiApplication.clipboard()
    mime_data = clipboard.mimeData()

    # Check if file data exists in clipboard
    if mime_data.hasUrls() and mime_data.urls()[0].isLocalFile():
        paths = [url.toLocalFile() for url in mime_data.urls()]
        for path in paths:
            if os.path.exists(path):
                if os.path.isfile(path):
                    create_read_node(path)
                elif os.path.isdir(path):
                    all_files = sorted(glob.glob(os.path.join(path, "*")))
                    file_groups = group_files_by_type(all_files)
                    for file_type, files in file_groups.items():
                        # Handle video files as single files
                        if file_type in ['.mp4', '.mov', '.avi']:
                            for video_file in files:
                                create_read_node(video_file)
                        else:
                            standalone_images = []
                            sequence_files = []

                            for f in files:
                                if is_part_of_sequence(f, files):
                                    sequence_files.append(f)
                                else:
                                    standalone_images.append(f)

                            # Handle sequences
                            sequence_files.sort(key=lambda x: extract_frame_number(x))
                            while sequence_files:
                                current_sequence = [sequence_files.pop(0)]
                                current_padding_length = len(extract_frame_number(current_sequence[0]))
                                remaining_files = []
                                for f in sequence_files:
                                    if len(extract_frame_number(f)) == current_padding_length:
                                        current_sequence.append(f)
                                    else:
                                        remaining_files.append(f)
                                sequence_files = remaining_files
                                start_frame = int(extract_frame_number(current_sequence[0]))
                                end_frame = int(extract_frame_number(current_sequence[-1]))
                                # Correctly construct the sequence path using the base name of the first file in the sequence
                                base_name = re.sub(r"\d+$", "", os.path.basename(os.path.splitext(current_sequence[0])[0]))
                                if not base_name.endswith('_'):
                                    base_name += '_'
                                sequence_path = os.path.join(os.path.dirname(current_sequence[0]), base_name + "%0{}d".format(current_padding_length) + os.path.splitext(current_sequence[0])[1])
                                create_read_node(sequence_path, start_frame, end_frame)

                            # Handle standalone images
                            for img in standalone_images:
                                create_read_node(img)

    elif mime_data.hasImage():
        pixmap = QPixmap(mime_data.imageData())
        script_path = nuke.root().name()
        project_folder = os.path.join(os.path.dirname(script_path), "temp") if script_path != "Root" else os.path.join(os.path.expanduser("~"), "temp")
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = "clipboard_image_" + now + ".png"
        file_path = os.path.join(project_folder, file_name)
        os.makedirs(project_folder, exist_ok=True)
        pixmap.save(file_path, "PNG")
        create_read_node(file_path, 1, 1)

def group_files_by_type(files):
    """Groups files by their extensions."""
    file_groups = defaultdict(list)
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        file_groups[ext].append(file)
    return file_groups

def extract_frame_number(filename):
    """Extracts the frame number from the filename."""
    match = re.search(r"(\d+)(?=\.\w+$)", filename)
    if match:
        return match.group(1)
    else:
        return "0"

def is_part_of_sequence(filename, files):
    """Determines if a file is part of a sequence."""
    base_name = re.sub(r"\d+$", "", os.path.basename(os.path.splitext(filename)[0]))
    for other_file in files:
        if other_file == filename:
            continue
        other_base = re.sub(r"\d+$", "", os.path.basename(os.path.splitext(other_file)[0]))
        if other_base == base_name:
            return True
    return False

def create_read_node(file_path, start_frame=None, end_frame=None):
    read_node = nuke.createNode("Read")
    read_node["file"].fromUserText(file_path)
    if start_frame and end_frame:
        read_node["first"].setValue(start_frame)
        read_node["last"].setValue(end_frame)
        read_node["origfirst"].setValue(start_frame)
        read_node["origlast"].setValue(end_frame)

nuke.menu('Nuke').addCommand('Edit/Paste Image from Clipboard', 'paste_image_from_clipboard()', 'Ctrl+Alt+V')



















