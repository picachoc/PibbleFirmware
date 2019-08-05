import os

def getConfig(path):
    confs = {}
    with open(path, "r") as file:
        datas = file.read()
        pair = datas.split("\n")
        for element in pair:
            if element != "":
                element = element.replace(" ", "")
                key, val = element.split("=")
                if val.isdigit():
                    val = int(val)
                confs.update({key : val})
    return confs
