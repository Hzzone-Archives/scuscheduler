import requests
import config
import bs4
import ics
import datetime
import pytz

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
    courses_list = body.findAll('tr')
    scheduler = []
    temp = []
    for index in range(len(courses_list)):
        c = []
        row = courses_list[index]
        cells = row.findAll('td')
        for tr in cells:
            text = process(tr.text)
            # if text == '':
            #     continue
            c.append(text)
        temp.append(c)
    for index, course in enumerate(temp):
        c = []
        # course = temp[index-1]
        # print(course)
        # print(len(course))
        if len(course) != 17:
            name = temp[index-1][2]
            credit = temp[index-1][4]
            weeks = course[0]
            week = course[1]
            sections = course[2]
            location = course[3] + course[4] + course[5]
            c.extend([name, credit, weeks, week, sections, location])
            scheduler.append(c)
            continue
        name = course[2]
        credit = course[4]
        weeks = course[11]
        week = course[12]
        sections = course[13]
        location = course[14] + course[15] + course[16]
        c.extend([name, credit, weeks, week, sections, location])
        # print(c)
        scheduler.append(c)
    for course in scheduler:
        sections = course[4]
        course[4] = [int(x) for x in sections.split('~')]
        course[1] = float(course[1])
        course[3] = int(course[3])
    print(scheduler)


def add_events(path):
    courses = config.courses
    c = ics.Calendar()
    start_date = datetime.datetime.strptime(config.start_time, '%Y-%m-%d')
    tz = pytz.timezone('Asia/Taipei')
    for course in courses:
        course_name = course[0]
        course_description = '学分：' + str(course[1])
        course_weeks = course[2]
        course_week = course[3]
        course_section = course[4]
        course_location = course[5]
        for week in course_weeks:
            e = ics.Event()
            e.location = course_location
            e.description = course_description
            e.name = course_name
            delta = datetime.timedelta(days=(week-1)*7+course_week)
            temp = start_date + delta
            s_time = temp.strftime('%Y:%m:%d') + ' ' + classStartTimeJA[course_section[0]-1]
            e_time = temp.strftime('%Y:%m:%d') + ' ' + classEndTimeJA[course_section[-1]-1]
            d1 = datetime.datetime.strptime(s_time, '%Y:%m:%d %H:%M:%S')
            d2 = datetime.datetime.strptime(e_time, '%Y:%m:%d %H:%M:%S')
            d1 = d1.replace(tzinfo=tz)
            d2 = d2.replace(tzinfo=tz)
            delta = datetime.timedelta(minutes=6)
            d1 = d1 + delta
            d2 = d2 + delta
            e.begin = d1
            e.end = d2
            c.events.append(e)
    with open(path, 'w') as f:
        f.writelines(c)

if __name__ == "__main__":
    parser(login())
    # add_events('/Users/HZzone/Desktop/course.ics')

