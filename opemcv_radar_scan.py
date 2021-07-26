import numpy as np
import cv2 as cv

# 生成一个700*700的空灰度图像
canvas = np.zeros((700, 700, 3), np.uint8)

point_size = 1
white = (255, 255, 255)
red = (0, 0, 255)
blue = (255, 0, 0)
yellow = (0, 255, 255)

# 绘制雷达显示器界面的同心圆
cv.circle(canvas, (350, 350), 100, white, 2)
cv.circle(canvas, (350, 350), 200, white, 2)
cv.circle(canvas, (350, 350), 300, white, 2)
# 绘制十字线
cv.line(canvas, (50, 350), (650, 350), white, 2)
cv.line(canvas, (350, 50), (350, 650), white, 2)
start_point = (int(350 - 300 * np.sin(0.25 * np.pi)), int(350 - 300 * np.sin(0.25 * np.pi)))
end_point = (int(350 + 300 * np.sin(0.25 * np.pi)), int(350 + 300 * np.sin(0.25 * np.pi)))
cv.line(canvas, start_point, end_point, white, 1)
start_point = (int(350 - 300 * np.sin(0.25 * np.pi)), int(350 + 300 * np.sin(0.25 * np.pi)))
end_point = (int(350 + 300 * np.sin(0.25 * np.pi)), int(350 - 300 * np.sin(0.25 * np.pi)))
cv.line(canvas, start_point, end_point, white, 1)
# 添加正北指向和距离刻度文字
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(canvas, "N", (340, 40), font, 1, (255, 255, 255), 1)
cv.putText(canvas, "30", (5, 360), font, 1, (255, 255, 255), 1)
cv.putText(canvas, "30", (650, 360), font, 1, (255, 255, 255), 1)
# 添加参数指示文字
cv.putText(canvas, "Speed(m/s):", (500, 15), font, 0.5, (255, 255, 255), 1)
cv.putText(canvas, "Rotation:", (530, 35), font, 0.5, (255, 255, 255), 1)
cv.putText(canvas, "Coordinate(X):", (488, 55), font, 0.5, (255, 255, 255), 1)
cv.putText(canvas, "Coordinate(Y):", (488, 75), font, 0.5, (255, 255, 255), 1)


# 定义绘制扫描辉亮函数，ang为扫描线所在角度位置
def drawScanner(ang):
    img = np.zeros((700, 700, 3), np.uint8)
    a = 255 / 60  # 将颜色值255等分60，60为辉亮夹角
    for i in range(60):
        # 逐次绘制1度扇形，颜色从255到0
        cv.ellipse(img, (350, 350), (300, 300), 1, ang - i, ang - i - 1, (255 - i * a, 255 - i * a, 255 - i * a), -1)
    return img


# 运动目标初始值，beta飞行角度,speed速度
beta = 225 / 180 * np.pi  # 飞行方位角
speed = 300  # 飞行速度
pointStartX = 500
pointStartY = 10
pointEndX = 500
pintEndY = 500

i = 0
delteT = 1  # 目标运动的比例值
while (1):
    i += 1
    pointStartX += int(speed * delteT * 0.01 * np.cos(beta))
    pointStartY += -int(speed * delteT * 0.01 * np.sin(beta))

    cv.circle(canvas, (pointStartX, pointStartY), point_size, yellow, 1)  # 目标运动轨迹点
    # 复制雷达界面，将目标运动和参数指示绘制在复制图上
    temp = np.copy(canvas)
    cv.circle(temp, (pointStartX, pointStartY), point_size, red, 6)  # 目标点

    cv.putText(temp, str(speed), (605, 15), font, 0.5, (0, 255, 0), 1)
    cv.putText(temp, str(beta / np.pi * 180), (605, 35), font, 0.5, (0, 255, 0), 1)
    cv.putText(temp, str(pointStartX), (605, 55), font, 0.5, (0, 255, 0), 1)
    cv.putText(temp, str(pointStartY), (605, 75), font, 0.5, (0, 255, 0), 1)

    scanImg = drawScanner(i)  # 绘制扫描辉亮
    blend = cv.addWeighted(temp, 1.0, scanImg, 0.6, 0.0)  # 将雷达显示与扫描辉亮混合
    cv.imshow('My Radar', blend)
    if cv.waitKey(100) == 27:  # 按下ESC键退出
        break
