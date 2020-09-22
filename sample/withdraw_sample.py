# -*- coding: utf-8 -*-
from thebill import Login
from thebill.withdraw import WithDrawResult, WithDraw
import pyrebase
import hashlib
from urllib.parse import quote

# firebase 연결 정보
firebaseConfig = {
    "apiKey": "dsfsaf-adsfasd",
    "authDomain": "asdfsadf.firebaseapp.com",
    "databaseURL": "https://sdafasf.firebaseio.com",
    "projectId": "asdfasdf",
    "storageBucket": "asdfasdfasdf.appspot.com",
    "messagingSenderId": "dfdf",
    "appId": "1:asdfasdf:web:asdfasd",
    "measurementId": "G-asdfsdaf"
}

firebase = pyrebase.initialize_app(firebaseConfig)

login = Login(user_id='<id>', password='<password>', driver_path="<driver path>")
login.headless(True)


# key 를 만들어 낸다 (이름 + 전화번호 4자리)
def key_create(result):
    _src = "{}{}".format(result.user_name, result.phone4)
    _encode_key = quote(_src)
    _encode = hashlib.sha256(_encode_key.encode("utf-8"))
    return _encode.hexdigest()


if __name__ == "__main__":
    db = firebase.database()
    count = 0
    with WithDraw() as withdraw:
        withdraw.submit()
        for r in withdraw.result():
            key = key_create(r)
            find_user = db.child("the_bill").child(key).get().val()
            last_date = max(r.date if ("출금성공" in r.status or "정산완료" in r.status) else "",
                            "" if find_user is None else find_user.get("last_date") or "")
            if find_user is not None and r.date < find_user.get("date") and last_date == "":
                print("[SKIP] update 할 필요가 없는 데이터 =>", last_date, r, find_user)
                continue
            count += 1
            if count % 100 == 0:
                print("INTERVAL - {}".format(count))
            new_data = dict(user_id=r.user_id, date=r.date, status=r.status, last_date=last_date)
            db.child("the_bill").child(key).set(new_data)
            print(count, key, new_data)
