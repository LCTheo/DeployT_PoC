
def lisToDict(inlist):
    outdict = {}
    if inlist:
        for line in inlist:
            key, val = line.split(":")
            outdict[key] = val
        return outdict
    else:
        return outdict
