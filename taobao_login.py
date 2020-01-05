import re
import os
import json

import requests

"""
获取详细教程、获取代码帮助、提出意见建议
关注微信公众号「裸睡的猪」与猪哥联系

@Author  :   猪哥,
@Version :   2.0"
"""

s = requests.Session()
# cookies序列化文件
COOKIES_FILE_PATH = 'taobao_login_cookies.txt'


class TaoBaoLogin:

    def __init__(self, session):
        """
        账号登录对象
        :param username: 用户名
        :param ua: 淘宝的ua参数
        :param TPL_password2: 加密后的密码
        """
        # 检测是否需要验证码的URL
        self.user_check_url = 'https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'
        # 验证淘宝用户名密码URL
        self.verify_password_url = "https://login.taobao.com/member/login.jhtml"
        # 访问st码URL
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'
        # 淘宝个人 主页
        self.my_taobao_url = 'http://i.taobao.com/my_taobao.htm'

        # 淘宝用户名
        self.username = '15982165246'
        # 淘宝重要参数，从浏览器或抓包工具中复制，可重复使用
        self.ua = '122#XeKM3JxGEExaYJpZMEpJEJponDJE7SNEEP7rEJ+/f9t/2oQLpo7iEDpWnDEeK51HpyGZp9hBuDEEJFOPpC76EJponDJL7gNpEPXZpJRgu4Ep+FQLpoGUEJLWn4yP7SQEEyuLpERKVfvlprZCnaRx9kb/oUfeuw3iLwTi5msDfwYzOHGzRJ5LhXLw2E9q5v1JRATcIm8IPUXdmYHc2E5hqZsgr2buCH3Rx+0MqEPTji0gpMQpeBP5eGXyFH9SvqnxQ0+N0xwbKebPExpv8oL6+tue41a1ZS6g/8pxnSph1BC5Xzsm85C4JzbbyFfmqMf2ENpC3VDb5y0EDLXT8BLUJNI9UV4n7W3bD93xnSL1elWEELXZ8oL6JNEEyBfDqMAbEEpangL4ul0EDLVr8opUJ4bEyF3mqWivDEpxqMh1uO0EEL34HBWHuaIZe6pNnAyorjB7ugR81PMBMnrnHq8IFZ/LyAGDrIXh3P4v4Y/a9uEXyDEVwTUbER/sivMJCt+ZEHEyiZ5trGyvONKiU8CEjK0Zk6l10OJBBNZM1dQpzWIDr7yZ0iFekycacvI3bFK9mExYCi8xOTijzJVyaqNUisbS8MhAYRxJwzf2WAP7crgFHDV+GKl15fomNfMmyvfic/45na4bsyCk0ZVCByYxsQ0jXExo7SGpgyv32kCKarWTy+K9Vh+TyimqPyIdjeb44W2d10dvSg8H3Xp+N1XS1vnZtPfF4k7hMpBs4eyTFQUqVkYcpbJnvKCjyk+8Jd+saedFZIcEC3WVtv1A9j3LgzPmwfr+04+WLmNXdO11BAnmBTAZsFsxN0h6WoH0XanXmC2+Sx7WD9j6J1zutSBtZ3orLTyiDtLx22DJLyemhtt0MFZeXQSF0k5MgWmpVjwDOwPiWUJeSwaeLKYI8tTLwWWL7mrA4OR5PMtri9zkkmonKOHpn4ji2oEGVuc9Q2ELkTnTvhC0a7eh4/My7DR/e2Kzd9P/H65pCVpyIwtoeYswYF4kdvQq1QMrH+cE0Ie7+I8nrPtnjakXU1jL2uHBd+hbDYS9BVbZuysy9g3a1nW38HLSR91ZQclKdJwMsE8T3+HAjsiV/lazYgncy3gwQc7qSW+VcDCsRsCMIK5Au5tHGYs5mvlUit5DOkvrDXsxRK90Rf+LUPdgUJwSMdaKt/mQjHKJwVUuEU6yIBMDWdE8t0mWMeiyZjvieHcLWdW/S66lsS4VMANnLAEzbNwlbBX++y2cjPYOH0NtRAxgE21BsDQuQG0lbM+UcRRX3qYMnrPKh+QV9hkAZbsvNzz0+dbKonfMtQ2tPvWWmuKr4jhUxzF1GAX+ychmPIF0HNtfNdx4BFgi8X7ZbpZdAo5CinHpsMvOHZwaPEu872v/pdcw6bVTznQXxIpCEcgnWZ08sij4kCVJPn69y9qO0gpvi3y8xIlMGKKbCo9Z9Jt4NF0pIR5whgSaEMs6Xqy5vfafZYn56Fcppy1HMwDsM34SdinF0e6QuzjSRj/OdtRjls16ve18bEaxbqs+9aSVrTZ7ShXrU9d/txM8anFA1qiPvtjxF6wGZjr5l1egTz+rdga1E0iyVG9CxiM+8I2q1lyb9zh7nDltmZu2EfTxEW3ciUiFg7QPAUwFBteCxuMkHOY0LTXc8pbrBoexVVThmiwdwtfI3fQ='
        # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
        self.TPL_password2 = '21f04ba83158f2147c348dd175eea906f39abcc745dee9276ec340de60df7cb662eebd473e9d5883ad14f30c693443ff65eede052a5deb7d2fd64b18a9e3f450c2e5aadeb8fb7c74f44afb909a74ed819573cb9371c2947f859d2912185f05f4db0a439bde3ea16e5f0d80dd24d1a95e46b5ba50ac5b7b45774f3b279519ae52'

        # 请求超时时间
        self.timeout = 3
        # session对象，用于共享cookies
        self.session = session

        if not self.username:
            raise RuntimeError('草根也会胖')

    def _user_check(self):
        """
        检测账号是否需要验证码
        :return:
        """
        data = {
            'username': self.username,
            'ua': self.ua
        }
        try:
            response = self.session.post(self.user_check_url, data=data, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print('检测是否需要验证码请求失败，原因：')
            raise e
        needcode = response.json()['needcode']
        print('是否需要滑块验证：{}'.format(needcode))
        return needcode

    def _verify_password(self):
        """
        验证用户名密码，并获取st码申请URL
        :return: 验证成功返回st码申请地址
        """
        verify_password_headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://login.taobao.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://login.taobao.com/member/login.jhtml?from=taobaoindex&f=top&style=&sub=true&redirect_url=https%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm',
        }
        # 登录toabao.com提交的数据，如果登录失败，可以从浏览器复制你的form data
        verify_password_data = {
            'TPL_username': self.username,
            'ncoToken': '582097d88cc5e8858630ce0632a443a7730a20e8',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'https://s.taobao.com/search?q=%E6%83%85%E8%B6%A3%E5%86%85%E8%A1%A3&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200104&ie=utf8&bcoffset=4&p4ppushleft=1%2C48&ntoffset=4&s=88',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            # 'gvfdcre': '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61323330722E312E3735343839343433372E372E33353836363032633279704A767526663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246732E74616F62616F2E636F6D25324673656172636825334671253344253235453925323538302532353946253235453525323542412532354136253235453925323538302532353946253235453525323542412532354136253236696D6766696C65253344253236636F6D6D656E64253344616C6C2532367373696425334473352D652532367365617263685F747970652533446974656D253236736F75726365496425334474622E696E64657825323673706D253344613231626F2E323031372E3230313835362D74616F62616F2D6974656D2E31253236696525334475746638253236696E69746961746976655F69642533447462696E6465787A5F3230313730333036',
            'TPL_password_2': self.TPL_password2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'oslanguage': 'zh-CN',
            'sr': '1440*900',
            'osVer': 'macos|10.145',
            'naviVer': 'chrome|76.038091',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'osPF': 'MacIntel',
            'appkey': '00000000',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?spm=a230r.1.754894437.1.252532d27cmYcy&f=top&redirectURL=https://s.taobao.com/search?q=%E6%83%85%E8%B6%A3%E5%86%85%E8%A1%A3&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200104&ie=utf8&bcoffset=4&p4ppushleft=1%2C48&ntoffset=4&s=88&useMobile=true',
            'showAssistantLink': '',
            'um_token': 'TE0E58D37A2B663A64F5754CCF8979495C65B8F0DB959B5528F7778718A',
            'ua': self.ua
        }
        try:
            response = self.session.post(self.verify_password_url, headers=verify_password_headers, data=verify_password_data,
                              timeout=self.timeout)
            response.raise_for_status()
            # 从返回的页面中提取申请st码地址
        except Exception as e:
            print('验证用户名和密码请求失败，原因：')
            raise e
        # 提取申请st码url
        apply_st_url_match = re.search(r'<script src="(.*?)"></script>', response.text)
        # 存在则返回
        if apply_st_url_match:
            print('验证用户名密码成功，st码申请地址：{}'.format(apply_st_url_match.group(1)))
            return apply_st_url_match.group(1)
        else:
            raise RuntimeError('用户名密码验证失败！response：{}'.format(response.text))

    def _apply_st(self):
        """
        申请st码
        :return: st码
        """
        apply_st_url = self._verify_password()
        try:
            response = self.session.get(apply_st_url)
            response.raise_for_status()
        except Exception as e:
            print('申请st码请求失败，原因：')
            raise e
        st_match = re.search(r'"data":{"st":"(.*?)"}', response.text)
        if st_match:
            print('获取st码成功，st码：{}'.format(st_match.group(1)))
            return st_match.group(1)
        else:
            raise RuntimeError('获取st码失败！response：{}'.format(response.text))

    def login(self):
        """
        使用st码登录
        :return:
        """
        # 加载cookies文件
        if self._load_cookies():
            return True
        # 判断是否需要滑块验证
        self._user_check()
        st = self._apply_st()
        headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = self.session.get(self.vst_url.format(st), headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('st码登录请求，原因：')
            raise e
        # 登录成功，提取跳转淘宝用户主页url
        my_taobao_match = re.search(r'top.location.href = "(.*?)"', response.text)
        if my_taobao_match:
            print('登录淘宝成功，跳转链接：{}'.format(my_taobao_match.group(1)))
            self._serialization_cookies()
            return True
        else:
            raise RuntimeError('登录失败！response：{}'.format(response.text))

    def _load_cookies(self):
        # 1、判断cookies序列化文件是否存在
        if not os.path.exists(COOKIES_FILE_PATH):
            return False
        # 2、加载cookies
        self.session.cookies = self._deserialization_cookies()
        # 3、判断cookies是否过期
        try:
            self.get_taobao_nick_name()
        except Exception as e:
            os.remove(COOKIES_FILE_PATH)
            print('cookies过期，删除cookies文件！')
            return False
        print('加载淘宝登录cookies成功!!!')
        return True

    def _serialization_cookies(self):
        """
        序列化cookies
        :return:
        """
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        with open(COOKIES_FILE_PATH, 'w+', encoding='utf-8') as file:
            json.dump(cookies_dict, file)
            print('保存cookies文件成功！')

    def _deserialization_cookies(self):
        """
        反序列化cookies
        :return:
        """
        with open(COOKIES_FILE_PATH, 'r+', encoding='utf-8') as file:
            cookies_dict = json.load(file)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            return cookies

    def get_taobao_nick_name(self):
        """
        获取淘宝昵称
        :return: 淘宝昵称
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = self.session.get(self.my_taobao_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('获取淘宝主页请求失败！原因：')
            raise e
        # 提取淘宝昵称
        nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if nick_name_match:
            print('登录淘宝成功，你的用户名是：{}'.format(nick_name_match.group(1)))
            return nick_name_match.group(1)
        else:
            raise RuntimeError('获取淘宝昵称失败！response：{}'.format(response.text))


if __name__ == '__main__':
    ul = TaoBaoLogin(s)
    ul.login()
    ul.get_taobao_nick_name()