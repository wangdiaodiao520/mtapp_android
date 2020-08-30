#!/usr/bin/env python
# -*- coding:utf-8 -*-


import re
import requests
import time


class NewYiMa:

    """"
    36113 美团注册 【美团网】881888（登录验证码）。

    """

    # '930f9adeb51b0cc4e6beee9dc0bc142e'
    def __init__(self, name='xuejie', password='wenwen000', itemid='36113'):

        self.domain_name = 'http://203.195.147.231:8000/api/'

        self.name = name
        self.password = password
        self.itemid = itemid

        self.token = '930f9adeb51b0cc4e6beee9dc0bc142e'

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }
        self.login_in()
        print(self.token)

    def requests(self, url):
        try:
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                # print(res.content.decode())
                # return res.text
                return res.content.decode()
        except Exception as err:
            print('WangMa_requests', err)
        return None

    def login_in(self):

        try:
            url = self.domain_name + 'sign/username=%s&password=%s' % (self.name, self.password)
            content = self.requests(url)
            print(content)
            if content is not None:
                if content[0] == '1':
                    self.token = content.split('|')[1]
                else:
                    print(content)
                    return None
        except Exception as err:
            print('loginin', err)
            pass

        return None

    def get_phone(self):

        # card=1 获取指定类型的号码，0:随机，1:虚拟号段，2:正常号段。(默认值0)
        # url = self.domain_name + 'GetPhone/?id=%s&token=%s&card=1&loop=1' % (self.itemid, self.token)
        url = self.domain_name + 'yh_qh/id=%s&operator=0&Region=0&card=0&phone=&loop=1&token=%s' % (self.itemid, self.token)

        while True:
            content = self.requests(url)
            # print(content)
            if content is not None:
                if content[0] == '1':
                    return content[2:]
                else:
                    print(content)
                    if '余额不足' in content:
                        time.sleep(100)

            time.sleep(4)

    def get_code(self, phone):

        get_code_wait_all = 0
        get_code_wait = 5
        url = self.domain_name + 'yh_qm/id=%s&phone=%s&t=%s&token=%s' % (self.itemid, phone, self.name, self.token)
        # print(url)

        while True:
            try:
                content = self.requests(url)
                print(content)
                if content is not None:
                    if content[0] == '1':
                        code = re.findall('】(.*?)（', content)
                        return code[0] if len(code) else None
                    else:
                        # print(content)
                        if '余额不足' in content:
                            return None

            except Exception as err:
                print(err)

            get_code_wait_all += get_code_wait
            if get_code_wait_all >= 60:
                return None
            time.sleep(get_code_wait)

    def addblack(self, phone):
        try:
            url = self.domain_name + 'yh_lh/id=%s&phone=%s&token=%s' % (self.itemid, phone, self.token)
            res = requests.get(url, headers=self.headers)
            # print(res.text)
        except Exception as err:
            print(err)

    def release(self, phone):
        try:
            url = self.domain_name + 'yh_sf/id=%s&phone=%s&token=%s' % (self.itemid, phone, self.token)
            res = requests.get(url, headers=self.headers)
            # print(res.text)
        except Exception as err:
            print(err)


def new_yima_test():

    new_yima = NewYiMa()

    #phone = new_yima.get_phone()
    #print(phone)

    # phone = '17030030609'
    # code = new_yima.get_code(phone)
    # print(code)

    # code = new_yima.addblack(phone)
    code = new_yima.release('16572959475')



if __name__ == '__main__':
    #new_yima_test()
    pass



