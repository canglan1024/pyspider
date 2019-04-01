from selenium import webdriver
import pymysql
import datetime

time = datetime.datetime.now()
table_name = 'M'+str(time.month)+'D'+str(time.day)+'h'+str(time.hour)+'m'+str(time.minute)

url = 'http://top.baidu.com/buzz?b=1&fr=topindex'

host = 'localhost'
port = 3306
username = 'root'
password = 'password'
database = 'baidu_top'

try:
    db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
    cursor = db.cursor()
except pymysql.MySQLError as e:
    print(e.args)

create_table = "CREATE TABLE " + table_name + "(rank int UNSIGNED AUTO_INCREMENT,keyword varchar(100) NOT NULL,hit int NOT NULL,PRIMARY KEY(rank))DEFAULT charset=utf8;"

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

titles = browser.find_elements_by_class_name('list-title')
hits = browser.find_elements_by_class_name('last')
for i in range(50):
    rank = str(i+1)
    keyword = titles[i].text
    hit = hits[i+2].text
    try:
        cursor.execute("INSERT INTO "+table_name+"(rank,keyword,hit)  VALUES(%s,%s,%s);", (rank, keyword, hit))
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

print('Save to ', table_name, ' in ', database, ' completed!')
browser.quit()
cursor.close()
db.close()
