#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/1 14:29
# @Version : 1.0
# @File    : mqclient.py
# @Author  : Jingsheng Tang
# @Version : 1.0
# @Contact : mrtang@nudt.edu.cn   mrtang_cs@163.com
# @License : (C) All Rights Reserved

import paho.mqtt.client as mqtt


connect_rc = {'0':'[mqtt] connect succeed!',
              '1':'[mqtt] connect failure, incorrect mqtt protocol version',
              '2':'[mqtt] connect failure, invalid client id',
              '3':'[mqtt] connect failure, broker inaccessible',
              '4':'[mqtt] connect failure, incorrect username or password',
              '5':'[mqtt] connect failure, unauthorized'}


class MqClient():
    def __init__(self,username = '', client_id = '', host = '127.0.0.1',port = 1883, sub_topic = '', keepalive = 600, loop_sync = True):
        # username:     用户名，为空时缺省
        # client_id:     客户端标识符，为空时系统自动分配
        # host:         代理的地址
        # port:            代理的端口
        # sub_topic:    订阅的主题，为空时不订阅任何主题
        # keepalive:    与代理连接的时间
        # loop_sync:    True: 以loop_start方式，启用线程来处理网络请求事件，主线程可以对发布以及订阅作进一步处理，常用
        #                False:以loop_forever方式，阻塞。
        
        self.sub_topic = sub_topic
        self.client = mqtt.Client(client_id,)
        if len(username) > 0:
            self.client.username_pw_set(username,password = None)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(host, port, keepalive)
        if loop_sync:
            self.client.loop_start()
        else:
            self.client.loop_forever()

    def on_disconnect(self,client,userdata,rc):
        self.client.loop_stop()

    def on_connect(self,client,userdata,flags,rc):
        if rc == 0 and len(self.sub_topic) > 0:
            client.subscribe(self.sub_topic)

        rc = str(rc)
        if rc in connect_rc:
            print(connect_rc[rc])
        else:
            print('[mqtt] connect failure')

    def on_message(self,client,userdata,msg):
        mg = msg.payload
        print(mg)
        return mg

    def publish(self,payload,topic,qos = 0):
        # 在要求较高的场合，注意使用on_publish回调来获取消息发送的状态
        self.client.publish(topic,payload,qos)

    def disconnect(self):
        self.client.disconnect()
        
def main():
    mq = MqClient(host = '192.168.66.2',sub_topic = 'esp32topic',loop_sync = False)


def main2():
    import time
    mqp = MqClient(host = '192.168.66.2',client_id = 'pub_0')
    for i in range(10):
        mqp.publish(str(i),'test')
        time.sleep(1)
        print(str(i))

if __name__ == '__main__':
    main()
    


