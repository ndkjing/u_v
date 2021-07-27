import numpy as np
import cv2


class RadarScan:
    def __init__(self):
        # 生成一个700*700的空灰度图像
        self.canvas = np.zeros((700, 700, 3), np.uint8)
        self.point_size = 1
        self.white = (255, 255, 255)
        self.red = (0, 0, 255)
        self.blue = (255, 0, 0)
        self.yellow = (0, 255, 255)

        # 绘制雷达显示器界面的同心圆
        cv2.circle(self.canvas, (350, 350), 100, self.white, 2)
        cv2.circle(self.canvas, (350, 350), 200, self.white, 2)
        cv2.circle(self.canvas, (350, 350), 300, self.white, 2)
        # 绘制十字线
        cv2.line(self.canvas, (50, 350), (650, 350), self.white, 2)
        cv2.line(self.canvas, (350, 50), (350, 650), self.white, 2)
        start_point = (int(350 - 300 * np.sin(0.25 * np.pi)), int(350 - 300 * np.sin(0.25 * np.pi)))
        end_point = (int(350 + 300 * np.sin(0.25 * np.pi)), int(350 + 300 * np.sin(0.25 * np.pi)))
        cv2.line(self.canvas, start_point, end_point, self.white, 1)
        start_point = (int(350 - 300 * np.sin(0.25 * np.pi)), int(350 + 300 * np.sin(0.25 * np.pi)))
        end_point = (int(350 + 300 * np.sin(0.25 * np.pi)), int(350 - 300 * np.sin(0.25 * np.pi)))
        cv2.line(self.canvas, start_point, end_point, self.white, 1)
        # 添加正北指向和距离刻度文字
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.canvas, "N", (340, 40), self.font, 1, (255, 255, 255), 1)
        cv2.putText(self.canvas, "30", (5, 360), self.font, 1, (255, 255, 255), 1)
        cv2.putText(self.canvas, "30", (650, 360), self.font, 1, (255, 255, 255), 1)
        # 添加参数指示文字
        cv2.putText(self.canvas, "Speed(m/s):", (500, 15), self.font, 0.5, (255, 255, 255), 1)
        cv2.putText(self.canvas, "Rotation:", (530, 35), self.font, 0.5, (255, 255, 255), 1)
        cv2.putText(self.canvas, "Coordinate(X):", (488, 55), self.font, 0.5, (255, 255, 255), 1)
        cv2.putText(self.canvas, "Coordinate(Y):", (488, 75), self.font, 0.5, (255, 255, 255), 1)
        # 运动目标初始值，beta飞行角度,speed速度
        self.beta = 225 / 180 * np.pi  # 飞行方位角
        self.speed = 300  # 飞行速度
        self.pointStartX = 500
        self.pointStartY = 10
        self.pointEndX = 500
        self.pintEndY = 500

        self.i = 0
        self.delteT = 1  # 目标运动的比例值

    # 定义绘制扫描辉亮函数，ang为扫描线所在角度位置
    def drawScanner(self, ang):
        img = np.zeros((700, 700, 3), np.uint8)
        a = 255 / 60  # 将颜色值255等分60，60为辉亮夹角
        for i in range(60):
            # 逐次绘制1度扇形，颜色从255到0
            cv2.ellipse(img, (350, 350), (300, 300), 1, ang - i, ang - i - 1, (255 - i * a, 255 - i * a, 255 - i * a),
                        -1)
        return img

    def get_img(self):
        self.i += 3
        self.i %= 360
        self.pointStartX += int(self.speed * self.delteT * 0.01 * np.cos(self.beta))
        self.pointStartY += -int(self.speed * self.delteT * 0.01 * np.sin(self.beta))

        cv2.circle(self.canvas, (self.pointStartX, self.pointStartY), self.point_size, self.yellow, 1)  # 目标运动轨迹点
        # 复制雷达界面，将目标运动和参数指示绘制在复制图上
        temp = np.copy(self.canvas)
        cv2.circle(temp, (self.pointStartX, self.pointStartY), self.point_size, self.red, 6)  # 目标点

        cv2.putText(temp, str(self.speed), (605, 15), self.font, 0.5, (0, 255, 0), 1)
        cv2.putText(temp, str(self.beta / np.pi * 180), (605, 35), self.font, 0.5, (0, 255, 0), 1)
        cv2.putText(temp, str(self.pointStartX), (605, 55), self.font, 0.5, (0, 255, 0), 1)
        cv2.putText(temp, str(self.pointStartY), (605, 75), self.font, 0.5, (0, 255, 0), 1)
        scanImg = self.drawScanner(self.i)  # 绘制扫描辉亮
        blend = cv2.addWeighted(temp, 1.0, scanImg, 0.6, 0.0)  # 将雷达显示与扫描辉亮混合
        frame = cv2.resize(blend, (640, 640),
                           interpolation=cv2.INTER_AREA)
        return frame


if __name__ == '__main__':
    obj = RadarScan()
    while True:
        img = obj.get_img()
        cv2.imshow('My Radar', img)
        cv2.waitKey(1)
