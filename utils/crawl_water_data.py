import requests
import json
import re
import enum
import config

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
link = 'http://106.37.208.243:8068/GJZ/Business/Publish/RealDatas.html'
referer = "Referer: " + link
headers = {"Referer": referer,
           "User-Agent": user_agent,
           "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
           "Accept": "application/json, text/javascript, */*; q=0.01"}


class CrawlWaterData:
    """
    抓取水质数据
    """
    def __init__(self):
        self.base_url = 'http://106.37.208.243:8068/GJZ/Ajax/Publish.ashx?PageIndex=1&PageSize=60&action=getRealDatas&AreaID='

    def get_data_dict(self, area_id=None):
        """
        获取目标市的水质数据，area_id为市的行政编码
        :param area_id: 默认值None 若不传则使用武汉市编码
        :return:
        """
        return_data_dict = {}
        if area_id is None or not isinstance(area_id, int) or area_id > 999999 or area_id > 100000:
            area_id = 420100
            # area_id = 420000
        url = self.base_url + str(area_id)
        print('请求水质数据')
        html = requests.post(url, headers=headers)
        json_data = json.loads(html.content)
        if json_data.get('tbody'):
            return_data_dict.update({'省份': json_data.get('tbody')[0][0]})
            return_data_dict.update({'流域': json_data.get('tbody')[0][1]})
            city = re.findall(':(..市)', json_data.get('tbody')[0][2])[0]
            return_data_dict.update({'所属市': city})
        wt_list = []
        pH_list = []
        DO_list = []
        EC_list = []
        TD_list = []
        NH3NH4_list = []
        count = 0
        for data_list in json_data.get('tbody'):
            count += 1
            if len(re.findall('>(.*)<', data_list[5]))>0:
                wt = float(re.findall('>(.*)<', data_list[5])[0])
                wt_list.append(wt)
            if len(re.findall('>(.*)<', data_list[6])) > 0:
                pH = float(re.findall('>(.*)<', data_list[6])[0])
                pH_list.append(pH)
            if len(re.findall('>(.*)<', data_list[7])) > 0:
                DO = float(re.findall('>(.*)<', data_list[7])[0])
                DO_list.append(DO)
            if len(re.findall('>(.*)<', data_list[8])) > 0:
                EC = float(re.findall('>(.*)<', data_list[8])[0])
                EC_list.append(EC)
            if len(re.findall('>(.*)<', data_list[9])) > 0:
                TD = float(re.findall('>(.*)<', data_list[9])[0])
                TD_list.append(TD)
            if len(re.findall('>(.*)<', data_list[11])) > 0:
                NH3NH4 = float(re.findall('>(.*)<', data_list[11])[0])
                NH3NH4_list.append(NH3NH4)

        return_data_dict.update({config.WaterType.wt: wt_list})
        return_data_dict.update({config.WaterType.pH: pH_list})
        return_data_dict.update({config.WaterType.DO: DO_list})
        return_data_dict.update({config.WaterType.EC: EC_list})
        return_data_dict.update({config.WaterType.TD: TD_list})
        return_data_dict.update({config.WaterType.NH3_NH4: NH3NH4_list})
        return return_data_dict


if __name__ == '__main__':
    obj = CrawlWaterData()
    data_dict = obj.get_data_dict()
    print(data_dict)
