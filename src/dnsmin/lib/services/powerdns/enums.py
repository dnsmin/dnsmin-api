from enum import Enum


class AZoneRRSetChangeTypeEnum(str, Enum):
    """Defines the different types of authoritative zone RRSet change types there can be."""
    DELETE = "DELETE"
    EXTEND = "EXTEND"
    PRUNE = "PRUNE"
    REPLACE = "REPLACE"


class RZoneRRSetChangeTypeEnum(str, Enum):
    """Defines the different types of recursive zone RRSet change types there can be."""
    DELETE = "DELETE"
    REPLACE = "REPLACE"
