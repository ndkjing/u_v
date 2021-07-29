"""
RRT_CONNECT_2D
@author: huiming zhou
"""

import numpy as np
import math
import cv2
from tsp_solver.greedy import solve_tsp
import copy
from tqdm import tqdm

import config
from externalConnect import baidu_map


class Utils:
    def __init__(self,pool_cnts):
        self.env = Env(pool_cnts)
        self.pool_cnts = pool_cnts
        self.delta = 0.5

    def update_obs(self, obs_cir, obs_bound, obs_rec):
        self.obs_circle = obs_cir
        self.obs_boundary = obs_bound
        self.obs_rectangle = obs_rec

    def get_obs_vertex(self):
        delta = self.delta
        obs_list = []

        for (ox, oy, w, h) in self.obs_rectangle:
            vertex_list = [[ox - delta, oy - delta],
                           [ox + w + delta, oy - delta],
                           [ox + w + delta, oy + h + delta],
                           [ox - delta, oy + h + delta]]
            obs_list.append(vertex_list)

        return obs_list

    def is_intersect_rec(self, start, end, o, d, a, b):
        v1 = [o[0] - a[0], o[1] - a[1]]
        v2 = [b[0] - a[0], b[1] - a[1]]
        v3 = [-d[1], d[0]]

        div = np.dot(v2, v3)

        if div == 0:
            return False

        t1 = np.linalg.norm(np.cross(v2, v1)) / div
        t2 = np.dot(v1, v3) / div

        if t1 >= 0 and 0 <= t2 <= 1:
            shot = Node((o[0] + t1 * d[0], o[1] + t1 * d[1]))
            dist_obs = self.get_dist(start, shot)
            dist_seg = self.get_dist(start, end)
            if dist_obs <= dist_seg:
                return True

        return False

    def is_intersect_circle(self, o, d, a, r):
        d2 = np.dot(d, d)
        delta = self.delta

        if d2 == 0:
            return False

        t = np.dot([a[0] - o[0], a[1] - o[1]], d) / d2

        if 0 <= t <= 1:
            shot = Node((o[0] + t * d[0], o[1] + t * d[1]))
            if self.get_dist(shot, Node(a)) <= r + delta:
                return True
        return False

    def is_collision(self, start, end):
        # print()
        in_cnt1 = cv2.pointPolygonTest(np.array(self.pool_cnts), (int(start.x), int(start.y)), False)
        in_cnt2 = cv2.pointPolygonTest(np.array(self.pool_cnts), (int(end.x), int(end.y)), False)
        # 使用经纬度判断 大于0说明属于该轮廓
        if in_cnt1 >= 0 or in_cnt2 >= 0:
            return True

        o, d = self.get_ray(start, end)
        obs_vertex = self.get_obs_vertex()

        for (v1, v2, v3, v4) in obs_vertex:
            if self.is_intersect_rec(start, end, o, d, v1, v2):
                return True
            if self.is_intersect_rec(start, end, o, d, v2, v3):
                return True
            if self.is_intersect_rec(start, end, o, d, v3, v4):
                return True
            if self.is_intersect_rec(start, end, o, d, v4, v1):
                return True

        for (x, y, r) in self.obs_circle:
            if self.is_intersect_circle(o, d, [x, y], r):
                return True
        return False

    def is_inside_obs(self, node):
        delta = self.delta

        for (x, y, r) in self.obs_circle:
            if math.hypot(node.x - x, node.y - y) <= r + delta:
                return True

        for (x, y, w, h) in self.obs_rectangle:
            if 0 <= node.x - (x - delta) <= w + 2 * delta \
                    and 0 <= node.y - (y - delta) <= h + 2 * delta:
                return True

        for (x, y, w, h) in self.obs_boundary:
            if 0 <= node.x - (x - delta) <= w + 2 * delta \
                    and 0 <= node.y - (y - delta) <= h + 2 * delta:
                return True
        return False

    @staticmethod
    def get_ray(start, end):
        orig = [start.x, start.y]
        direc = [end.x - start.x, end.y - start.y]
        return orig, direc

    @staticmethod
    def get_dist(start, end):
        return math.hypot(end.x - start.x, end.y - start.y)

