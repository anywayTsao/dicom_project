from utils.file_util import deep_scan
from models.dicom import Dicom
from utils.enum import Modality, Manufacturer, NoduleType
from lxml import objectify, etree

import os, re

class Edge:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'<Edge(x = {self.x}, y = {self.y})>'

class Nodule:

    def __init__(self, ns, roi):
        self.z_position = roi.find(f'{ns}imageZposition').text
        self.image_uid = roi.find(f'{ns}imageSOP_UID').text
        inclusion_element = roi.find(f'{ns}inclusion')
        if inclusion_element:
            self.inclusion = roi.find(f'{ns}inclusion').text
        else:
            self.inclusion = None
        edge_map_element_list = roi.findall(f'{ns}edgeMap')
        locus_element_list = roi.findall(f'{ns}locus')
        
        self.edge_map_list = []
        for edge_map_element in edge_map_element_list:
            edge = Edge(edge_map_element.find(f'{ns}xCoord').text, edge_map_element.find(f'{ns}yCoord').text)
            self.edge_map_list.append(edge)
        for locus_element in locus_element_list:
            edge = Edge(locus_element.find(f'{ns}xCoord').text, locus_element.find(f'{ns}yCoord').text)
            self.edge_map_list.append(edge)
        
        if len(edge_map_element_list) > 0:
            if len(self.edge_map_list) > 1:
                self.type = NoduleType.NODULE_GREATER_THAN_3MM
            elif len(self.edge_map_list) == 1:
                self.type = NoduleType.NODULE_LESS_THAN_3MM
            else:
                raise Exception('Cannot tell the nodule type')
        elif len(locus_element_list) > 0:
            if len(self.edge_map_list) == 1:
                self.type = NoduleType.NON_NODULE_GREATER_THAN_3MM
            else:
                raise Exception('Cannot tell the nodule type')
        else:
            raise Exception('Cannot tell the nodule type')

        # print(self)
        
    def __repr__(self):
        return f'<Nodule(image_uid = {self.image_uid}, z_position = {self.z_position}, type = {self.type.value}, len(edge_map_list) = {len(self.edge_map_list)})>'
    