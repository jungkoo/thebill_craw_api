# -*- coding: utf-8 -*-
import logging
import requests
from selenium import webdriver
import threading

_thread_local = threading.local()


class LoginSession:
    """
    request 를 이용한 데이터 조회
    """
    def __init__(self, user_id, password):
        self._user_id = user_id
        self._password = password
        self._login_session = requests.session()
        self._header = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        self._authentication()
        self._limit = 100000
        _thread_local.login_req = self

    def _authentication(self):
        data = {'layoutCd': 'spa00', 'loginid': self._user_id, 'loginpw': self._password}
        self._login_session.get("https://www.thebill.co.kr", headers=self._header)
        r = self._login_session.post("https://www.thebill.co.kr/webuser/loginProc.json", headers=self._header, data=data)
        if r.json()['resultMsg'] != "":
            raise Exception("LOGIN ERROR")

    def post(self, url, **data):
        return self._login_session.post(url, headers=self._header, data=data)

    def result_list_generator(self, url, **data):
        res = self.post(url, **data)
        json_res = res.json()
        page_cnt = json_res['PageVO']['pageCnt']
        page_param = dict()
        page_param.update(data)

        count = 0
        for page_num in range(1, int(page_cnt)+1):
            page_param['pageno'] = page_num
            if count >= self._limit:
                break
            res = self.post(url, **page_param)
            json_res = res.json()
            for row in json_res['resultList'] or []:
                if count >= self._limit:
                    break
                count += 1
                yield dict(filter(lambda elem: elem[1] is not None, row.items()))

    def session(self):
        return self._login_session

    @staticmethod
    def current():
        try:
            val = _thread_local.login_req
        except AttributeError:
            logging.debug("current login info not found")
        else:
            return val


class BrowserLogin:
    """
    크롬 셀레니움을 이용한 수집 로그인
    """
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