class Env:
    def __init__(self,pool_cnts):
        (x, y, w, h) = cv2.boundingRect(np.asarray(pool_cnts))
        self.x_range = (0, w)
        self.y_range = (0, h)
        self.pool_cnts = pool_cnts

class Node:
    def __init__(self, n):
        self.x = n[0]
        self.y = n[1]
        self.parent = None

class RrtConnect:
    def __init__(self, s_start, s_goal, step_len, goal_sample_rate, iter_max,pool_cnts):
        self.s_start = Node(s_start)
        self.s_goal = Node(s_goal)
        self.step_len = step_len
        self.goal_sample_rate = goal_sample_rate
        self.iter_max = iter_max
        self.V1 = [self.s_start]
        self.V2 = [self.s_goal]

        self.env =Env(pool_cnts)
        # self.plotting = plotting.Plotting(s_start, s_goal)
        self.utils = Utils(pool_cnts)

        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.pool_cnts = self.env.pool_cnts


    def planning(self):
        for i in range(self.iter_max):
            node_rand = self.generate_random_node(self.s_goal, self.goal_sample_rate)
            node_near = self.nearest_neighbor(self.V1, node_rand)
            node_new = self.new_state(node_near, node_rand)

            if node_new and not self.utils.is_collision(node_near, node_new):
                self.V1.append(node_new)
                node_near_prim = self.nearest_neighbor(self.V2, node_new)
                node_new_prim = self.new_state(node_near_prim, node_new)

                if node_new_prim and not self.utils.is_collision(node_new_prim, node_near_prim):
                    self.V2.append(node_new_prim)

                    while True:
                        node_new_prim2 = self.new_state(node_new_prim, node_new)
                        if node_new_prim2 and not self.utils.is_collision(node_new_prim2, node_new_prim):
                            self.V2.append(node_new_prim2)
                            node_new_prim = self.change_node(node_new_prim, node_new_prim2)
                        else:
                            break

                        if self.is_node_same(node_new_prim, node_new):
                            break

                if self.is_node_same(node_new_prim, node_new):
                    return self.extract_path(node_new, node_new_prim)

            if len(self.V2) < len(self.V1):
                list_mid = self.V2
                self.V2 = self.V1
                self.V1 = list_mid

        return None

    @staticmethod
    def change_node(node_new_prim, node_new_prim2):
        node_new = Node((node_new_prim2.x, node_new_prim2.y))
        node_new.parent = node_new_prim

        return node_new

    @staticmethod
    def is_node_same(node_new_prim, node_new):
        if node_new_prim.x == node_new.x and \
                node_new_prim.y == node_new.y:
            return True

        return False

    def generate_random_node(self, sample_goal, goal_sample_rate):
        delta = self.utils.delta

        if np.random.random() > goal_sample_rate:
            return Node((int(np.random.uniform(self.x_range[0] + delta, self.x_range[1] - delta)),
                         int(np.random.uniform(self.y_range[0] + delta, self.y_range[1] - delta))))
        return sample_goal

    @staticmethod
    def nearest_neighbor(node_list, n):
        return node_list[int(np.argmin([math.hypot(nd.x - n.x, nd.y - n.y)
                                        for nd in node_list]))]

    def new_state(self, node_start, node_end):
        dist, theta = self.get_distance_and_angle(node_start, node_end)
        dist = min(self.step_len, dist)
        node_new = Node((int(node_start.x + dist * math.cos(theta)),
                         int(node_start.y + dist * math.sin(theta))))
        node_new.parent = node_start
        return node_new

    @staticmethod
    def extract_path(node_new, node_new_prim):
        path1 = [(node_new.x, node_new.y)]
        node_now = node_new

        while node_now.parent is not None:
            node_now = node_now.parent
            path1.append((node_now.x, node_now.y))

        path2 = [(node_new_prim.x, node_new_prim.y)]
        node_now = node_new_prim

        while node_now.parent is not None:
            node_now = node_now.parent
            path2.append((node_now.x, node_now.y))

        return list(list(reversed(path1)) + path2)

    @staticmethod
    def get_distance_and_angle(node_start, node_end):
        dx = node_end.x - node_start.x
        dy = node_end.y - node_start.y
        return math.hypot(dx, dy), math.atan2(dy, dx)

