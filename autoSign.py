# -*- coding: utf-8 -*-
'''
* Project: autoSign
* Author ：Original
* Environment: Python3.8.6
* Blog: https://blog.899988.xyz
* Web: https://www.899988.xyz
* Date: 2021-01-12 10:42:37
'''

import requests
from bs4 import BeautifulSoup
import threading


class chunyuAutoSign:
    API = {
        'login': 'https://www.chunyuyisheng.com/ssl/api/weblogin/?next=/',
        'sign': 'https://api.chunyuyisheng.com/api/gold/task/local/finish?name=USE_CHUNYU&version=8.3.4',
    }

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
        'Referer': API['login']
    }

    def start(self, userList):
        for user in userList:
            self.session = requests.session()
            self.session.headers.update(self.header)
            self._startSign(user['userName'], user['userPwd'])

    def _startSign(self, userName, userPwd):
        csrfToken = self._getCsrfToken()
        self._login(userName, userPwd, csrfToken)
        self._sign(userName)

    def _getCsrfToken(self):
        req = self.session.get(self.API['login'])
        soup = BeautifulSoup(req.text, 'lxml')
        return soup.find('input', {'name': ['csrfmiddlewaretoken']})['value']

    def _login(self, userName, userPwd, csrfToken):
        data = {
            'csrfmiddlewaretoken': csrfToken,
            'next': '/',
            'username': userName,
            'password': userPwd
        }
        self.session.post(self.API['login'], data)

    def _sign(self, userName):
        req = self.session.get(self.API['sign'])
        print(req.text)
        res = req.json()
        coins = res['coins_num']

        if res['gold_task']:
            tmp = f'{userName}，签到成功，当前金币[{coins}]'
        else:
            tmp = f'{userName}，无需重复签到，当前金币[{coins}]'
        
        print(tmp)


def main():
    users = [
        {
            'userName': '用户名',
            'userPwd': '密码'
        },
    ]

    chunyu = chunyuAutoSign()
    chunyu.start(users)


if __name__ == '__main__':
    main()
