import datetime
from datetime import timedelta

#从代理网站中提取代理IP
class IP_logic:
    def __init__(self,IP_dict):
        IP_resp = IP_dict['data'][0]
        self.IP_url = "https://" + IP_resp['ip'] + ":" + str(IP_resp['port'])
        expire_time = IP_resp['expire_time']
        self.exprie_time = datetime.datetime.strptime(expire_time,'%Y-%m-%d %H:%M:%S')
        #IP是否被黑默认为否
        self.is_blacked = False


    #当前IP是否过期判定
    @property
    def time_expiring(self):
        #当前时间赋值给now
        now = datetime.datetime.now()
        # 若代理过期时间小于10s那么就更新代理。
        if self.expire_time - now <= timedelta(seconds=10):
            return True
        else:
            return False
