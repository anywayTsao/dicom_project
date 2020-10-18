from utils.file_util import deep_scan
from utils.enum import Modality, Manufacturer, NoduleType
from lxml import objectify, etree

import os, re


class Edge:
    def __init__(self, x, y):
        self.point = (int(x), int(y))
        self.x = int(x)
        self.y = int(y)


class Nodule:

    def __init__(self, ns, roi):
        self.z_position = roi.find(f'{ns}imageZposition').text
        self.image_uid = roi.find(f'{ns}imageSOP_UID').text
        inclusion_element = roi.find(f'{ns}inclusion')
        if inclusion_element is not None:
            self.inclusion = inclusion_element.text
        else:
            self.inclusion = None
        edge_map_element_list = roi.findall(f'{ns}edgeMap')
        locus_element_list = roi.findall(f'{ns}locus')
        
        self.edge_map_list = []
        for edge_map_element in edge_map_element_list:
            edge = Edge(edge_map_element.find(f'{ns}xCoord').text, edge_map_element.find(f'{ns}yCoord').text)
            self.edge_map_list.append(edge.point)
        for locus_element in locus_element_list:
            edge = Edge(locus_element.find(f'{ns}xCoord').text, locus_element.find(f'{ns}yCoord').text)
            self.edge_map_list.append(edge.point)

        self.roi = sorted(list(set(self.edge_map_list)))
        self.roi_set = self.fill_roi()
        self.area = len(self.roi_set)

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

    def fill_roi(self):

        filled_group_roi_list = list()
        filled_group_roi_list.extend(self.fill_blank_area(self.roi))
        # for grouped_roi in grouped_roi_list:
        #     filled_group_roi_list.extend(self.fill_blank_area(grouped_roi))

        return set(filled_group_roi_list)

    def fill_blank_area(self, grouped_roi):
        loc_dict = dict()

        for s in grouped_roi:
            y_list = loc_dict.get(s[0]) or list()
            y_list.append(s[1])
            loc_dict[s[0]] = sorted(y_list)

        filled_loc_list = list()
        for x, y_list in loc_dict.items():
            y_seq = range(y_list[0], y_list[-1] + 1)
            for y in y_seq:
                filled_loc_list.append((x, y))

        # print(f'filled_loc_list = {filled_loc_list}')
        return filled_loc_list

    def __repr__(self):
        return f'<Nodule(image_uid={self.image_uid}, z_position={self.z_position}, type={self.type.value}, inclusion={self.inclusion}, len(edge_map_list)={len(self.edge_map_list)})>'
