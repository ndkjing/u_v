"""

"""

import os
import sys
import math
import heapq
import numpy as np
import cv2
from tsp_solver.greedy import solve_tsp
import copy
from tqdm import tqdm

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
sys.path.append(
    os.path.join(
        root_path,
        'baiduMap'))
sys.path.append(
    os.path.join(
        root_path,
        'dataGetSend'))
sys.path.append(
    os.path.join(
        root_path,
        'utils'))
sys.path.append(
    os.path.join(
        root_path,
        'pathPlanning'))

import config
from webServer import server_config
from externalConnect import baidu_map


class Env:
    """
    Env 2D
    """

    def __init__(self, outpool_points):
        # self.x_range = 51  # size of background
        # self.y_range = 31
        self.motions = [(-server_config.pix_interval, 0), (-server_config.pix_interval, server_config.pix_interval),
                        (0, server_config.pix_interval), (server_config.pix_interval, server_config.pix_interval),
                        (server_config.pix_interval, 0), (server_config.pix_interval, -server_config.pix_interval),
                        (0, -server_config.pix_interval), (-server_config.pix_interval, -server_config.pix_interval)]
        self.outpool_points = outpool_points
        self.obs = self.obs_map()

    def update_obs(self, obs):
        self.obs = obs

    def obs_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """
        obs = set()
        for i in self.outpool_points:
            obs.add((i[0], i[1]))
        return obs


class AStar:
    """AStar set the cost + heuristics as the priority
    """

    def __init__(self, s_start, s_goal, heuristic_type, pool_cnts, search_safe_pix=None):
        self.s_start = s_start
        self.s_goal = s_goal
        self.heuristic_type = heuristic_type

        self.env = Env(pool_cnts)  # class Env

        self.u_set = self.env.motions  # feasible input set
        self.obs = self.env.obs  # position of obstacles

        self.OPEN = []  # priority queue / OPEN set
        self.CLOSED = []  # CLOSED set / VISITED order
        self.PARENT = dict()  # recorded parent
        self.g = dict()  # cost to come
        if search_safe_pix:
            self.search_safe_pix = search_safe_pix
        else:
            self.search_safe_pix = 20

    def searching(self):
        """
        A_star Searching.
        :return: path, visited order
        """

        self.PARENT[self.s_start] = self.s_start
        self.g[self.s_start] = 0
        self.g[self.s_goal] = math.inf
        heapq.heappush(self.OPEN,
                       (self.f_value(self.s_start), self.s_start))

        while self.OPEN:
            _, s = heapq.heappop(self.OPEN)
            self.CLOSED.append(s)
            # print('s', s)
            if s == self.s_goal:  # stop condition
                break

            for s_n in self.get_neighbor(s):
                if s_n not in self.g:
                    self.g[s_n] = math.inf
                new_cost = self.g[s] + self.cost(s, s_n)
                if new_cost < self.g[s_n]:  # conditions for updating Cost
                    self.g[s_n] = new_cost
                    self.PARENT[s_n] = s
                    heapq.heappush(self.OPEN, (self.f_value(s_n), s_n))
        return self.extract_path(self.PARENT), self.CLOSED

    def searching_repeated_astar(self, e):
        """
        repeated A*.
        :param e: weight of A*
        :return: path and visited order
        """

        path, visited = [], []

        while e >= 1:
            p_k, v_k = self.repeated_searching(self.s_start, self.s_goal, e)
            path.append(p_k)
            visited.append(v_k)
            e -= 0.5

        return path, visited

    def repeated_searching(self, s_start, s_goal, e):
        """
        run A* with weight e.
        :param s_start: starting state
        :param s_goal: goal state
        :param e: weight of a*
        :return: path and visited order.
        """

        g = {s_start: 0, s_goal: float("inf")}
        PARENT = {s_start: s_start}
        OPEN = []
        CLOSED = []
        heapq.heappush(OPEN,
                       (g[s_start] + e * self.heuristic(s_start), s_start))

        while OPEN:
            _, s = heapq.heappop(OPEN)
            CLOSED.append(s)

            if s == s_goal:
                break

            for s_n in self.get_neighbor(s):
                new_cost = g[s] + self.cost(s, s_n)

                if s_n not in g:
                    g[s_n] = math.inf

                if new_cost < g[s_n]:  # conditions for updating Cost
                    g[s_n] = new_cost
                    PARENT[s_n] = s
                    heapq.heappush(OPEN, (g[s_n] + e * self.heuristic(s_n), s_n))

        return self.extract_path(PARENT), CLOSED

    def get_neighbor(self, s):
        """
        find neighbors of state s that not in obstacles.
        :param s: state
        :return: neighbors
        """

        return [(s[0] + u[0], s[1] + u[1]) for u in self.u_set]

    def cost(self, s_start, s_goal):
        """
        Calculate Cost for this motion
        :param s_start: starting node
        :param s_goal: end node
        :return:  Cost for this motion
        :note: Cost function could be more complicate!
        """

        if self.is_collision(s_start, s_goal):
            return math.inf

        return math.hypot(s_goal[0] - s_start[0], s_goal[1] - s_start[1])

    def is_collision(self, s_start, s_end):
        """
        check if the line segment (s_start, s_end) is collision.
        :param s_start: start node
        :param s_end: end node
        :return: True: is collision / False: not collision
        """
        point1 = (s_start[0], s_start[1])
        point2 = (s_end[0], s_end[1])
        in_cnt1 = cv2.pointPolygonTest(np.asarray([self.env.outpool_points]), point1, True)
        in_cnt2 = cv2.pointPolygonTest(np.asarray([self.env.outpool_points]), point2, True)
        # 安全距离
        if in_cnt1 < self.search_safe_pix or in_cnt2 < self.search_safe_pix:
            return True
        else:
            return False
        # if s_start in self.obs or s_end in self.obs:
        #     return True
        # if s_start[0] != s_end[0] and s_start[1] != s_end[1]:
        #     if s_end[0] - s_start[0] == s_start[1] - s_end[1]:
        #         s1 = (min(s_start[0], s_end[0]), min(s_start[1], s_end[1]))
        #         s2 = (max(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
        #     else:
        #         s1 = (min(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
        #         s2 = (max(s_start[0], s_end[0]), min(s_start[1], s_end[1]))
        #     if cv2.pointPolygonTest(np.asarray([self.env.outpool_points]), s1, True)>0:
        #         return True
        #     if cv2.pointPolygonTest(np.asarray([self.env.outpool_points]), s2, True)>0:
        #         return True
        #     # if s1 in self.obs or s2 in self.obs:
        #     #     return True

    def f_value(self, s):
        """
        f = g + h. (g: Cost to come, h: heuristic value)
        :param s: current state
        :return: f
        """

        return self.g[s] + self.heuristic(s)

    def extract_path(self, PARENT):
        """
        Extract the path based on the PARENT set.
        :return: The planning path
        """

        path = [self.s_goal]
        s = self.s_goal

        while True:
            s = PARENT[s]
            path.append(s)

            if s == self.s_start:
                break

        return list(path)

    def heuristic(self, s):
        """
        Calculate heuristic.
        :param s: current node (state)
        :return: heuristic function value
        """

        heuristic_type = self.heuristic_type  # heuristic type
        goal = self.s_goal  # goal node

        if heuristic_type == "manhattan":
            return abs(goal[0] - s[0]) + abs(goal[1] - s[1])
        else:
            return math.hypot(goal[0] - s[0], goal[1] - s[1])


def get_outpool_set(contour, safe_distance=0):
    """
    :param contour 湖泊轮廓
    :param safe_distance 像素安全距离
    """
    # 求坐标点最大外围矩阵
    (x, y, w, h) = cv2.boundingRect(contour)
    # print('(x, y, w, h)', (x, y, w, h))
    # 循环判断点是否在湖泊范围外
    outpool_cnts_set = []
    # 间距
    pix_gap = 1
    # 起始点
    start_x, start_y = x, y
    # 当前点
    current_x, current_y = start_x, start_y + server_config.pix_interval
    # 判断x轴是递增的加还是减 True 为加
    b_add_or_sub = True

    while current_y <= (y + h):
        while current_x <= (x + w) and current_x >= x:
            point = (current_x, current_y)
            in_cnt = cv2.pointPolygonTest(contour, point, True)
            if in_cnt <= safe_distance:
                outpool_cnts_set.append(list(point))
            if b_add_or_sub:
                current_x += server_config.pix_interval
            else:
                current_x -= server_config.pix_interval
        current_y += server_config.pix_interval
        if b_add_or_sub:
            current_x -= server_config.pix_interval
            b_add_or_sub = False
        else:
            current_x += server_config.pix_interval
            b_add_or_sub = True
    return outpool_cnts_set


def distance(p0, p1, digits=2):
    a = map(lambda x: (x[0] - x[1]) ** 2, zip(p0, p1))
    return round(math.sqrt(sum(a)), digits)

# 判断轨迹是否经过陆地区域
def cross_outpool(point_i, point_j, pool_cnts,search_safe_pix=None):
    if not search_safe_pix:
        search_safe_pix=15
    line_points = []
    dx = point_j[0] - point_i[0]
    dy = point_j[1] - point_i[1]
    steps = 0
    # 斜率判断
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)
    # 必有一个等于1，一个小于1
    if steps == 0:
        return True
    delta_x = float(dx / steps)
    delta_y = float(dy / steps)
    # 四舍五入，保证x和y的增量小于等于1，让生成的直线尽量均匀
    x = point_i[0] + 0.5
    y = point_i[1] + 0.5
    for i in range(0, int(steps + 1)):
        # 绘制像素点
        line_points.append([int(x), int(y)])
        x += delta_x
        y += delta_y
    for point in line_points:
        point_temp = (point[0], point[1])
        in_cnt = cv2.pointPolygonTest(pool_cnts, point_temp, True)
        if in_cnt < search_safe_pix:
            # 经过湖泊周围陆地
            return False
    # 不经过陆地
    return True


# path matrix
path_matrix = {}


# 统计点之间距离
def measure_distance(scan_cnt, pool_cnt, map_connect):
    global path_matrix
    l = len(scan_cnt)
    distance_matrix = np.full(shape=(l, l), fill_value=np.inf)
    for i in tqdm(range(l)):
        for j in range(l):
            if i == j:
                distance_matrix[i, j] = 0
            if i > j:
                continue
            d = distance(scan_cnt[i], scan_cnt[j], digits=2)
            distance_matrix[i, j] = d
            distance_matrix[j, i] = d

    for i in tqdm(range(l)):
        c = min(len(scan_cnt), map_connect)
        d = copy.deepcopy(distance_matrix[i, :])
        sort_scan_cnt = list(d)
        sort_scan_cnt.sort()
        end_scan_index_list = [sort_scan_cnt.index(i) for i in sort_scan_cnt[1:1 + c]]
        for j in range(l):
            if i == j:
                distance_matrix[i, j] = 0
                continue
            if i > j:
                continue
            if j in end_scan_index_list and not cross_outpool(scan_cnt[i], scan_cnt[j], pool_cnt):
                print(i, '-->', j, 'False')
                s_index = i
                e_index = j
                s_start = (scan_cnt[s_index][0], scan_cnt[s_index][1])
                s_goal = (scan_cnt[e_index][0], scan_cnt[e_index][1])
                s_start = mod_point(s_start)
                s_goal = mod_point(s_goal)
                # 去不了会搜索报错
                try:
                    astar = AStar(s_start, s_goal, "euclidean", pool_cnt)
                    path, visited = astar.searching()
                    distance_i_j = 0
                    for index_i, value in enumerate(path):
                        if index_i < len(path) - 1:
                            distance_i_j += distance(value, path[index_i + 1])
                    distance_matrix[i, j] = distance_i_j
                    distance_matrix[j, i] = distance_i_j
                    path_matrix.update({'%d_%d' % (i, j): path[::-1]})
                except:
                    print('error searching', i, '-->', j, 'False')
                    distance_matrix[i, j] = math.inf
                    distance_matrix[j, i] = math.inf
            elif not cross_outpool(scan_cnt[i], scan_cnt[j], pool_cnt):
                distance_matrix[i, j] = math.inf
                distance_matrix[j, i] = math.inf
            else:
                dis = distance(scan_cnt[i], scan_cnt[j], digits=2)
                distance_matrix[i, j] = dis
                distance_matrix[j, i] = dis
            if not cross_outpool(scan_cnt[i], scan_cnt[j], pool_cnt):
                print('i,j', i, j)
                distance_matrix[i, j] = math.inf
                distance_matrix[j, i] = math.inf
    return distance_matrix


# 判断points内的点处在同一条直线上吗？
# points内至少有3个点。
def on_one_line(points):
    delta_x = points[1][0] - points[0][0]
    delta_y = points[1][1] - points[0][1]
    distance_square = delta_x ** 2 + delta_y ** 2
    # 传入了相同的点 返回True
    if distance_square == 0:
        return True
    sin_times_cos = delta_x * delta_y / distance_square
    for j in range(2, len(points)):
        dx = points[j][0] - points[0][0]
        dy = points[j][1] - points[0][1]
        if math.fabs(dx * dy / (dx * dx + dy * dy) - sin_times_cos) > 10 ** -9:
            return False
    return True


# 将直线上多个点合并为按直线最少的点
def multi_points_to_simple_points(points):
    if len(points) <= 3:
        return points
    else:
        return_points = []
        test_points = []
        return_points.append(points[0])
        test_points.append(points[0])
        test_points.append(points[1])
        # test_points.append(points[2])
        for index_i in range(2, len(points)):
            test_points.append(points[index_i])
            if on_one_line(test_points):
                pass
            else:
                # if index_i == len(points) - 1:
                return_points.append(test_points[2])
            test_points.pop(0)
        return return_points


# 将点转换为符合模数的数
def mod_point(point):
    point = list(point)
    if point[0] % server_config.pix_interval != 0:
        point[0] = point[0] + server_config.pix_interval - point[0] % server_config.pix_interval
    if point[1] % server_config.pix_interval != 0:
        point[1] = point[1] + +server_config.pix_interval - point[1] % server_config.pix_interval
    point = tuple(point)
    return point


def get_path(baidu_map_obj,
             target_lng_lats,
             b_show=False,
             ):
    """
    根据设置模式返回高德地图上规划路径
    :param baidu_map_obj 地图对象
    :param target_lng_lats 目标经纬度集合，传入为高德经纬度
    :param b_show 是否显示图像
    """
    mode = len(target_lng_lats)
    global path_matrix
    if config.home_debug and baidu_map_obj is None:
        baidu_map_obj = baidu_map.BaiduMap(config.ship_gaode_lng_lat, zoom=16, scale=1,
                                           map_type=baidu_map.MapType.gaode)
        pool_cnts, (pool_cx, pool_cy) = baidu_map_obj.get_pool_pix(b_show=False)
        if pool_cnts is None:
            return 'pool_cx is None'
    if baidu_map_obj.ship_gaode_lng_lat is None:
        return 'no ship gps'

    search_safe_pix = int(config.path_search_safe_distance / baidu_map_obj.pix_2_meter)
    print(config.path_search_safe_distance,baidu_map_obj.pix_2_meter)
    # 单点
    print('mode', mode)
    if mode == 1:
        baidu_map_obj.ship_pix = baidu_map_obj.gaode_lng_lat_to_pix(baidu_map_obj.ship_gaode_lng_lat)

        row_start = tuple(baidu_map_obj.ship_pix)
        row_goal = tuple(baidu_map_obj.gaode_lng_lat_to_pix(target_lng_lats[0]))
        s_start = mod_point(row_start)
        s_goal = mod_point(row_goal)
        print('row_start,row_goal ', row_start, row_goal, 's_start,s_goal', s_start, s_goal,)
        print('search_safe_pix', search_safe_pix)
        # 判断是否能直线到达，不能则采用路径搜索
        if not cross_outpool(s_start, s_goal, baidu_map_obj.pool_cnts, search_safe_pix):
            astar = AStar(s_start, s_goal, "euclidean", baidu_map_obj.pool_cnts, search_safe_pix)
            try:
                astar_path, visited = astar.searching()
                return_pix_path = astar_path[::-1]
                simple_return_pix_path = multi_points_to_simple_points(return_pix_path)
                print('原始长度', len(return_pix_path), '简化后长度', len(simple_return_pix_path))
                _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(simple_return_pix_path)
                if b_show:
                    baidu_map_obj.show_img = cv2.polylines(baidu_map_obj.show_img,
                                                           [np.array(astar_path, dtype=np.int32)], False, (255, 0, 0),
                                                           1)
                    cv2.circle(baidu_map_obj.show_img, s_start, 5, [255, 0, 255], -1)
                    cv2.circle(baidu_map_obj.show_img, s_goal, 5, [255, 0, 255], -1)
                    # baidu_map_obj.show_img = cv2.drawContours(baidu_map_obj.show_img, [return_pix_path], -1,
                    #                                           (0, 0, 255), 3)
                    cv2.imshow('scan', baidu_map_obj.show_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                return return_gaode_lng_lat_path
            except Exception as e:
                print('error ', e)
                if b_show:
                    cv2.circle(baidu_map_obj.show_img, s_start, 5, [0, 255, 0], -1)
                    cv2.circle(baidu_map_obj.show_img, s_goal, 5, [0, 0, 255], -1)
                    cv2.imshow('scan', baidu_map_obj.show_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                return 'can not fand path'
        # 直接可达模式
        else:
            return_pix_path = []
            # return_pix_path.append(row_start)
            return_pix_path.append(row_goal)
            _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(return_pix_path)
            if b_show:
                cv2.circle(baidu_map_obj.show_img, s_start, 5, [255, 255, 0], -1)
                cv2.circle(baidu_map_obj.show_img, s_goal, 5, [255, 255, 0], -1)
                baidu_map_obj.show_img = cv2.drawContours(baidu_map_obj.show_img, np.array([return_pix_path]), -1,
                                                          (0, 0, 255), 3)
                cv2.imshow('scan', cv2.resize(baidu_map_obj.show_img, (512, 512)))
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            return return_gaode_lng_lat_path
    # 多点
    else:
        if target_lng_lats is None:
            return 'target_pixs is None'
        elif len(target_lng_lats) <= 1:
            return 'len(target_pixs) is<=1 choose mode 0'
        baidu_map_obj.ship_pix = baidu_map_obj.gaode_lng_lat_to_pix(baidu_map_obj.ship_gaode_lng_lat)
        target_pixs = []
        for target_lng_lat in target_lng_lats:
            target_pixs.append(baidu_map_obj.gaode_lng_lat_to_pix(target_lng_lat))
        # 使用TSP优化路径
        if config.b_tsp:
            # 测量距离
            distance_matrix = measure_distance(target_pixs, baidu_map_obj.pool_cnts, map_connect=config.find_points_num)
            tsp_path = solve_tsp(distance_matrix)
            if config.b_tsp:
                tsp_path = solve_tsp(distance_matrix)
            path_points = []
            print('path_matrix', path_matrix)
            for index_i, val in enumerate(tsp_path):
                if index_i < len(tsp_path) - 1:
                    if '%d_%d' % (val, tsp_path[index_i + 1]) in path_matrix.keys():
                        path_points.extend(path_matrix['%d_%d' % (val, tsp_path[index_i + 1])])
                    elif '%d_%d' % (tsp_path[index_i + 1], val) in path_matrix.keys():
                        path_points.extend(path_matrix['%d_%d' % (tsp_path[index_i + 1], val)][::-1])
                    else:
                        path_points.append(target_pixs[val])
                elif index_i == len(tsp_path) - 1:
                    if '%d_%d' % (val, tsp_path[index_i - 1]) in path_matrix.keys() or '%d_%d' % (
                            val, tsp_path[index_i - 1]) in path_matrix.keys():
                        pass
                    else:
                        path_points.append(target_pixs[val])
        else:
            path_points = []
            for index, val in enumerate(target_lng_lats):
                if index == 0:
                    row_start = tuple(baidu_map_obj.ship_pix)
                    row_goal = tuple(baidu_map_obj.gaode_lng_lat_to_pix(target_lng_lats[index]))
                else:
                    row_start = tuple(baidu_map_obj.gaode_lng_lat_to_pix(target_lng_lats[index - 1]))
                    row_goal = tuple(baidu_map_obj.gaode_lng_lat_to_pix(target_lng_lats[index]))
                s_start = mod_point(row_start)
                s_goal = mod_point(row_goal)
                print('row_start,row_goal', row_start, row_goal, 's_start,s_goal', s_start, s_goal)
                # 判断是否能直线到达，不能则采用路径搜索
                if not cross_outpool(s_start, s_goal, baidu_map_obj.pool_cnts):
                    astar = AStar(s_start, s_goal, "euclidean", baidu_map_obj.pool_cnts, search_safe_pix)
                    try:
                        astar_path, visited = astar.searching()
                        return_pix_path = astar_path[::-1]
                        # simple_return_pix_path = multi_points_to_simple_points(return_pix_path)
                        # print('原始长度', len(return_pix_path), '简化后长度', len(simple_return_pix_path))
                        # _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(simple_return_pix_path)
                        if b_show:
                            baidu_map_obj.show_img = cv2.polylines(baidu_map_obj.show_img,
                                                                   [np.array(astar_path, dtype=np.int32)], False,
                                                                   (255, 0, 0),
                                                                   1)
                            cv2.circle(baidu_map_obj.show_img, s_start, 5, [255, 0, 255], -1)
                            cv2.circle(baidu_map_obj.show_img, s_goal, 5, [255, 0, 255], -1)
                            # baidu_map_obj.show_img = cv2.drawContours(baidu_map_obj.show_img, [return_pix_path], -1,
                            #                                           (0, 0, 255), 3)
                            cv2.imshow('scan', baidu_map_obj.show_img)
                            cv2.waitKey(0)
                            cv2.destroyAllWindows()
                        path_points.extend(return_pix_path)
                    except Exception as e:
                        print('error ', e)
                        if b_show:
                            cv2.circle(baidu_map_obj.show_img, s_start, 5, [0, 255, 0], -1)
                            cv2.circle(baidu_map_obj.show_img, s_goal, 5, [0, 0, 255], -1)
                            cv2.imshow('scan', baidu_map_obj.show_img)
                            cv2.waitKey(0)
                            cv2.destroyAllWindows()
                        path_points.append(row_goal)
                # 直接可达模式
                else:
                    path_points.append(list(row_goal))
        return_pix_path = path_points
        # print('原始长度', len(return_pix_path))
        # return_pix_path = multi_points_to_simple_points(return_pix_path)
        # print('简化后长度', len(return_pix_path))
        _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(return_pix_path)
        if b_show:
            baidu_map_obj.show_img = cv2.polylines(baidu_map_obj.show_img, [np.array(path_points, dtype=np.int32)],
                                                   False, (255, 0, 0), 1)
            cv2.imshow('scan', baidu_map_obj.show_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return return_gaode_lng_lat_path


if __name__ == '__main__':
    config.home_debug = True
    # 114.431299,30.521363
    # 114.433853,30.519553
    # 114.432477, 30.521501
    # [114.431133,30.522252],[114.432464,30.521108],[114.430983,30.519953],[114.432625,30.52036],[114.430726,30.519158],[114.430726,30.519158],[114.433853,30.519553]
    # r1 = get_path(mode=0,b_show=True,target_lng_lats=[[114.347533,30.465757]])
    # print('r1', r1)
    r2 = get_path(b_show=True, target_lng_lats=[[114.347533, 30.465757],
                                                [114.346803, 30.46401],
                                                [114.347189, 30.462891],
                                                [114.348927, 30.463168],
                                                [114.349957, 30.462946]])
    print('r2', r2)

# baidu_map_obj.ship_pix [566, 565]
# (x, y, w, h) (420, 249, 414, 653)
