import numpy as np
import enum
import os
import config
from storage import save_data
from utils import crawl_water_data
import time
import copy

"""
110000	北京市
120000	天津市
130000	河北省
140000	山西省
150000	内蒙古自治区
210000	辽宁省
220000	吉林省
230000	黑龙江省
310000	上海市
320000	江苏省
330000	浙江省
340000	安徽省
350000	福建省
360000	江西省
370000	山东省
410000	河南省
420000	湖北省
430000	湖南省
440000	广东省
450000	广西壮族自治区
460000	海南省
500000	重庆市
510000	四川省
520000	贵州省
530000	云南省
540000	西藏自治区
610000	陕西省
620000	甘肃省
630000	青海省
640000	宁夏回族自治区
650000	新疆维吾尔自治区
710000	台湾省
810000	香港特别行政区
820000	澳门特别行政区
"""
area_id_dict = {110000:'北京市',
        120000:'天津市',
        130000:'河北省',
        140000:'山西省',
        150000:'内蒙古自治区',
        210000:'辽宁省',
        220000:'吉林省',
        230000:'黑龙江省',
        310000:'上海市',
        320000:'江苏省',
        330000:'浙江省',
        340000:'安徽省',
        350000:'福建省',
        360000:'江西省',
        370000:'山东省',
        410000:'河南省',
        420000:'湖北省',
        430000:'湖南省',
        440000:'广东省',
        450000:'广西壮族自治区',
        460000:'海南省',
        500000:'重庆市',
        510000:'四川省',
        520000:'贵州省',
        530000:'云南省',
        540000:'西藏自治区',
        610000:'陕西省',
        620000:'甘肃省',
        630000:'青海省',
        640000:'宁夏回族自治区',
        650000:'新疆维吾尔自治区',
        710000:'台湾省',
        810000:'香港特别行政区',
        820000:'澳门特别行政区'}

min_max_wt = (0, 35)
wt = [
    29.8,
    32.5,
    30.4,
    29.8,
    30.8,
    30.5,
    27.4,
    26.6,
    31.8,
    29.6,
    30.7,
    29.5,
    30.0,
    30.4,
    31.1,
    30.5,
    26.8
]
min_max_EC = (140, 468)
EC = [
    465.7,
    183.9,
    141.7,
    176.4,
    205.1,
    156.1,
    298.8,
    292.3,
    212.4,
    194.1,
    273.6,
    147.4,
    172.9,
    514.3,
    468.0,
    403.3,
    273.1
]

min_max_pH = (6, 9)
pH = [7.23,
      8.25,
      8.18,
      8.29,
      8.30,
      8.58,
      7.76,
      6.20,
      7.18,
      7.53,
      8.01,
      7.40,
      7.39,
      6.73,
      7.28,
      6.99,
      7.69]

min_max_DO = (2, 7.5)
DO = [
    3.28,
    12.39,
    8.14,
    7.49,
    8.20,
    7.77,
    7.49,
    6.57,
    7.35,
    7.88,
    9.02,
    6.40,
    7.93,
    2.16,
    3.04,
    2.91,
    6.85
]
min_max_TD = (2.5, 50)
TD = [
    44.2,
    34.0,
    9.4,
    2.8,
    13.0,
    7.3,
    9.1,
    29.6,
    16.1,
    26.7,
    23.4,
    27.2,
    12.1,
    32.4,
    180.0,
    30.9,
    23.4
]
min_max_NH3_NH4 = (0.15, 2.0)
NH3_NH4 = [
    0.170,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
    0.056,
    0.025,
    0.233,
    0.212,
    0.063,
    0.130,
    0.144,
    0.660,
    0.025,
    0.226,
    0.130
]

water_data_dict = {}
water_data_dict.update(
    {config.WaterType.wt: {'min_data': min_max_wt[0], 'max_data': min_max_wt[1], 'data': wt, 'keep_valid_decimals': 1}})
water_data_dict.update(
    {config.WaterType.pH: {'min_data': min_max_pH[0], 'max_data': min_max_pH[1], 'data': pH, 'keep_valid_decimals': 2}})
water_data_dict.update(
    {config.WaterType.EC: {'min_data': min_max_EC[0], 'max_data': min_max_EC[1], 'data': EC, 'keep_valid_decimals': 1}})
water_data_dict.update(
    {config.WaterType.DO: {'min_data': min_max_DO[0], 'max_data': min_max_DO[1], 'data': DO, 'keep_valid_decimals': 2}})
water_data_dict.update(
    {config.WaterType.TD: {'min_data': min_max_TD[0], 'max_data': min_max_TD[1], 'data': TD, 'keep_valid_decimals': 1}})
water_data_dict.update(
    {config.WaterType.NH3_NH4: {'min_data': min_max_NH3_NH4[0], 'max_data': min_max_NH3_NH4[1], 'data': NH3_NH4,
                                'keep_valid_decimals': 3}})

def adcode_2_area_id(adcode):
    area_id = int(str(adcode)[:2])*10000
    if area_id in area_id_dict:
        return area_id
    else:
        return 420000

def update_enum_type(data_dict,b_map_inv=True):
    water_map_dict = {config.WaterType.wt : 0,
                      config.WaterType.EC: 1,
                      config.WaterType.pH: 2,
                      config.WaterType.DO: 3,
                      config.WaterType.TD: 4,
                      config.WaterType.NH3_NH4: 5,
                }
    inv_water_map_dict = {str(v):k for k,v in water_map_dict.items()}
    return_data_dict = {}
    for i in data_dict.copy():
        if b_map_inv:
            if i in water_map_dict:
                return_data_dict.update({water_map_dict[i]: data_dict[i]})
            else:
                return_data_dict.update({i:data_dict[i]})
        else:
            if i in inv_water_map_dict:
                return_data_dict.update({inv_water_map_dict[i]: data_dict[i]})
            else:
                return_data_dict.update({i:data_dict[i]})
    return return_data_dict


