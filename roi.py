class ROI:

    def __init__(self, roi_list):
        self.roi_list = sorted(list(set(roi_list)))
        self.roi_set = self.fill_roi()
        self.area = len(self.roi_set)

    def __repr__(self):
        return f"""
            roi_list = {self.roi_list},
            roi_set = {sorted(self.roi_set)},
            area = {self.area},
        """

    def fill_roi(self):
        input_roi = sorted(list(set(self.roi_list)))  # unique the roi list
        # grouped_roi_list = list()
        # while len(input_roi) > 0:
        #     print(f'.............. finding group = {len(grouped_roi_list) + 1} ..............')
        #     neighbor_list = list()
        #     started = input_roi.pop(0)
        #     neighbor_list.append(started)
        #     print(f'started = {started}')
        #     for i in range(len(input_roi)):
        #         neighbor = self.find_neighbor_by_clockwise(started, input_roi)
        #         # print(f'neighbor = {neighbor}')
        #         if neighbor:
        #             started = neighbor
        #             neighbor_list.append(neighbor)
        #             input_roi.remove(neighbor)  # remove neighbor
        #     # print(f'neighbor_list = {neighbor_list}')
        #     grouped_roi_list.append(neighbor_list)
        #
        # for grouped_roi in grouped_roi_list:
        #     print(f'grouped_roi = {grouped_roi}')

        filled_group_roi_list = list()
        filled_group_roi_list.extend(self.fill_blank_area(self.roi_list))
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

    # def find_neighbor_by_clockwise(self, point, roi_list):
    #     """ 以 X 為中心，依照順序由 1, 2, 3 往下找他的鄰居在哪，並歸至一類
    #     8  1  2
    #     7  X  3
    #     6  5  4
    #     """
    #     for i in range(1, 9):
    #         if i == 1:
    #             neighbor = (point[0], point[1] + 1)
    #         elif i == 2:
    #             neighbor = (point[0] + 1, point[1] + 1)
    #         elif i == 3:
    #             neighbor = (point[0] + 1, point[1])
    #         elif i == 4:
    #             neighbor = (point[0] + 1, point[1] - 1)
    #         elif i == 5:
    #             neighbor = (point[0], point[1] - 1)
    #         elif i == 6:
    #             neighbor = (point[0] - 1, point[1] - 1)
    #         elif i == 7:
    #             neighbor = (point[0] - 1, point[1])
    #         elif i == 8:
    #             neighbor = (point[0] - 1, point[1] + 1)
    #
    #         if neighbor in roi_list:
    #             return neighbor
    #     return None


def inspection_information(input_area_list: set) -> dict:
    """
    set 的操作：https://wenyuangg.github.io/posts/python3/python-set.html
    回傳 input_area_list 裡面所有的 (交集面積/聯集面積)
    """
    union = set()
    intersection = set()
    for area in input_area_list:
        union = union | area
    intersection = union
    for area in input_area_list:
        intersection = intersection & area
    # print(f"""
    #     intersection = {len(intersection)}
    #     union = {len(union)}
    # """)
    # print(f"""
    #     intersection/union = {len(intersection)/len(union)},
    # """)
    return {
        'union_roi': union,
        'intersection_roi': intersection,
        'union_area': len(union),
        'intersection_area': len(intersection),
        'common_rate': len(intersection) / len(union)
    }


a = [(312, 355),
     (311, 356),
     (310, 357),
     (309, 357),
     (308, 358),
     (308, 359),
     (308, 360),
     (307, 360),
     (306, 361),
     (306, 362),
     (305, 363),
     (304, 364),
     (303, 365),
     (303, 366),
     (302, 367),
     (302, 368),
     (302, 369),
     (301, 370),
     (301, 371),
     (300, 371),
     (299, 372),
     (299, 373),
     (299, 374),
     (299, 375),
     (299, 376),
     (300, 377),
     (301, 378),
     (302, 379),
     (303, 379),
     (304, 379),
     (305, 379),
     (306, 379),
     (307, 378),
     (308, 377),
     (308, 376),
     (309, 375),
     (310, 375),
     (311, 375),
     (312, 375),
     (313, 375),
     (314, 375),
     (315, 375),
     (316, 375),
     (317, 375),
     (318, 375),
     (319, 375),
     (320, 374),
     (321, 373),
     (322, 372),
     (322, 371),
     (322, 370),
     (323, 367),
     (324, 368),
     (325, 367),
     (326, 366),
     (327, 365),
     (328, 364),
     (328, 363),
     (327, 362),
     (327, 361),
     (326, 360),
     (325, 359),
     (324, 359),
     (323, 358),
     (322, 358),
     (321, 357),
     (320, 358),
     (319, 358),
     (318, 358),
     (318, 357),
     (317, 356),
     (316, 355),
     (315, 355),
     (314, 355),
     (313, 355),
     (312, 355),
     ]

zzz = ROI(a)
print(zzz)

area_list = list()
area_list.append(zzz.roi_set)
area_list.append(zzz.roi_set)
area_list.append(zzz.roi_set)
c = [(312, 355),
     (311, 356),
     (310, 357),
     (309, 357),
     (308, 358),
     (308, 359),
     (308, 360),
     (307, 360),
     (306, 361),
     (306, 362),
     (305, 363),
     (304, 364),
     (303, 365),
     (303, 366),
     (302, 367),
     (302, 368),
     (302, 369),
     (301, 370),
     (301, 371),
     (300, 371),
     (299, 372),
     (299, 373),
     (299, 374),
     (299, 375),
     (299, 376),
     (300, 377),
     (301, 378),
     (302, 379),
     (303, 379),
     (304, 379),
     (305, 379),
     (306, 379),
     (307, 378),
     (308, 377),
     (308, 376),
     (309, 375),
     (310, 375),
     (311, 375),
     (312, 375),
     (313, 375),
     (314, 375),
     (315, 375),
     (316, 375),
     (317, 375),
     (318, 375),
     (319, 375),
     (320, 374),
     (321, 373),
     (322, 372),
     (322, 371),
     (322, 370),
     (323, 367),
     (324, 368),
     (325, 367),
     (326, 366),
     (327, 365),
     (325, 359),
     (324, 359),
     (323, 358),
     (322, 358),
     (321, 357),
     (320, 358),
     (319, 358),
     (318, 358),
     (318, 357),
     (317, 356),
     (316, 355),
     (315, 355),
     (314, 355),
     (313, 355),
     (312, 355),
     ]
xxx = ROI(c)
area_list.append(xxx.roi_set)


inspection = inspection_information(area_list)
print(inspection)
