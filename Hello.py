from os import listdir
from os.path import isfile, join
import re


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


dirRaw="/home/asztrik/Documents/Work/cassio/cassio test/KUN R"
dirJpg="/home/asztrik/Documents/Work/cassio/cassio test/KUN AJ"
rawFiles = [f for f in listdir(dirRaw) if isfile(join(dirRaw, f))]
jpgFiles = [f for f in listdir(dirJpg) if isfile(join(dirJpg, f))]

rawlist = build_filelist(rawFiles)
jpglist = build_filelist(jpgFiles)

compare(jpglist, rawlist)

print("JPG")
print(get_stats(jpglist))

"""print_picturelist(jpglist, "delete")"""

print("RAW")
print(get_stats(rawlist))

"""print_picturelist(rawlist, "delete")"""
