# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import glob

import wechat
import json
import time
from wechat import WeChatManager, MessageType

wechat_manager = WeChatManager(libs_path='../../libs')

imgs = []

# 这里测试函数回调
@wechat.CONNECT_CALLBACK(in_class=False)
def on_connect(client_id):
    print('[on_connect] client_id: {0}'.format(client_id))


@wechat.RECV_CALLBACK(in_class=False)
def on_recv(client_id, message_type, message_data):
    print('[on_recv] client_id: {0}, message_type: {1}, message:{2}'.format(client_id,
                                                                            message_type, message_data))

    # 如果发送文本信息 且 发送对象是文本传输助手
    # if message_type == MessageType.MT_RECV_TEXT_MSG and message_data['to_wxid'] == "filehelper":
    #
    #     # 本地图片库中搜索图片
    #     img_text = message_data['msg']
    #     for name in glob.glob(r'E:\workspace\python\tran\emoji\*'+img_text+'*.jpg'):
    #         imgs.append(name)
    #         print("找到图片："+name)
    #     for img in imgs[:6]:
    #         wechat_manager.send_image(client_id, message_data['to_wxid'], img)
    #         time.sleep(0.3)
    #         print('开始发送表情： ', img)
    #     imgs.clear()

    if message_type == MessageType.MT_RECV_TEXT_MSG and message_data['to_wxid'] == "wxid_ocjpv4fvhm8122":

        # 本地图片库中搜索图片
        img_text = message_data['msg']
        for name in glob.glob(r'E:\workspace\python\tran\emoji\*'+img_text+'*.jpg'):
            imgs.append(name)
            print("找到图片："+name)
        for img in imgs[:6]:
            wechat_manager.send_image(client_id, message_data['from_wxid'], img)
            time.sleep(0.3)
            print('开始发送表情： ', img)
        imgs.clear()


@wechat.CLOSE_CALLBACK(in_class=False)
def on_close(client_id):
    print('[on_close] client_id: {0}'.format(client_id))


# 这里测试类回调， 函数回调与类回调可以混合使用
class LoginTipBot(wechat.CallbackHandler):

    @wechat.RECV_CALLBACK(in_class=True)
    def on_message(self, client_id, message_type, message_data):
        # 判断登录成功后，就向文件助手发条消息
        if message_type == MessageType.MT_USER_LOGIN:
            time.sleep(2)
            wechat_manager.send_text(client_id, 'filehelper', '😂😂😂\uE052该消息通过wechat_pc_api项目接口发送')

            wechat_manager.send_link(client_id,
            'filehelper',
            'wechat_pc_api项目',
            'WeChatPc机器人项目',
            'https://github.com/smallevilbeast/wechat_pc_api',
            'https://www.showdoc.com.cn/server/api/attachment/visitfile/sign/0203e82433363e5ff9c6aa88aa9f1bbe?showdoc=.jpg)')


if __name__ == "__main__":
    bot = LoginTipBot()

    # 添加回调实例对象
    wechat_manager.add_callback_handler(bot)
    wechat_manager.manager_wechat(smart=True)

    # 阻塞主线程
    while True:
        time.sleep(0.5)