from os import listdir
from os.path import isfile, join
import re
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel

"""Region: filename comparison"""


class Picture(object):
    def __init__(self, serialnum=None, extension=None, rating=0, info=None, originalname=None, action='delete'):
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
                jpg.action = 'ok'
                raw.action = 'ok'
                hit = True
        if not hit:
            jpg.action = 'delete'


def load_and_run(dirRaw, dirJpg):
    rawFiles = [f for f in listdir(dirRaw) if isfile(join(dirRaw, f))]
    jpgFiles = [f for f in listdir(dirJpg) if isfile(join(dirJpg, f))]

    rawlist = build_filelist(rawFiles)
    jpglist = build_filelist(jpgFiles)

    compare(jpglist, rawlist)

    jpgstats = get_stats(jpglist)
    jpgdellist = get_picturelist(jpglist, "delete")
    rawstats = get_stats(rawlist)
    rawdellist = get_picturelist(rawlist, "delete")

    print("JPG")
    print(jpgstats)
    print(jpgdellist)

    print("RAW")
    print(rawstats)
    print(rawdellist)

    returnstring = "Az összehasonlítás befejeződött.\nJPG:\n"\
                   + str(jpgstats)\
                   + "\nTörlendő:\n"\
                   + str(jpgdellist)\
                   + "\nRAW:\n"\
                   + str(rawstats) \
                   + "\nTörlendő:\n" \
                   + str(rawdellist)

    """TODO: display file list line by line, offer deleting only RAW only JPG, all..."""

    return returnstring


"""Region: GUI"""


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.rawpath = QLineEdit("C:\cassio test\KUN R")
        self.jpgpath = QLineEdit("C:\cassio test\KUN AJ")
        self.button = QPushButton("Összehasonlítás indítása")
        self.results = QLabel("Az indításhoz válassz mappákat!")
        layout = QVBoxLayout()
        layout.addWidget(self.rawpath)
        layout.addWidget(self.jpgpath)
        layout.addWidget(self.button)
        layout.addWidget(self.results)
        self.setLayout(layout)
        self.button.clicked.connect(self.greetings)
        self.setFixedWidth(500)
        self.setWindowTitle("Cassiodorus 4")

    def greetings(self):
        self.results.setText(load_and_run(self.rawpath.text(), self.jpgpath.text()))


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())






