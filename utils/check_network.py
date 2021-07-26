import os, sys

sys.path.append(os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__))))
import time
from subprocess import run, PIPE
import config
import re
import subprocess


def check_network():
    r = run('ping www.baidu.com',
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            shell=True)
    if r.returncode:
        return False
    else:
        return True


def get_ping_delay():
    if config.current_platform == config.CurrentPlatform.pi:
        (status, output) = subprocess.getstatusoutput('ping -c 4 %s' % ('www.baidu.com'))
        res = re.findall('time=(.+)ms', output)
    else:
        (status, output) = subprocess.getstatusoutput('ping %s' % ('www.baidu.com'))
        res = re.findall('时间.(.+)ms', output)
    # res = re.findall('/./d+//(.+)//',output)
    res = [float(i) for i in res]
    # 判断网络状况
    if len(res) == 0:
        return 0
    else:
        return sum(res) / len(res)


if __name__ == '__main__':
    while 1:
        # start_time = time.time()
        # print("network: ", check_network())
        # 时间大概在 3.1 到20 秒
        # print('cost time:', time.time() - start_time)
        # time.sleep(config.check_network_interval)
        print(get_ping_delay())
