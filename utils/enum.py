from enum import Enum


class Modality(Enum):
    CT = 'CT'


class Manufacturer(Enum):
    GE_MEDICAL_SYSTEMS = 'GE MEDICAL SYSTEMS'


class NoduleType(Enum):
    NODULE_GREATER_THAN_3MM = 2
    NODULE_LESS_THAN_3MM = 1 
    NON_NODULE_GREATER_THAN_3MM = 0