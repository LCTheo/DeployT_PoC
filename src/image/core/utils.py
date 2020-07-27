from typing import List, Dict


def lisToDict(inlist: List[str]) -> Dict[str, str]:
    """transform a list of string with a pattern like 'key:value' to a dictionary"""
    outDict = {}
    for line in inlist:
        key, val = line.split(":")
        outDict[key] = val
    return outDict
