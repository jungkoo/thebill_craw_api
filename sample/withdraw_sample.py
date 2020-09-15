# -*- coding: utf-8 -*-
from thebill import Login
from thebill.withdraw import WithDraw

login = Login(user_id='<아이디>', password='<비밀번호>', driver_path="<chromedriver 경로>")
login.headless(False)

if __name__ == "__main__":
    withdraw = WithDraw()
    withdraw.goto_sub_menu()
