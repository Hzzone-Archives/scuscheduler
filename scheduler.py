import requests
import config
import bs4
import ics

BASE_URL = "http://zhjw.scu.edu.cn"
LOGIN_URL = BASE_URL + "/loginAction.do"
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
headers = {
    "User-Agent": agent
}
time_delay = 1
data = {"zjh": config.zjh, "mm": config.mm}
classStartTimeJA = ['08:15:00', '09:10:00', '10:15:00', '11:10:00', '13:50:00', '14:45:00', '15:40:00', '16:45:00', '17:40:00', '19:20:00', '20:15:00', '21:10:00'];
classEndTimeJA = ['09:00:00', '09:55:00', '11:00:00', '11:55:00', '14:35:00', '15:30:00', '16:25:00', '17:30:00', '18:25:00', '20:05:00', '21:00:00', '21:55:00'];

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


def process(text):
    text = text.replace(' ', '')
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\t', '')
    text = text.strip()
    return text

def parser(scheduler_html):
    soup = bs4.BeautifulSoup(scheduler_html)
    table = soup.select('table.displayTag')[1]
    body = table.find_all('tbody')[0]
    scheduler = ics.Calendar()
    courses = []
    for index, row in enumerate(body.findAll('tr')):
        c = []
        for tr in row.findAll('td'):
            rowspan = tr['rowspan']
            text = process(tr.text)
            if text == '':
                continue
            c.append(text)
        generate_one_course()
        if rowspan == 1:
            pass
        elif rowspan == 2:
            pass
        else:
            pass

def generate_one_course(c):
    e = ics.Event()
    week = c[10]
    print(week)

if __name__ == "__main__":
    parser(login())
