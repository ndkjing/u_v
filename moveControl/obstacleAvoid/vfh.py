"""
实现vfh算法
"""


def vfh_func(index, obstacle_list):
    """
    返回是否有可以通过区域 正常返回相对船头角度，返回-1表示没有可以通过区域
    :param index:
    :param obstacle_list:
    :return:
    """
    # angle_point = lng_lat_calculate.angleFromCoordinate(self.lng_lat[0],
    #                                                     self.lng_lat[1],
    #                                                     path_planning_point_gps[0],
    #                                                     path_planning_point_gps[1])
    # if angle_point > 180:
    #     angle_point_temp = angle_point - 360
    # else:
    #     angle_point_temp = angle_point
    # point_angle_index = angle_point_temp // self.pi_main_obj.view_cell + 9
    point_angle_index = 9
    index_i = 0
    value_list = []
    cell_size = len(obstacle_list)
    ceil_max = 3
    view_cell = 5
    field_of_view = 90
    while index_i < cell_size:
        kr = index_i
        index_j = index_i
        while index_j < cell_size and obstacle_list[index_j] == 0:
            kl = index_j
            if kl - kr >= ceil_max-1:  # 判断是否是宽波谷
                v = round((kl + kr) / 2)
                value_list.append(v)
                break
            index_j = index_j + 1
        index_i += 1
    # 没有可以通过通道
    if len(value_list) == 0:
        return -1
    else:
        how = []
        for value_i in value_list:
            howtemp = abs(value_i - point_angle_index)
            how.append(howtemp)
        ft = how.index(min(how))
        kb = value_list[int(ft)]
        print('kb', kb,'value_list',value_list)
        angle = int(kb * view_cell - field_of_view / 2)
        # 该角度为相对船头角度不是相对于北方角度
        if angle < 0:
            angle += 360
        return angle


if __name__ == '__main__':
    import random

    obstacle_list = [0 if random.random() > 0.2 else 1 for i in range(18)]
    print(obstacle_list)
    print(vfh_func(9, obstacle_list))
