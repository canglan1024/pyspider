import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 保存文件
filename = 'answers.txt'
# 问题ID
q_id = ''

# 关闭图像加载
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
         'images': 2,   # 1使用 2关闭
            }
    }
options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(chrome_options=options)
browser.get('https://www.zhihu.com/question/' + q_id)
time.sleep(3)
wait = WebDriverWait(browser, 2)

# 问题、网址、关键词、回答数、评论数、创建时间、修改时间、浏览数、关注数
q_name = browser.find_element_by_xpath('//meta[@itemprop="name"]').get_attribute('content')
q_url = browser.find_element_by_xpath('//meta[@itemprop="url"]').get_attribute('content')
q_keywords = browser.find_element_by_xpath('//meta[@itemprop="keywords"]').get_attribute('content')
q_answerCount = browser.find_element_by_xpath('//meta[@itemprop="answerCount"]').get_attribute('content')
q_commentCount = browser.find_element_by_xpath('//meta[@itemprop="commentCount"]').get_attribute('content')
q_dateCreated = browser.find_element_by_xpath('//meta[@itemprop="dateCreated"]').get_attribute('content')
q_dateModified = browser.find_element_by_xpath('//meta[@itemprop="dateModified"]').get_attribute('content')
q_visitsCount = browser.find_element_by_xpath('//meta[@itemprop="zhihu:visitsCount"]').get_attribute('content')
q_followerCount = browser.find_element_by_xpath('//meta[@itemprop="zhihu:followerCount"]').get_attribute('content')

# 问题详情
button_detail_more = browser.find_element_by_class_name('QuestionRichText-more')
button_detail_more.click()
q_detail = browser.find_element_by_class_name('QuestionHeader-detail').text

# 保存问题详情
with open(filename, 'a', encoding='utf-8') as f:
    f.write('问题：' + q_name + '\n')
    f.write('链接：' + q_url + '\n')
    f.write('关键词：' + q_keywords + '\n')
    f.write('回答数：' + q_answerCount + '\n')
    f.write('评论数：' + q_commentCount + '\n')
    f.write('浏览数：' + q_visitsCount + '\n')
    f.write('关注数：' + q_followerCount + '\n')
    f.write('创建日期：' + q_dateCreated + '\n')
    f.write('修改日期：' + q_dateModified + '\n')
    f.write('问题描述：' + q_detail + '\n')
    f.write('回答列表：' + '\n\n')


def get_answer(a_index):
    """
    获取回答并存入列表
    :param a_index: 回答索引
    :return:
    """

    xpath = '//div[@data-za-index="' + str(a_index) + '"]'
    try:
        loaded = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print('timeout')
        # 滚动条下滑加载新回答
        js = "document.documentElement.scrollTop=" + str(a_index*100000)
        browser.execute_script(js)
        # time.sleep(2)
        get_answer(a_index)
        return

    try:
        # 回答者、签名、赞同数、回答内容
        author_name = loaded.find_element_by_class_name('AuthorInfo-head').text
        author_detail = loaded.find_element_by_class_name('AuthorInfo-detail').text
        # answer_voters = loaded.find_element_by_class_name('Voters').text  # 0赞无此条目
        answer_text = loaded.find_element_by_class_name('CopyrightRichText-richText').text
    except NoSuchElementException:
        print('nosuch')
        time.sleep(2)
        get_answer(a_index)
        return

    answer = {'index': index, 'name': author_name, 'detail': author_detail,
              'answer': answer_text}
    print('index=' + str(a_index))

    # 保存回答
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(str(answer) + '\n')
    return


for index in range(0, 1000):
    get_answer(index)

browser.close()
