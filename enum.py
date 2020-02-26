from enum import Enum


class Modality(Enum):
    CT = 'CT'


class Manufacturer(Enum):
    GE_MEDICAL_SYSTEMS = 'GE MEDICAL SYSTEMS'


class NoduleType(Enum):
    NODULE_GREATER_THAN_3MM = 'NODULE_GREATER_THAN_3MM' 
    NODULE_LESS_THAN_3MM = 'NODULE_LESS_THAN_3MM' 
    NON_NODULE_GREATER_THAN_3MM = 'NON_NODULE_GREATER_THAN_3MM' 