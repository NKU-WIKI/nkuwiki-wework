# -*- coding: utf-8 -*-
import sys
import ntwork

wework = ntwork.WeWork()

# 打开pc企业微信, smart: 是否管理已经登录的微信
wework.open(smart=True)

# 等待登录
wework.wait_login()

# 获取群列表并输出
rooms = wework.get_rooms()
print("群列表: ")
print(rooms)


ntwork.exit_()
sys.exit()