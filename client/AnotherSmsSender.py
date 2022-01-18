
import http.client
from urllib import parse


class SmsSender:
    apiKey = ""
    apiSecret = ""
    host = "api.qirui.com:7891"

    def __init__(self):
        self.apiKey = "2318250010"
        self.apiSecret = "06539b1f9a694128a4de"

    def getRequestUrl(self, mobile, message):
        params = parse.urlencode(
            {"dc": "15", "un": self.apiKey, "pw": self.apiSecret, "da": mobile, "sm": message, "tf": "3", "rf": "2",
             "rd": "1"})
        return "/mt?%s" % (params)

    def sendMsg(self, mobile, message):
        sendUrl = self.getRequestUrl(mobile, message)
        # print sendUrl
        conn = None
        try:
            conn = http.client.HTTPConnection(self.host, timeout=5)
            conn.request("GET", sendUrl)
            response = conn.getresponse()
            # print response.status, response.reason
            data = response.read()
            # 打印返回结果
            print(data)
        except Exception as e:
            print(e)
        finally:
            if (conn):
                conn.close()


if __name__ == "__main__":
    # 接受短信的手机号
    mobile = "15110202919"
    # 短信内容(【签名】+短信内容)，系统提供的测试签名和内容，如需要发送自己的短信内容请在启瑞云平台申请短信签名
    message = "【中电三公司】你好，你的验证码为：3325，有效期三分钟。"
    sender = SmsSender()
    sender.sendMsg(mobile, message)
