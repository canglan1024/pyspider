from selenium import webdriver
import pymysql
import datetime

time = datetime.datetime.now()
table_name = 'M'+str(time.month)+'D'+str(time.day)+'h'+str(time.hour)+'m'+str(time.minute)

url = 'https://s.weibo.com/top/summary?cate=realtimehot'

host = 'localhost'
port = 3306
username = 'root'
password = 'password'
database = 'weibo_top'

try:
    db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
    cursor = db.cursor()
except pymysql.MySQLError as e:
    print(e.args)

create_table = "CREATE TABLE " + table_name + "(rank int AUTO_INCREMENT,keyword varchar(100) NOT NULL,hit int NOT NULL,PRIMARY KEY(rank))DEFAULT charset=utf8;"

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

titles = browser.find_elements_by_class_name('td-02')
for i in range(51):
    rank = str(i+1)
    if i == 0:
        keyword = titles[i].text
        hit = '999999'
    else:
        words = titles[i].text.split(' ')
        n = len(words)
        if n == 2:
            keyword = words[0]
            hit = words[1]
        elif n > 2:
            keyword = ''.join(words[0:-1])
            hit = words[n-1]
        else:
            continue

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
