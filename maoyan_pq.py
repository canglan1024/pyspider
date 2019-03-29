from pyquery import PyQuery as pq
import requests
import re,json,time
from requests.exceptions import RequestException

def get_one_page(url):
	try:
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
		}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None
	
def parse_one_page(html):
	doc = pq(html)
	board = doc('.board-wrapper')
	for item in board('dd').items():
		yield {
			'index': item('.board-index').text(),
			'image': item('.board-img').attr('data-src'),
			'title': item('.name a').text(),
			'star':  item('.star').text().strip()[3:],
			'time':  item('.releasetime').text().strip()[5:],
			'score': item('.integer').text() + item('.fraction').text()
		}
		
def write_to_file(content):
	with open('result_pq.txt', 'a', encoding='utf-8') as f:
		f.write(json.dumps(content, ensure_ascii=False)+'\n')
	
	
def main(offset):
	url = 'http://maoyan.com/board/4?offset=' + str(offset)
	html = get_one_page(url)
	for item in parse_one_page(html):
		print(item)
		write_to_file(item)
	
if __name__ == '__main__':
	for i in range(10):
		main(offset=i*10)
		time.sleep(1)
