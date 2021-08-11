import numpy as np
import math
# import matplotlib.pyplot as plt

k = 0.1  # 前视距离系数
Lfc = 5.0  # 前视距离
Kp = 1.0  # 速度P控制器系数
dt = 0.1  # 时间间隔，单位：s
L = 1.5  # 车辆轴距，单位：m


class PurePursuit:
    def __init__(self, lng=0.0, lat=0.0, yaw=0.0, v=0.0):
        """
        :param x: 经度
        :param y: 纬度
        :param yaw: 偏航角
        :param v: 速度
        """
        self.lng = lng
        self.lat = lat
        self.yaw = yaw
        self.v = v

    def update(self, lng, lat, yaw, v):
        self.lng = lng
        self.lat = lat
        self.yaw = yaw
        self.v = v

    def calc_target_index(self, cx, cy):
        # 搜索最临近的路点
        dx = [self.lng - icx for icx in cx]
        dy = [self.lat - icy for icy in cy]
        d = [abs(math.sqrt(idx ** 2 + idy ** 2)) for (idx, idy) in zip(dx, dy)]
        ind = d.index(min(d))
        L = 0.0
        Lf = k * self.v + Lfc

        while Lf > L and (ind + 1) < len(cx):
            dx = cx[ind + 1] - cx[ind]
            dy = cx[ind + 1] - cx[ind]
            L += math.sqrt(dx ** 2 + dy ** 2)
            ind += 1
        return ind

    def p_control(self, target, current):
        a = Kp * (target - current)
        return a

    def pure_pursuit_control(self, cx, cy, pind):
        ind = self.calc_target_index(cx, cy)
        if pind >= ind:
            ind = pind
        if ind < len(cx):
            tx = cx[ind]
            ty = cy[ind]
        else:
            tx = cx[-1]
            ty = cy[-1]
            ind = len(cx) - 1
        alpha = math.atan2(ty - self.lat, tx - self.lng) - self.yaw
        if self.v < 0:  # back
            alpha = math.pi - alpha
        Lf = k * self.v + Lfc
        delta = math.atan2(2.0 * L * math.sin(alpha) / Lf, 1.0)
        return delta, ind

    def pid_pwm(self,distance,theta_error):
        left_pwm=0
        right_pwm=0
        return left_pwm,right_pwm



def main():
    #  设置目标路点
    cx = np.arange(0, 50, 1)
    cy = [math.sin(ix / 5.0) * ix / 2.0 for ix in cx]
    target_speed = 10.0 / 3.6  # [m/s]
    T = 100.0  # 最大模拟时间
    # 设置车辆的初始状态
    vehicle = PurePursuit(lng=-0.0, lat=-3.0, yaw=0.0, v=0.0)
    lastIndex = len(cx) - 1
    time = 0.0
    x = [vehicle.lng]
    y = [vehicle.lat]
    yaw = [vehicle.yaw]
    v = [vehicle.v]
    t = [0.0]
    target_ind = vehicle.calc_target_index(cx, cy)

    while T >= time and lastIndex > target_ind:
        ai = vehicle.p_control(target_speed, vehicle.v)
        di, target_ind = vehicle.pure_pursuit_control(cx, cy, target_ind)
        x_cal = vehicle.lng + vehicle.v * math.cos(vehicle.yaw) * dt
        y_cal = vehicle.lat + vehicle.v * math.sin(vehicle.yaw) * dt
        yaw_cal = vehicle.yaw + vehicle.v / L * math.tan(di) * dt
        v_cal = vehicle.v + ai * dt
        vehicle.update(x_cal, y_cal, yaw_cal, v_cal)
        time = time + dt
        x.append(vehicle.lng)
        y.append(vehicle.lat)
        yaw.append(vehicle.yaw)
        v.append(vehicle.v)
        t.append(time)
        # plt.cla()
        # plt.plot(cx, cy, ".r", label="course")
        # plt.plot(x, y, "-b", label="trajectory")
        # plt.plot(cx[target_ind], cy[target_ind], "go", label="target")
        # plt.axis("equal")
        # plt.grid(True)
        # plt.title("Speed[km/h]:" + str(vehicle.v * 3.6)[:4])
        # plt.pause(0.001)


# 纯追踪控制控制转向角度，使用一个简单的P控制器控制速度
if __name__ == '__main__':
    main()
