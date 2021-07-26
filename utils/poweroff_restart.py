from os import system
# 重启电脑
def restart():
    system('sudo reboot')

def poweroff():
    system('sudo shutdown now')

