import sys

def search(set, item):
    for i in range ( 0, len( set ) ):
        if( set[i] == item ):
            return i
    return sys.maxint