def get_outpool_set(contour,safe_distance=0):
    """
    :param contour 湖泊轮廓
    :param safe_distance 像素安全距离
    """
    # 求坐标点最大外围矩阵
    (x, y, w, h) = cv2.boundingRect(contour)
    print('(x, y, w, h)', (x, y, w, h))
    # 循环判断点是否在湖泊范围外
    outpool_cnts_set = []
    # 间距
    pix_gap = 1
    # 起始点
    start_x, start_y = x, y + pix_gap
    # 当前点
    current_x, current_y = start_x, start_y
    # 判断x轴是递增的加还是减 True 为加
    b_add_or_sub = True

    while current_y <= (y + h):
        while current_x <= (x + w) and current_x >= x:
            point = (current_x, current_y)
            in_cnt = cv2.pointPolygonTest(contour, point, True)
            if in_cnt <= safe_distance:
                outpool_cnts_set.append(list(point))
            if b_add_or_sub:
                current_x += pix_gap
            else:
                current_x -= pix_gap
        current_y += pix_gap
        if b_add_or_sub:
            current_x -= pix_gap
            b_add_or_sub = False
        else:
            current_x += pix_gap
            b_add_or_sub = True
    return outpool_cnts_set


def distance(p0, p1, digits=2):
    a = map(lambda x: (x[0] - x[1]) ** 2, zip(p0, p1))
    return round(math.sqrt(sum(a)), digits)

safe_distance=0

# 判断轨迹是否经过陆地区域
def cross_outpool(point_i,point_j,pool_cnts):
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
    if steps==0:
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
        if in_cnt < safe_distance:
            # 经过湖泊周围陆地
            return False
    # 不经过陆地
    return True


# path matrix
path_matrix = {}

# 统计点之间距离
def measure_distance(scan_cnt,pool_cnt,outpool_set,map_connect):
    global path_matrix
    l = len(scan_cnt)
    distance_matrix = np.full(shape=(l, l),fill_value=np.inf)
    for i in tqdm(range(l)):
        for j in range(l):
            if i == j:
                distance_matrix[i, j] = 0
            if i > j :
                continue
            d = distance(scan_cnt[i], scan_cnt[j], digits=2)
            distance_matrix[i,j] =d
            distance_matrix[j,i] =d

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
            if j in end_scan_index_list and not cross_outpool(scan_cnt[i],scan_cnt[j],pool_cnt):
                print(i,'-->',j,'False')
                s_index = i
                e_index = j
                s_start = (scan_cnt[s_index][0], scan_cnt[s_index][1])
                s_goal = (scan_cnt[e_index][0], scan_cnt[e_index][1])
                # 去不了会搜索报错
                try:
                    # astar = AStar(s_start, s_goal, "euclidean", outpool_set)
                    # path, visited = astar.searching()
                    rrt_conn = RrtConnect(s_start, s_goal, 1, 0.05, 5000)
                    path = rrt_conn.planning()
                    distance_i_j = 0
                    for index_i, value in enumerate(path):
                        if index_i < len(path) - 1:
                            distance_i_j += distance(value, path[index_i + 1])
                    distance_matrix[i, j] = distance_i_j
                    distance_matrix[j, i] = distance_i_j
                    path_matrix.update({'%d_%d' % (i, j): path[::-1]})
                except:
                    print('error searching',i,'-->',j,'False')
                    distance_matrix[i, j] = math.inf
                    distance_matrix[j, i] = math.inf
            elif not cross_outpool(scan_cnt[i],scan_cnt[j],pool_cnt):
                distance_matrix[i, j] = math.inf
                distance_matrix[j, i] = math.inf
            else:
                dis = distance(scan_cnt[i], scan_cnt[j], digits=2)
                distance_matrix[i,j] =dis
                distance_matrix[j,i] =dis
            if not cross_outpool(scan_cnt[i],scan_cnt[j],pool_cnt):
                print('i,j',i,j)
                distance_matrix[i, j] = math.inf
                distance_matrix[j, i] = math.inf

    return distance_matrix


