#!/usr/bin/python3
import sys
import os
sys.path.append("/home/vkobryn/Projects/mistofm")
import config


def ices_get_next(*args, **kwargs):
    onlyfiles = [f for f in os.listdir(config.STATION_JINGLE_FOLDER)
                 if os.path.isfile(os.path.join(config.STATION_JINGLE_FOLDER, f))]
    return onlyfiles[0]