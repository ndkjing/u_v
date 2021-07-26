"""
生成随机数据
"""

"""
from uuid import uuid4
import random
import copy
import time


# 生成船号
def get_ship_code():
    return str(uuid4())

# 剩余电量
def get_dump_energy():
    return init_dump_energy - round((time.time() - init_time)/60, 1)

# 当前经纬度
def get_current_lng_lat(init_lng_lat):
    if random.random()>0.5:
        init_lng_lat = [init_lng_lat[0] - round(random.random(), 1)/1000,init_lng_lat[1]]
    else:
        init_lng_lat = [init_lng_lat[0],init_lng_lat[1] - round(random.random(),1)/1000]

    return init_lng_lat


# 船号
ship_code = '3c50f4c3-a9c1-4872-9f18-883af014380b'
if ship_code == None:
    ship_code = get_ship_code()

# 湖号
pool_code = None
# 电量
init_dump_energy=100
# 初始时间
init_time = time.time()
# 经纬度
init_lng_lat = [114.39458,30.547412]



init_ststus_data={"dump_energy": 0.000,
                   "current_lng_lat": [100.155214,36.993676],
                   "liquid_level": 0.000,
                   "b_leakage": False,
                   "direction": 90.0,
                   "speed": 0.000,
                   "attitude_angle": [0,0,90.0],
                   "b_online": True,
                   "b_homing": False,
                   "charge_energy": 0.000,
                   "sampling_depth": 0.000,
                   "ship_code": ship_code,
                   "pool_code":pool_code,
                   "data_flow": 0.000,
                   "sampling_count": 0,
                   "capicity": 0.00
                   }

init_detect_data={
    "water_quality_data":{"pH": 0.000,
                       "DO": 0.000,
                       "COD": 0.000,
                       "EC": 0.000,
                       "TD": 0.000,
                       "NH3_NH4": 0.000,
                       "TN": 0.000,
                       "TP": 0.000,
                       },
    "meteorological_data":{"wind_speed": 0.000,
                       "wind_direction": "",
                       "rainfall": 0.000,
                       "illuminance": 0.000,
                       "temperature": 0.000,
                       "humidity": 0.000,
                       "pm25": 0.000,
                       "pm10": 0.000,
                       }
}
#
# 风向定义['东北','正北','西北','正西','西南','正南','东南','正东']
wind_direction=['315','0','45','90','135','180','225','270']


# 返回状态数据
def status_data():
    return_dict = copy.deepcopy(init_ststus_data)
    return_dict.update({'dump_energy':get_dump_energy()})
    return_dict.update({'current_lng_lat':get_current_lng_lat(init_lng_lat)})
    return_dict.update({'sampling_depth':round(random.random(),2)})

    return_dict.update({"deviceId": ship_code})
    return return_dict

def detect_data():
    init_detect_data["weather"].update({"wind_speed":round(random.random(),2)*10})
    init_detect_data["weather"].update({"wind_direction":wind_direction[random.randint(0,len(wind_direction)-1)]})
    init_detect_data["weather"].update({"rainfall":round(random.random(),2)*10})
    init_detect_data["weather"].update({"illuminance":round(random.random(),2)*10})
    init_detect_data["weather"].update({"temperature":random.randint(0,40)})
    init_detect_data["weather"].update({"humidity":random.randint(40,90)})
    init_detect_data["weather"].update({"pm25":random.randint(0,20)})
    init_detect_data["weather"].update({"pm10":random.randint(20,40)})

    init_detect_data["water"].update({"pH":random.randint(50,90)/10.0})
    init_detect_data["water"].update({"DO":random.randint(20,100)/10.0})
    init_detect_data["water"].update({"COD":random.randint(50,400)/10.0})
    init_detect_data["water"].update({"TD":random.randint(1,10)/10.0})
    init_detect_data["water"].update({"NH3_NH4":random.randint(2,100)/100.0})
    init_detect_data["water"].update({"TN":random.randint(10,200)/10.0})
    init_detect_data["water"].update({"TP":random.randint(0,2)/10.0})
    init_detect_data["water"].update({"EC":random.randint(480,600)/10.0})

    init_detect_data.update({"deviceId":ship_code})


    return init_detect_data

# if __name__ == '__main__':
#     print(ship_code)
#     while 1:
#         print(status_data())
#         print(detect_data())
#         time.sleep(2)

"""