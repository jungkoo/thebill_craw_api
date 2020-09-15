# -*- coding: utf-8 -*-
from thebill import Login
from thebill.withdraw import WithDraw

login = Login(user_id='<아이디>', password='<비밀번호>', driver_path="<chromedriver 경로>")
login.headless(False)

if __name__ == "__main__":
    withdraw = WithDraw()
    for r in withdraw.result():
        print(r)

    print("# 검색")
    withdraw.set_start_date("2020-08-14")
    withdraw.set_member_name("홍길동")
    withdraw.submit()
    for r in withdraw.result():
        print(r)
