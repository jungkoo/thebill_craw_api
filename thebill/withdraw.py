# -*- coding: utf-8 -*-
from collections import namedtuple

from thebill import Login

WithDrawResult = namedtuple('WithDrawResult', 'date code name phone4 status')


class WithDraw:
    def __init__(self):
        self._login: Login = Login.current()
        self._current_driver = self._login.webdriver()  # login 한 브라우저창을 재활용한다.
        self._start_date = None
        self._end_date = None
        self._name = None
        self._code = None
        self._result_size = 10
        self._sub_menu_code = ""
        self._load_page()

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

    def _goto_sub_menu(self, menu_code="CMS3510"):
        d = self._current_driver
        sub_menu = d.find_element_by_id(menu_code)
        sub_menu.click()
        self._sub_menu_code = menu_code

    def member_details(self):
        """
        회원개별출금
        :return:
        """
        if "CMS3510" != self._sub_menu_code:
            self._goto_sub_menu("CMS3510")

        # select 조건 변경

        # 조회

        # 결과 리턴

