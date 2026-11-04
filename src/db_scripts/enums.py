from enum import Enum
"""
    This is file contatining enums for the Acc0unt1ng. It will be updated to add more enums
    and classes to remove string udentifiers from code and replace with enums.
"""

class ReadType(Enum):
    """
    Enum for calssifying read queries for ReadNew().

    Value specifics: 
        First 100 values reserved for basic queries returning lists.
        101 - 200 values reserved for history related queries.
        201 - 300 values reserved for calculation queries.
        To be written later...
    """
    INITPB = 1
    DINITPB = 2
    CAT = 3
    CATINC = 4
    CATEXP = 5
    
    ALLMAIN = 101
    POSMAIN = 102
    NEGMAIN = 103
    ALLDEP = 104
    OPENDEP = 105
    CLOSEDEP = 106
    STDTRAN = 107
    ADVTRAN = 108
    PLANNING = 109
    CURRRATE = 110