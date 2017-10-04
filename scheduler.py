import requests
import config
import bs4
import numpy as np

BASE_URL = "http://zhjw.scu.edu.cn"
LOGIN_URL = BASE_URL + "/loginAction.do"
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
headers = {
    "User-Agent": agent
}
time_delay = 1
data = {"zjh": config.zjh, "mm": config.mm}

def login():
    jwc_session = requests.session()
    jwc_session.post(LOGIN_URL, data=data)
    jwc_session.headers.update(headers)
    while True:
        try:
            jwc_session.get(LOGIN_URL, timeout=time_delay)
            # 再访问一次加入cookies
            r = jwc_session.get(LOGIN_URL, timeout=time_delay)
            # 登录
            r = jwc_session.post(LOGIN_URL, data=data, timeout=time_delay)

            # 检查密码是否正确
            r = jwc_session.get(BASE_URL + "/xkAction.do?actionType=6", timeout=time_delay)


            if "错误信息" not in r.text:
                break
            else:
                print("账号或密码不正确，请重新输入账号和密码...")

        except:
            pass
    return r.text


class course:
    def __init__(self):
        pass


def parser(scheduler_html):
    soup = bs4.BeautifulSoup(scheduler_html)
    table = soup.select('table.titleTop2')[1]
    scheduler_array = []
    for row in table.findAll('tr'):
        for tr in row.findAll('td'):
            text = tr.text
            text = text.replace(' ', '')
            text = text.replace('\n', '')
            print('*'+text+'*')
            scheduler_array.append(tr.text)
    scheduler = np.array(scheduler_array)
    # scheduler = np.reshape(scheduler, (-1, 17))
    # print(scheduler)

if __name__ == "__main__":
    parser(login())