def return_to_base(point1,point2,baidu_map_obj,b_show=False):
    """
    return to start point
    """
    plus=1000
    s_start =tuple([int(point1[0]*plus),int(point1[1]*plus)])
    s_goal = tuple([int(point2[0]*plus),int(point2[1]*plus)])
    _,outpool_lng_lats_set = baidu_map_obj.pix_to_gps(baidu_map_obj.outpool_cnts_set)
    baidu_map_obj.outpool_lng_lats_set = [[int(i[0]*plus),int(i[1]*plus)] for i in outpool_lng_lats_set]
    in_cnt_start = cv2.pointPolygonTest(np.array(baidu_map_obj.outpool_lng_lats_set), s_start, True)
    in_cnt_goal = cv2.pointPolygonTest(np.array(baidu_map_obj.outpool_lng_lats_set), s_goal, True)
    print('in_cnt_start', in_cnt_start)
    print('in_cnt_goal', in_cnt_goal)
    # astar = AStar(s_start, s_goal, "euclidean", baidu_map_obj.outpool_lng_lats_set)
    # astar_path, visited = astar.searching()
    rrt_conn = RrtConnect(s_start, s_goal, 1, 0.05, 5000)
    astar_path = rrt_conn.planning()
    print('astar_path', astar_path)
    return astar_path

#判断points内的点处在同一条直线上吗？
#points内至少有3个点。
def on_one_line(points):
    delta_x = points[1][0] - points[0][0]
    delta_y = points[1][1] - points[0][1]
    distance_square = delta_x **2 + delta_y **2
    # 传入了相同的点 返回True
    if distance_square==0:
        return True
    sin_times_cos = delta_x * delta_y/ distance_square
    for j in range(2, len(points)):
        dx = points[j][0] - points[0][0]
        dy = points[j][1] - points[0][1]
        if math.fabs(dx * dy / (dx * dx + dy * dy) - sin_times_cos) > 10 ** -9:
            return False
    return True

# 将直线上多个点合并为按直线最少的点
def multi_points_to_simple_points(points):
    if len(points)<=3:
        return points
    else:
        return_points=[]
        test_points = []
        return_points.append(points[0])
        test_points.append(points[0])
        test_points.append(points[1])
        # test_points.append(points[2])
        for index_i in range(2,len(points)):
            test_points.append(points[index_i])
            if on_one_line(test_points):
                pass
            else:
                # if index_i == len(points) - 1:
                return_points.append(test_points[2])
            test_points.pop(0)
        return return_points

