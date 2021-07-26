"""
解析gps数据
"""


def resolve_gps(gps_str):
    """
    :param gps_str: gps数据字符串
    :return:{'lng':114.000,'lat':30.010,'lng_lat_error':2.5,} 字典
    """
    gps_dict = {}
    if gps_str.startswith('$GNGGA') or gps_str.startswith('$GPGGA'):
        data_list = gps_str.split(',')
        if len(data_list) < 8:
            return gps_dict
        lng, lat = round(float(data_list[4][:3]) +
                         float(data_list[4][3:]) /
                         60, 6), round(float(data_list[2][:2]) +
                                       float(data_list[2][2:]) /
                                       60, 6)
        lng_lat_error = float(data_list[8])
        if lng < 1 or lat < 1:
            return gps_dict
        else:
            gps_dict.update({'lng': lng, 'lat': lat, 'lng_lat_error': lng_lat_error})
            return gps_dict