from selenium import webdriver
import pymysql
import datetime

time = datetime.datetime.now()
table_name = 'M'+str(time.month)+'D'+str(time.day)+'h'+str(time.hour)+'m'+str(time.minute)

url = 'https://www.zhihu.com/billboard'

host = 'localhost'
port = 3306
username = 'root'
password = 'password'
database = 'zhihu_top'

try:
    db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
    cursor = db.cursor()
except pymysql.MySQLError as e:
    print(e.args)

create_table = "CREATE TABLE " + table_name + "(rank int UNSIGNED AUTO_INCREMENT,question varchar(255) NOT NULL,detail varchar(511) NOT NULL,hot varchar(127) NOT NULL,PRIMARY KEY(rank))DEFAULT charset=utf8;"

try:
    cursor.execute(create_table)
    db.commit()
except Exception as e:
    db.rollback()
    print(e)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)

questions = browser.find_elements_by_class_name('HotList-itemTitle')
details = browser.find_elements_by_class_name('HotList-itemExcerpt')
hots = browser.find_elements_by_class_name('HotList-itemMetrics')
for i in range(50):
    rank = str(i+1)
    question = questions[i].text
    hot = hots[i].text
    if i < len(details):
        detail = details[i].text
    else:
        detail = ''
    try:
        cursor.execute("INSERT INTO "+table_name+"(rank,question,detail,hot)  VALUES(%s,%s,%s,%s);", (rank, question, detail, hot))
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

print('Save to ', table_name, ' in ', database, ' completed!')
browser.quit()
cursor.close()
db.close()
