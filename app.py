import sys
import ntwork
import getConversationId
import sendMessages

wework = ntwork.WeWork()
# 打开pc企业微信, smart: 是否管理已经登录的微信
wework.open(smart=True)

# 等待登录
wework.wait_login()

getId = getConversationId.GetConversationId(5, wework)

sendMsg = sendMessages.SendMessages("localhost", "root", "******", "database", "'2025-07-07 00:00:00'", getId.getId("test"), wework)

sendMsg.sendMessage()

ntwork.exit_()
sys.exit()