def run_crawl_water_data(area_id=None):
    water_crawl_obj = crawl_water_data.CrawlWaterData()
    data_dict = water_crawl_obj.get_data_dict(area_id=area_id)
    str_date = time.strftime("%Y_%m_%d", time.localtime())
    if data_dict:
        save_data_dict = copy.deepcopy(data_dict)
        save_data_dict = update_enum_type(save_data_dict)
        save_data_dict.update({'save_date': str_date})
        save_data.set_data(save_data_dict, config.save_water_data_path)
        return data_dict
    else:
        return water_data_dict


def get_current_water_data(area_id=None):
    # 如果本地存在且时间为当天则不再重新抓取数据
    str_date = time.strftime("%Y_%m_%d", time.localtime())
    if os.path.exists(config.save_water_data_path):
        save_water_data = save_data.get_data(config.save_water_data_path)
        if save_water_data and save_water_data.get('save_date') and save_water_data.get('save_date')[-2:] == str_date[
                                                                                                             -2:]:
            data_dict = update_enum_type(save_water_data, b_map_inv=False)
        else:
            data_dict = run_crawl_water_data(area_id=area_id)
    else:
        data_dict = run_crawl_water_data(area_id=area_id)
    print('data_dict', data_dict)
    if isinstance(data_dict, dict):
        water_data_dict.update({config.WaterType.wt: {'min_data': min(data_dict[config.WaterType.wt]),
                                                      'max_data': max(data_dict[config.WaterType.wt]),
                                                      'data': data_dict[config.WaterType.wt],
                                                      'keep_valid_decimals': 1}})
        water_data_dict.update({config.WaterType.pH: {'min_data': min(data_dict[config.WaterType.pH]),
                                                      'max_data': max(data_dict[config.WaterType.pH]),
                                                      'data': data_dict[config.WaterType.pH],
                                                      'keep_valid_decimals': 2}})
        water_data_dict.update({config.WaterType.EC: {'min_data': min(data_dict[config.WaterType.EC]),
                                                      'max_data': max(data_dict[config.WaterType.EC]),
                                                      'data': data_dict[config.WaterType.EC],
                                                      'keep_valid_decimals': 1}})
        water_data_dict.update({config.WaterType.DO: {'min_data': min(data_dict[config.WaterType.DO]),
                                                      'max_data': max(data_dict[config.WaterType.DO]),
                                                      'data': data_dict[config.WaterType.DO],
                                                      'keep_valid_decimals': 2}})
        water_data_dict.update({config.WaterType.TD: {'min_data': min(data_dict[config.WaterType.TD]),
                                                      'max_data': max(data_dict[config.WaterType.TD]),
                                                      'data': data_dict[config.WaterType.TD],
                                                      'keep_valid_decimals': 1}})
        water_data_dict.update(
            {config.WaterType.NH3_NH4: {'min_data': min(data_dict[config.WaterType.NH3_NH4]),
                                        'max_data': max(data_dict[config.WaterType.NH3_NH4]),
                                        'data': data_dict[config.WaterType.NH3_NH4],
                                        'keep_valid_decimals': 3}})


def get_water_data(water_type, count=1, keep_valid_decimals=None):
    """
    返回该类型数据的最近统计数据的高斯分布数据
    :param water_type:水质数据类型
    :param count: 数量
    :param keep_valid_decimals 保留有效位数，如果不手动输入则按照默认值
    :return: 返回样式[30.648319731147538, 42.35755219891315]
    """
    # 求均值
    arr_mean = np.nanmean(water_data_dict[water_type]['data'])
    # 求方差
    arr_var = np.nanvar(water_data_dict[water_type]['data'])
    return_list = []
    for i in range(count):
        # d = np.random.normal(arr_mean, arr_var, 1)[0]  # 依据指定的均值和协方差生成数据
        # d = round(d,water_data_dict[water_type]['keep_valid_decimals'])
        d = -1000
        while d < water_data_dict[water_type]['min_data'] or d > water_data_dict[water_type]['max_data']:
            d = np.random.normal(arr_mean, arr_var, 1)[0]  # 依据指定的均值和协方差生成数据
            if keep_valid_decimals:
                d = round(d, keep_valid_decimals)
            else:
                d = round(d, water_data_dict[water_type]['keep_valid_decimals'])
        return_list.append(d)
    return return_list


def valid_water_data(water_type, data, keep_valid_decimals=None):
    """
    验证数据是否是合法值
    :param water_type: 水质数据类型
    :param data: 数据，浮点数
    :param keep_valid_decimals: 保留有效小数位数
    :return: 如果数据符合要求则返回原始数据，如果不符合要求范围则生成该数据
    """
    if water_data_dict[water_type]['min_data'] < data < water_data_dict[water_type]['max_data']:
        return data
    else:
        # 求均值
        arr_mean = np.nanmean(water_data_dict[water_type]['data'])
        # 求方差
        arr_var = np.nanvar(water_data_dict[water_type]['data'])
        d = -1000
        while d < water_data_dict[water_type]['min_data'] or d > water_data_dict[water_type]['max_data']:
            d = np.random.normal(arr_mean, arr_var, 1)[0]  # 依据指定的均值和协方差生成数据
            if keep_valid_decimals:
                d = round(d, keep_valid_decimals)
            else:
                d = round(d, water_data_dict[water_type]['keep_valid_decimals'])
        return d


if __name__ == '__main__':
    get_current_water_data()
    for i in config.WaterType:
        print(i)
        data = get_water_data(water_type=i, count=5)
        print(data)
        print(valid_water_data(i, -10))
