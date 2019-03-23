from os import listdir
from os.path import isfile, join
import re


class Picture(object):
    def __init__(self, serialnum=None, extension=None, rating=0, info=None, action=None):
        self.serialnum = serialnum
        self.extension = extension
        self.rating = rating
        self.info = info
        self.action = action


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


def print_picturelist(picturelist, actionfilter=""):
    for pic in picturelist:
        if actionfilter != "":
            if pic.action == actionfilter:
                print(pic.serialnum)
                print(pic.extension)
                print(pic.rating)
                print(pic.info)
                print(pic.action)
                print('...................')
        else:
            print(pic.serialnum)
            print(pic.extension)
            print(pic.rating)
            print(pic.info)
            print(pic.action)
            print('...................')


def build_filelist(filelist):
    picturelist = []
    for filename in filelist:
        picturelist.append(Picture(
            extract_sn(filename),
            extract_extension(filename),
            extract_rating(filename),
            extract_add_info(filename)))
    return picturelist


def compare(jpgs, raws):
    raw_del_count = 0
    jpg_del_count = 0
    for jpg in jpgs:
        hit = False
        for raw in raws:
            if jpg.serialnum == raw.serialnum:
                print("HIT!!!")
                jpg.action = 'none'
                raw.action = 'none'
                hit = True
            else:
                if raw.action is None:
                    print("NO HIT")
                    raw.action = 'delete'
                    raw_del_count = raw_del_count + 1
        if not hit:
            jpg.action = 'delete'
            jpg_del_count = jpg_del_count + 1
    return "Raw to be deleted " + str(raw_del_count) + " JPG to be deleted " + str(jpg_del_count)


dirRaw="/home/asztrik/Documents/Work/cassio/cassio test/KUN R"
dirJpg="/home/asztrik/Documents/Work/cassio/cassio test/KUN AJ"
rawFiles = [f for f in listdir(dirRaw) if isfile(join(dirRaw, f))]
jpgFiles = [f for f in listdir(dirJpg) if isfile(join(dirJpg, f))]

rawlist = build_filelist(rawFiles)
jpglist = build_filelist(jpgFiles)

print(compare(jpglist, rawlist))

print("JPG")
print("===========")

print_picturelist(jpglist, "delete")

print("RAW")
print("===========")

print_picturelist(rawlist, "delete")