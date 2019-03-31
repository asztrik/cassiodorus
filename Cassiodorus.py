from os import listdir
from os.path import isfile, join
import re
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QFileDialog

"""Region: filename comparison"""

class Picture(object):
    def __init__(self, serialnum=None, extension=None, rating=0, info=None, originalname=None, action="törlendő"):
        self.serialnum = serialnum
        self.extension = extension
        self.rating = rating
        self.info = info
        self.action = action
        self.originalname = originalname


def extract_sn(filename):
    m = re.search(r"([A-Z]{3})([0-9]{4})", filename)
    return m.group(1) + m.group(2)


def extract_add_info(filename):
    m = re.search(r"( [A-Za-z0-9 ]*)", filename)
    return m.group(1)[1:]


def extract_extension(filename):
    m = re.search(r"(\.[A-Za-z0-9]+)", filename)
    return m.group(1)[1:]


def extract_rating(filename):
    m = re.search(r"(\++)", filename)
    if m:
        return len(m.group(1))
    else:
        return 0


def get_picturelist(picturelist, actionfilter=""):
    picturereslist = []
    for pic in picturelist:
        if actionfilter != "":
            if pic.action == actionfilter:
                picturereslist.append(pic.originalname)
    return picturereslist


def print_picturelist(picturelist, actionfilter=""):
    for pic in picturelist:
        if actionfilter != "":
            if pic.action == actionfilter:
                print(pic.originalname)
                print(".  .  .  .  .  .  .")
                print(" SN: " + pic.serialnum)
                print(" EXT: " + pic.extension)
                print(" RATING: " + str(pic.rating))
                print(" INFO: " + pic.info)
                print(" ACTION: " + pic.action)
                print('...................')
        else:
            print(pic.originalname)
            print(".  .  .  .  .  .  .")
            print(" SN: " + pic.serialnum)
            print(" EXT: " + pic.extension)
            print(" RATING: " + str(pic.rating))
            print(" INFO: " + pic.info)
            print(" ACTION: " + pic.action)
            print('...................')


def get_stats(picturelist):
    stats = dict()
    for pic in picturelist:
        if pic.action in stats:
           stats[pic.action] = stats[pic.action] + 1
        else:
           stats[pic.action] = 1
    return stats


def build_filelist(filelist):
    picturelist = []
    for filename in filelist:
        picturelist.append(Picture(
            extract_sn(filename),
            extract_extension(filename),
            extract_rating(filename),
            extract_add_info(filename),
            filename))
    return picturelist


def compare(jpgs, raws):
    for jpg in jpgs:
        hit = False
        for raw in raws:
            if jpg.serialnum == raw.serialnum:
                jpg.action = "rendben"
                raw.action = "rendben"
                hit = True
        if not hit:
            jpg.action = "törlendő"


def load_and_run(dirRaw, dirJpg):
    rawFiles = [f for f in listdir(dirRaw) if isfile(join(dirRaw, f))]
    jpgFiles = [f for f in listdir(dirJpg) if isfile(join(dirJpg, f))]

    rawlist = build_filelist(rawFiles)
    jpglist = build_filelist(jpgFiles)

    compare(jpglist, rawlist)

    jpgstats = get_stats(jpglist)
    global jpgstodelete
    jpgstodelete = get_picturelist(jpglist, "törlendő")
    rawstats = get_stats(rawlist)
    global rawstodelete
    rawstodelete = get_picturelist(rawlist, "törlendő")

    print("JPG")
    print(jpgstats)
    print(jpgstodelete)

    print("RAW")
    print(rawstats)
    print(rawstodelete)

    returnstring = "A mappák állapota:\nJPG:\n"\
                   + str(jpgstats)\
                   + "\nRAW:\n"\
                   + str(rawstats)

    """TODO: display file list line by line, offer deleting only RAW only JPG, all..."""

    return returnstring


"""Region: GUI"""


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.rawpath = QPushButton("RAW mappa kijelölése")
        self.jpgpath = QPushButton("JPG mappa kijelölése")
        self.button = QPushButton("Összehasonlítás indítása")
        self.results = QLabel("Az indításhoz válassz mappákat!")
        self.deljpgbutton = QPushButton("Pár nélküli JPG-k törlése")
        self.delrawbutton = QPushButton("Pár nélküli RAW-ok törlése")
        self.delallbutton = QPushButton("Összes pár nélküli törlése")
        layout = QVBoxLayout()
        layout.addWidget(self.rawpath)
        layout.addWidget(self.jpgpath)
        layout.addWidget(self.button)
        layout.addWidget(self.results)
        layout.addWidget(self.deljpgbutton)
        layout.addWidget(self.delrawbutton)
        layout.addWidget(self.delallbutton)
        self.deljpgbutton.hide()
        self.delrawbutton.hide()
        self.delallbutton.hide()
        self.setLayout(layout)
        self.jpgpath.clicked.connect(self.selectjpg)
        self.rawpath.clicked.connect(self.selectraw)
        self.button.clicked.connect(self.docompare)
        self.deljpgbutton.clicked.connect(self.deljpg)
        self.delrawbutton.clicked.connect(self.delraw)
        self.delallbutton.clicked.connect(self.delall)
        self.setFixedWidth(500)
        self.setWindowTitle("Cassiodorus 4")

    def selectjpg(self):
        self.jpgpath.setText(str(QFileDialog.getExistingDirectory(self, "Válassz JPG-mappát")))

    def selectraw(self):
        self.rawpath.setText(str(QFileDialog.getExistingDirectory(self, "Válassz RAW-mappát")))

    def docompare(self):
        self.results.setText(load_and_run(self.rawpath.text(), self.jpgpath.text()))
        self.deljpgbutton.show()
        self.delrawbutton.show()
        self.delallbutton.show()

    def deljpg(self):
        deletednum = 0
        for jpg in jpgstodelete:
            os.remove(self.jpgpath.text() + "\\" + str(jpg))
            deletednum = deletednum + 1
        if deletednum > 0:
            self.results.setText(str(deletednum) + " db JPG törölve.")
        else:
            self.results.setText("Nem volt mit törölni.")

    def delraw(self):
        deletednum = 0
        for raw in rawstodelete:
            os.remove(self.rawpath.text() + "\\" + str(raw))
            deletednum = deletednum + 1
        if deletednum > 0:
            self.results.setText(str(deletednum) + " db RAW törölve.")
        else:
            self.results.setText("Nem volt mit törölni.")

    def delall(self):
        deletednumj = 0
        for jpg in jpgstodelete:
            os.remove(self.jpgpath.text() + "\\" + str(jpg))
            deletednumj = deletednumj + 1
        deletednumr = 0
        for raw in rawstodelete:
            os.remove(self.rawpath.text() + "\\" + str(raw))
            deletednumr = deletednumr + 1
        if deletednumj > 0 and deletednumr > 0:
            self.results.setText(str(deletednumj) + " db JPG törölve.\n"+str(deletednumr) + " db RAW törölve.")
        else:
            self.results.setText("Nem volt mit törölni.")


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())