def get_path(baidu_map_obj=None,
             mode=0,
             target_lng_lats=None,
             target_pixs=None,
             b_show=False,
             back_home=False,
             map_connect = 7,
             pix_gap=30):
    """
    根据设置模式返回高德地图上规划路径
    :param baidu_map_obj 地图对象
    :param mode 选择模式
    :param target_lng_lats 目标经纬度集合，传入为高德经纬度
    :param target_pixs 目标像素
    :param b_show 是否显示图像
    :param map_connect 搜索一个点最多连接数量
    :param pix_gap 自动搜索像素间隔
    mode
    ０　到达目标点后停留
    １　到达多个目标点
    ２　扫描整个湖泊
    4  返航
    """
    global path_matrix
    if baidu_map_obj==None:
        baidu_map_obj = baidu_map.BaiduMap(config.ship_gaode_lng_lat, zoom=16, scale=1, map_type=baidu_map.MapType.gaode)
        pool_cnts,(pool_cx,pool_cy) = baidu_map_obj.get_pool_pix(b_show=False)
        if pool_cnts is None:
            return 'pool_cx is None'
    baidu_map_obj.outpool_cnts_set = get_outpool_set(np.array(baidu_map_obj.pool_cnts))

    # 无GPS调试模式 以湖泊中心作为起点
    if config.home_debug:
        baidu_map_obj.ship_gaode_lng_lat=config.ship_gaode_lng_lat
        baidu_map_obj.ship_gps=config.ship_gaode_lng_lat

    if baidu_map_obj.ship_gps is None:
        return 'no ship gps'
    if mode==0:
        if target_lng_lats is None:
            return 'target_pixs is None'
        elif len(target_lng_lats)>1:
            return 'len(target_pixs) is >1 choose mode 1'
        if baidu_map_obj.ship_pix is None :
            if baidu_map_obj.ship_gaode_lng_lat is None :
                baidu_map_obj.ship_gaode_lng_lat = baidu_map_obj.gps_to_gaode_lng_lat(baidu_map_obj.ship_gps)
            baidu_map_obj.ship_pix = baidu_map_obj.gaode_lng_lat_to_pix(baidu_map_obj.ship_gaode_lng_lat)
        s_start = tuple(baidu_map_obj.ship_pix)
        s_goal = tuple(baidu_map_obj.gaode_lng_lat_to_pix(target_lng_lats[0]))
        print('s_start,s_goal',s_start,s_goal)
        # 判断是否能直线到达，不能则采用路径搜索
        if not cross_outpool(s_start,s_goal,baidu_map_obj.pool_cnts):
            try:
                # astar = AStar(s_start, s_goal, "euclidean", baidu_map_obj.outpool_cnts_set)
                # astar_path, visited = astar.searching()
                rrt_conn = RrtConnect(s_start, s_goal, 1, 0.1, 10000,baidu_map_obj.pool_cnts)
                astar_path = rrt_conn.planning()
                print('astar_path', astar_path)
                return_pix_path = astar_path[::-1]
                # 返航时添加
                if back_home:
                    return_pix_path.append(astar_path)
                print('原始长度',len(return_pix_path))
                return_pix_path = multi_points_to_simple_points(return_pix_path)
                print('简化后长度', len(return_pix_path))
                _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(return_pix_path)
                if b_show:
                    baidu_map_obj.show_img = cv2.polylines(baidu_map_obj.show_img,
                                                           [np.array(astar_path, dtype=np.int32)], False, (255, 0, 0),
                                                           1)
                    cv2.circle(baidu_map_obj.show_img, s_start, 5, [255, 0,255], -1)
                    cv2.circle(baidu_map_obj.show_img, s_goal, 5, [255, 0,255], -1)
                    baidu_map_obj.show_img = cv2.drawContours(baidu_map_obj.show_img, [return_pix_path], -1,
                                                              (0, 0, 255), 3)
                    cv2.imshow('scan', baidu_map_obj.show_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                return return_gaode_lng_lat_path
            except Exception as e :
                print('error ',e)
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
            return_pix_path.append(s_start)
            return_pix_path.append(s_goal)
            _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(return_pix_path)
            if b_show:
                cv2.circle(baidu_map_obj.show_img, s_start, 5, [255, 255, 0], -1)
                cv2.circle(baidu_map_obj.show_img, s_goal, 5, [255, 255, 0], -1)
                baidu_map_obj.show_img = cv2.drawContours(baidu_map_obj.show_img, np.array([return_pix_path]), -1,
                                                          (0, 0, 255), 3)
                cv2.imshow('scan', baidu_map_obj.show_img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            # 返航时添加家的经纬度
            if back_home:
                if config.home_debug:
                    return_gaode_lng_lat_path.append(config.ship_gaode_lng_lat)
                else:
                    return_gaode_lng_lat_path.append(baidu_map_obj.init_ship_gaode_lng_lat)
            return return_gaode_lng_lat_path

    elif mode == 1:
        if target_lng_lats is None:
            return 'target_pixs is None'
        elif len(target_lng_lats) <= 1:
            return 'len(target_pixs) is<=1 choose mode 0'
        if baidu_map_obj.ship_pix is None:
            if baidu_map_obj.ship_gaode_lng_lat is None:
                baidu_map_obj.ship_gaode_lng_lat = baidu_map_obj.gps_to_gaode_lng_lat(baidu_map_obj.ship_gps)
            baidu_map_obj.ship_pix = baidu_map_obj.gaode_lng_lat_to_pix(baidu_map_obj.ship_gaode_lng_lat)

        target_pixs=[]
        for target_lng_lat in target_lng_lats:
            target_pixs.append(baidu_map_obj.gaode_lng_lat_to_pix(target_lng_lat))
        target_pixs.insert(0,baidu_map_obj.ship_pix)
        distance_matrix = measure_distance(target_pixs,baidu_map_obj.pool_cnts,baidu_map_obj.outpool_cnts_set,map_connect=config.find_points_num)
        if back_home:
            tsp_path = solve_tsp(distance_matrix, endpoints=(0, 0))
        else:
            tsp_path = solve_tsp(distance_matrix, endpoints=(0, (len(target_pixs) - 1)))
        path_points=[]
        print('path_matrix',path_matrix)
        for index_i,val in enumerate(tsp_path):
            if index_i < len(tsp_path) - 1:
                if '%d_%d'%(val,tsp_path[index_i+1]) in path_matrix.keys():
                    path_points.extend(path_matrix['%d_%d'%(val,tsp_path[index_i+1])])
                elif '%d_%d'%(tsp_path[index_i+1],val) in path_matrix.keys():
                    path_points.extend(path_matrix['%d_%d' % (tsp_path[index_i + 1],val)][::-1])
                else:
                    path_points.append(target_pixs[val])
            elif index_i == len(tsp_path) - 1:
                if '%d_%d'%(val,tsp_path[index_i-1]) in path_matrix.keys() or '%d_%d'%(val,tsp_path[index_i-1]) in path_matrix.keys():
                    pass
                else:
                    path_points.append(target_pixs[val])

        return_pix_path = path_points
        print('原始长度', len(return_pix_path))
        return_pix_path = multi_points_to_simple_points(return_pix_path)
        print('简化后长度', len(return_pix_path))

        _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(return_pix_path)
        if b_show:
            baidu_map_obj.show_img = cv2.polylines(baidu_map_obj.show_img, [np.array(path_points, dtype=np.int32)],
                                                   False, (255, 0, 0), 1)
            cv2.imshow('scan', baidu_map_obj.show_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return return_gaode_lng_lat_path

    elif mode == 2:
        baidu_map_obj.scan_pool(baidu_map_obj.pool_cnts, pix_gap=pix_gap, b_show=False)
        print('len(scan_cnt)', len(baidu_map_obj.scan_point_cnts))
        distance_matrix = measure_distance(baidu_map_obj.scan_point_cnts,baidu_map_obj.pool_cnts,baidu_map_obj.outpool_cnts_set,map_connect=map_connect)
        tsp_path = solve_tsp(distance_matrix,endpoints=(0,0))
        print('tsp_path',tsp_path)
        path_points = []
        print('baidu_map_obj.pool_cnts', baidu_map_obj.pool_cnts)
        print('path_matrix',path_matrix)
        print('list path_matrix',list(path_matrix.keys()))
        for index_i,val in enumerate(tsp_path):
            if index_i < len(tsp_path) - 1:
                if '%d_%d'%(val,tsp_path[index_i+1]) in path_matrix.keys():
                    path_points.extend(path_matrix['%d_%d'%(val,tsp_path[index_i+1])])
                elif '%d_%d'%(tsp_path[index_i+1],val) in path_matrix.keys():
                    path_points.extend(path_matrix['%d_%d' % (tsp_path[index_i + 1],val)][::-1])
                else:
                    path_points.append(baidu_map_obj.scan_point_cnts[val])
            elif index_i == len(tsp_path) - 1:
                if '%d_%d'%(val,tsp_path[index_i-1]) in path_matrix.keys() or '%d_%d'%(val,tsp_path[index_i-1]) in path_matrix.keys():
                    pass
                else:
                    pass
                    # path_points.append(baidu_map_obj.scan_point_cnts[val])
        if b_show:
            baidu_map_obj.show_img = cv2.polylines(baidu_map_obj.show_img, [np.array(path_points, dtype=np.int32)],
                                                   False, (255, 0, 0), 1)
            cv2.imshow('scan', baidu_map_obj.show_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return_pix_path = path_points
        return_pix_path = path_points
        print('原始长度', len(return_pix_path))
        return_pix_path = multi_points_to_simple_points(return_pix_path)
        print('简化后长度', len(return_pix_path))
        _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(return_pix_path)
        return return_gaode_lng_lat_path

    elif mode == 3:
        pass

    # back home
    elif mode == 4:
        if baidu_map_obj.init_ship_gps is None:
            return 'ship init gps is None'
        if baidu_map_obj.init_ship_pix is None:
            if baidu_map_obj.init_ship_gaode_lng_lat is None:
                baidu_map_obj.init_ship_gaode_lng_lat= baidu_map_obj.gps_to_gaode_lng_lat(baidu_map_obj.init_ship_gps)
            baidu_map_obj.init_ship_pix = baidu_map_obj.gaode_lng_lat_to_pix(baidu_map_obj.init_ship_gaode_lng_lat)

        baidu_map_obj.ship_gaode_lng_lat = baidu_map_obj.gps_to_gaode_lng_lat(baidu_map_obj.ship_gps)
        baidu_map_obj.ship_pix = baidu_map_obj.gaode_lng_lat_to_pix(baidu_map_obj.ship_gaode_lng_lat)

        s_start = tuple(baidu_map_obj.ship_pix)
        s_goal = tuple(baidu_map_obj.init_ship_pix)
        print('s_start,s_goal', s_start, s_goal)
        # 判断是否能直线到达，不能则采用路径搜索
        if not cross_outpool(s_start, s_goal, baidu_map_obj.pool_cnts):
            rrt_conn = RrtConnect(s_start, s_goal, 1, 0.05, 100000,baidu_map_obj.pool_cnts)
            astar_path = rrt_conn.planning()
            print('astar_path', astar_path)
            baidu_map_obj.show_img = cv2.polylines(baidu_map_obj.show_img, [np.array(astar_path, dtype=np.int32)],
                                                   False, (255, 0, 0), 1)
            return_pix_path = astar_path[::-1]
            return_pix_path = multi_points_to_simple_points(return_pix_path)
            _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(return_pix_path)
            if b_show:
                cv2.circle(baidu_map_obj.show_img, s_start, 5, [255, 0, 255], -1)
                cv2.circle(baidu_map_obj.show_img, s_goal, 5, [0, 0, 255], -1)
                baidu_map_obj.show_img = cv2.drawContours(baidu_map_obj.show_img, [return_pix_path], -1, (0, 0, 255), 3)
                cv2.imshow('scan', baidu_map_obj.show_img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            return return_gaode_lng_lat_path
            # except:
            #     if b_show:
            #         cv2.circle(baidu_map_obj.show_img, s_start, 5, [255, 255, 0], -1)
            #         cv2.circle(baidu_map_obj.show_img, s_goal, 5, [255, 255, 0], -1)
            #         baidu_map_obj.show_img = cv2.drawContours(baidu_map_obj.show_img, [return_pix_path], -1, (0, 0, 255), 3)
            #
            #         cv2.imshow('scan', baidu_map_obj.show_img)
            #         cv2.waitKey(0)
            #         cv2.destroyAllWindows()
            #         return -3
        # 直接可达模式
        else:
            return_pix_path = []
            return_pix_path.append(s_start)
            return_pix_path.append(s_goal)
            _, return_gaode_lng_lat_path = baidu_map_obj.pix_to_gps(return_pix_path)
            if b_show:
                cv2.circle(baidu_map_obj.show_img, s_start, 5, [255, 255, 0], -1)
                cv2.circle(baidu_map_obj.show_img, s_goal, 5, [255, 255, 0], -1)
                cv2.imshow('scan', baidu_map_obj.show_img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            return return_gaode_lng_lat_path
    else:
        return 1

if __name__ == '__main__':
    # 初始化高德经纬度[114.431804, 30.524169]
    # 114.431299,30.521363
    # 114.434323,30.520183
    # 4  114.433247,30.520328
    #1 114.433279,30.525809  2 114.42938,30.525924  3 114.428924,30.520329   4 114.433204,30.520365
    # [114.431133,30.522252],[114.432464,30.521108],[114.430983,30.519953],[114.432625,30.52036],[114.430726,30.519158],[114.430726,30.519158],[114.433853,30.519553]
    r = get_path(mode=0,b_show=True,target_lng_lats=[[114.432608,30.527356]])
    # r = get_path(mode=2,b_show=True,pix_gap=150)
    print('r',r)

# def main():
#     x_start = (2, 2)  # Starting node
#     x_goal = (49, 24)  # Goal node
#
#     rrt_conn = RrtConnect(x_start, x_goal, 1, 0.05, 5000)
#     path = rrt_conn.planning()
#     print('path',path)
#     # rrt_conn.plotting.animation_connect(rrt_conn.V1, rrt_conn.V2, path, "RRT_CONNECT")
#
#
# if __name__ == '__main__':
#     main()
