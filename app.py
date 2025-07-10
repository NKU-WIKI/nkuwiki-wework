import sys
import ntwork
import getConversationId
import sendMessages
from time import sleep

try:
    wework = ntwork.WeWork()
    # 打开pc企业微信, smart: 是否管理已经登录的微信
    wework.open(smart=True)

    # 等待登录
    wework.wait_login()

    getId = getConversationId.GetConversationId(5, wework)

    create_time = "'2025-07-07 00:00:00'"

    while True:
        sendMsg = sendMessages.SendMessages("localhost", "root", "******", "database", create_time, getId.getId("room"), wework)

        create_time = sendMsg.sendMessage()

        sleep(5)
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()