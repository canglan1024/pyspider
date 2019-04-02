from selenium import webdriver
import pymysql
import datetime


def astr(num=0):
    if num < 10:
        return '0'+str(num)
    else:
        return str(num)


time = datetime.datetime.now()
table_name = 'M'+astr(time.month)+'D'+astr(time.day)+'h'+astr(time.hour)+'m'+astr(time.minute)

url = 'https://www.bilibili.com/ranking/all/0/0/7'

host = 'localhost'
port = 3306
username = 'root'
password = 'xuanyuan'
database = 'bili_top'

try:
    db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
    cursor = db.cursor()
except pymysql.MySQLError as e:
    print(e.args)

create_table = "CREATE TABLE " + table_name + "(rank int AUTO_INCREMENT,title varchar(255) NOT NULL,play varchar(40) " \
                                              "NOT NULL,view varchar(40) NOT NULL, author varchar(50), " \
                                              "url varchar(100), PRIMARY KEY(rank))DEFAULT charset=utf8;"

try:
    cursor.execute(create_table)
    db.commit()
except Exception as e:
    db.rollback()
    print(e)

options = webdriver.ChromeOptions()
# 无头模式
options.add_argument('--headless')
# 关闭沙盒 允许root运行
options.add_argument('--no-sandbox')
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,  # 不加载图片
        'javascript': 2,  # 不加载JS
    }
}
options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)

titles = browser.find_elements_by_class_name('title')
datas = browser.find_elements_by_class_name('data-box')
for i in range(len(titles)):
    rank = str(i+1)
    title = titles[i].text
    vurl = titles[i].get_attribute('href')
    play = datas[3*i].text
    view = datas[3*i+1].text
    author = datas[3*i+2].text
    try:
        cursor.execute("INSERT INTO "+table_name+"(rank,title,play,view,author,url)  VALUES(%s,%s,%s,%s,%s,%s);",
                       (rank, title, play, view, author, vurl))
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

print('Save to ', table_name, ' in ', database, ' completed!')
browser.quit()
cursor.close()
db.close()
