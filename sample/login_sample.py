# -*- coding: utf-8 -*-
from thebill import Login

login = Login(user_id='<아이디>', password='<비밀번호>', driver_path="<chromedriver 경로>")
login.headless(False)

if __name__ == "__main__":
    d = login.webdriver()
    import time
    time.sleep(5)
    d.close()
