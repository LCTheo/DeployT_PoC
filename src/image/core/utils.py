
def lisToDict(inlist):
    outdict = {}
    for line in inlist:
        key, val = line.split(":")
        outdict[key] = val
    return outdict
