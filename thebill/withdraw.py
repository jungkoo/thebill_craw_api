# -*- coding: utf-8 -*-
from collections import namedtuple
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from thebill import Login

WithDrawResult = namedtuple('WithDrawResult', 'date user_id user_name phone4 status')


class WithDraw:
    def __init__(self):
        self._login: Login = Login.current()
        self._current_driver = self._login.webdriver()  # login 한 브라우저창을 재활용한다.
        self._sub_menu_code = ""
        self._load_page()
        self._goto_sub_menu("CMS5010")
        self._set_display_size(100)

    def _load_page(self):
        """
        자동 이체 메뉴로 이동
        :return:
        """
        d = self._current_driver
        menu = d.find_element_by_css_selector("div.menu_top td:nth-child(2) > a")  # 자동이체
        menu.click()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        l: Login = Login.current()
        l.close()

    def _get_value(self, attr_name):
        d = self._current_driver
        obj = d.find_element_by_name(attr_name)
        val = obj.get_attribute("value")
        return val

    def _set_value(self, attr_name, value):
        d = self._current_driver
        obj = d.find_element_by_name(attr_name)
        obj.clear()
        obj.send_keys(value)

    def get_start_date(self):
        return self._get_value("startDate")

    def set_start_date(self, value):
        self._set_value("startDate", value)

    def get_end_date(self):
        return self._get_value("endDate")

    def set_end_date(self, value):
        self._set_value("endDate", value)

    def get_member_name(self):
        return self._get_value("srchMemberName")

    def set_member_name(self, value):
        return self._set_value("srchMemberName", value)

    def get_member_id(self):
        return self._get_value("srchMemberId")

    def set_member_id(self, value):
        self._set_value("srchMemberId", value)

    def _goto_sub_menu(self, menu_code="CMS3510"):
        d = self._current_driver
        sub_menu = d.find_element_by_id(menu_code)
        sub_menu.click()
        self._sub_menu_code = menu_code

    def _set_display_size(self, value=100):
        select_box = self._current_driver.find_element_by_id("setListPerPage")
        display = Select(select_box)
        display.select_by_value(str(value))

    def submit(self):
        search = self._current_driver.find_element_by_css_selector("#content_wrap input:nth-child(1)")
        search.click()
        import time
        time.sleep(1)
        return self

    def result(self):
        """
        자동이체 -> 출금결과 조회
        :return:
        """
        for row in self._current_driver.find_elements_by_css_selector("#v-tab01>tbody>tr[id='v-list']"):
            cols = [x.text.strip() for x in row.find_elements_by_css_selector("td")]
            yield WithDrawResult(date=cols[2][:10],
                                 user_id=cols[3],
                                 user_name=cols[4],
                                 phone4=cols[5].split("-")[2],
                                 status=cols[9].split("[")[0].strip())




