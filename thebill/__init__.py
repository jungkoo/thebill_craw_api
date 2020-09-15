# -*- coding: utf-8 -*-
import logging

from selenium import webdriver
import threading

_thread_local = threading.local()


class Login:
    def __init__(self, user_id, password, driver_path):
        self._user_id = user_id
        self._password = password
        self._driver_path = driver_path
        self._headless = True
        self._open_web_driver = []
        _thread_local.login = self

    def headless(self, headless=True):
        self._headless = headless
        return self

    def webdriver(self):
        option = webdriver.ChromeOptions()
        option.headless = self._headless
        option.add_argument('--lang=ko-KR')
        option.add_argument('--user-agent="Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/37.0.2049.0 Safari/537.36"')
        option.add_argument("window-size=1024x768")
        url = "https://www.thebill.co.kr/main.jsp?mobileChk=N"
        d = webdriver.Chrome(self._driver_path, chrome_options=option)
        d.implicitly_wait(3)
        d.get(url)
        d.find_element_by_css_selector("input[type='text'][name='loginid'").send_keys(self._user_id)
        d.find_element_by_css_selector("input[type='password'][name='loginpw']").send_keys(self._password)
        d.find_element_by_css_selector("input[type=\"submit\"]").click()
        self._open_web_driver.append(d)
        return d

    def close(self):
        for ow in self._open_web_driver:
            try:
                if ow:
                    ow.close()
            except Exception:
                pass

    @staticmethod
    def current():
        try:
            val = _thread_local.login
        except AttributeError:
            logging.debug("current login info not found")
        else:
            return val
