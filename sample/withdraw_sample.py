# -*- coding: utf-8 -*-
from thebill import BrowserLogin, LoginSession
import pyrebase
import hashlib
from urllib.parse import quote
import datetime
from thebill.payment import PaymentAPI

start_date_str = (datetime.date.today() - datetime.timedelta(2)).strftime("%Y-%m-%d")
end_date_str = (datetime.date.today() + datetime.timedelta(5)).strftime("%Y-%m-%d")

# firebase 연결 정보
firebaseConfig = {
    "apiKey": "ddasfdsaf-Ssg",
    "authDomain": "asdfasdfasdf.firebaseapp.com",
    "databaseURL": "https://asdfasdfsdf.firebaseio.com",
    "projectId": "asdfasdf",
    "storageBucket": "dsfasdf.appspot.com",
    "messagingSenderId": "234234324234",
    "appId": "1:234234234:web:48017940e16f836b02471a",
    "measurementId": "G-fsadfadsf"
}

firebase = pyrebase.initialize_app(firebaseConfig)
LoginSession(user_id='<패스워드>', password='<암호>')


# key 를 만들어 낸다 (이름 + 전화번호 4자리)
def key_create(result):
    _src = "{}{}".format(result.user_name, result.phone4)
    _encode_key = quote(_src)
    _encode = hashlib.sha256(_encode_key.encode("utf-8"))
    return _encode.hexdigest()


if __name__ == "__main__":
    db = firebase.database()
    api = PaymentAPI()
    count = 0

    for r in api.with_draw_result(start_date=start_date_str, end_date=end_date_str):
        key = key_create(r)
        find_user = db.child("the_bill").child(key).get().val()
        last_date = max(r.date if ("정상처리" in r.status or "출금성공" in r.status) else "",
                        "" if find_user is None else find_user.get("last_date") or "")
        if find_user is not None and r.date <= find_user.get("date"):
            print("[SKIP] update 할 필요가 없는 데이터 =>", last_date, r, find_user)
            continue
        count += 1
        if count % 100 == 0:
            print("INTERVAL - {}".format(count))
        new_data = dict(user_id=r.user_id, date=r.date, status=r.status, last_date=last_date)
        db.child("the_bill").child(key).set(new_data)
        # print(count, key, last_date, "||old=>", find_user, "||new=>", r, "||update=>", new_data)
    print("[완료] 총 {} 건".format(count))
