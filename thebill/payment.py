# -*- coding: utf-8 -*-
from collections import namedtuple
from thebill import LoginSession

WithDrawResult = namedtuple('WithDrawResult', 'date user_id user_name phone4 status')


class PaymentAPI:
    def __init__(self):
        self._session: LoginSession = LoginSession.current()

    def with_draw_result(self, start_date, end_date):
        """
        자동이체 -> 출금결과 조회
        :return:
        """
        seed_url = "https://www.thebill.co.kr/cms2/cmsPayList.json"
        req_data = dict(sortGubn1="01", sortGubn2="D", setListPerPage=10, divAcctYN="N", searchDateType="send",
                        startDate=start_date, endDate=end_date, serviceType="", statusCd="", srchMemberName="",
                        srchMemberId="", srchDealWon="", srchServiceName="", srchCusGubn1="", srchCusGubn2="", pageno=1)
        for row in self._session.result_list_generator(seed_url, **req_data):
            date = row.get("sendDt")
            new_date = date[0:4] + "-" + date[4:6] + "-" + date[6:8] # minbdate  orgSendDt
            user_id = row.get("memberId", "")
            phone4 = row.get("hpNo", "")[-4:]
            user_name = row.get("memberName", "")
            result_msg = row.get("statusNm", "") + "[" + row.get("resultMsg", "") + "]"
            yield WithDrawResult(date=new_date, user_id=user_id, user_name=user_name, phone4=phone4, status=result_msg)
