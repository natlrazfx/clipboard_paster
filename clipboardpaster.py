# Cool Clipboard Paste Feature v02
# Natalia Raz

import nuke
import os, glob, re
from collections import defaultdict
from datetime import datetime

# Use PySide6 on Nuke 16+, otherwise PySide2
if nuke.NUKE_VERSION_MAJOR >= 16:
    from PySide6.QtGui import QGuiApplication, QPixmap
else:
    from PySide2.QtGui import QGuiApplication, QPixmap

def paste_image_from_clipboard():
    clipboard = QGuiApplication.clipboard()
    mime = clipboard.mimeData()
    if mime.hasUrls() and mime.urls()[0].isLocalFile():
        for path in [u.toLocalFile() for u in mime.urls()]:
            if os.path.isfile(path):
                create_read_node(path)
            elif os.path.isdir(path):
                process_folder(path)
    elif mime.hasImage():
        pix = QPixmap(mime.imageData())
        save_and_read(pix)

def process_folder(path):
    files = sorted(glob.glob(os.path.join(path, "*")))
    groups = defaultdict(list)
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        groups[ext].append(f)
    for ext, flist in groups.items():
        if ext in ['.mp4','.mov','.avi']:
            for f in flist: create_read_node(f)
        else:
            handle_sequences_and_standalones(flist)

def handle_sequences_and_standalones(files):
    seq, stand = [], []
    for f in files:
        (seq if is_part_of_sequence(f, files) else stand).append(f)
    load_sequence(seq)
    for f in stand: create_read_node(f)

def load_sequence(sequence_files):
    sequence_files.sort(key=extract_frame_number)
    while sequence_files:
        cs = [sequence_files.pop(0)]
        pad = len(extract_frame_number(cs[0]))
        rem = []
        for f in sequence_files:
            if len(extract_frame_number(f)) == pad:
                cs.append(f)
            else:
                rem.append(f)
        sequence_files = rem
        start = int(extract_frame_number(cs[0]))
        end = int(extract_frame_number(cs[-1]))
        base = re.sub(r"\d+$", "", os.path.splitext(os.path.basename(cs[0]))[0])
        if not base.endswith('_'):
            base += '_'
        seqpath = os.path.join(os.path.dirname(cs[0]), base + "%0{}d".format(pad) + os.path.splitext(cs[0])[1])
        create_read_node(seqpath, start, end)

def save_and_read(pix):
    script = nuke.root().name()
    folder = os.path.join(os.path.dirname(script), "temp") if script != "Root" else os.path.expanduser("~")
    os.makedirs(folder, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fp = os.path.join(folder, f"clipboard_image_{now}.png")
    pix.save(fp, "PNG")
    create_read_node(fp, 1, 1)

def group_files_by_type(flist): pass  # replaced by process_folder

def extract_frame_number(fn):
    m = re.search(r"(\d+)(?=\.\w+$)", fn)
    return m.group(1) if m else "0"

def is_part_of_sequence(fn, files):
    base = re.sub(r"\d+$", "", os.path.splitext(os.path.basename(fn))[0])
    return any(re.sub(r"\d+$","",os.path.splitext(os.path.basename(f))[0]) == base for f in files if f != fn)

def create_read_node(fp, start=None, end=None):
    n = nuke.createNode("Read")
    n["file"].fromUserText(fp)
    if start and end:
        n["first"].setValue(start)
        n["last"].setValue(end)
        n["origfirst"].setValue(start)
        n["origlast"].setValue(start)

nuke.menu('Nuke').addCommand('Edit/Paste Image from Clipboard', 'paste_image_from_clipboard()', 'Ctrl+Alt+V')



















