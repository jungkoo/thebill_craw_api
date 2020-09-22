# -*- coding: utf-8 -*-
from thebill import Login
from thebill.withdraw import WithDraw
import pyrebase
import hashlib
from urllib.parse import quote

# firebase 연결 정보
firebaseConfig = {
    "apiKey": "sdafdfssdafsadfasdf-Ssg",
    "authDomain": "naveruniuon.firebaseapp.com",
    "databaseURL": "https://naveruniuon.firebaseio.com",
    "projectId": "sdfsdfasdf",
    "storageBucket": "asdfasdf.appasdfsdfspot.sdfas",
    "messagingSenderId": "asdfasdfasf",
    "appId": "1:dfasdfasf:web:sdfadsfasdf",
    "measurementId": "G-asdfadsf"
}

firebase = pyrebase.initialize_app(firebaseConfig)

login = Login(user_id='<아이디>', password='<암호>', driver_path="<구글 크롬 드라이버 위치>")
login.headless(False)


# key 를 만들어 낸다 (이름 + 전화번호 4자리)
def key_create(result):
    _src = "{}{}".format(result.user_name, result.phone4)
    _encode_key = quote(_src)
    _encode = hashlib.sha256(_encode_key.encode("utf-8"))
    return _encode.hexdigest()


if __name__ == "__main__":
    db = firebase.database()

    with WithDraw() as withdraw:
        withdraw.submit()
        for r in withdraw.result():
            key = key_create(r)
            find_user = db.child("the_bill").child(key).get().val()
            if (find_user is not None) and (find_user.get("date") > r.date) and find_user.get("last_date") != "":
                print("[SKIP] 수집한 데이터가 오래된 데이터입니다")
                continue

            last_date = max(r.date if r.status in ("출금성공", "정산완료") else "", find_user.get("last_date") or "")
            new_data = dict(user_id=r.user_id, date=r.date, status=r.status, last_date=last_date)
            db.child("the_bill").child(key).set(new_data)  # merge
