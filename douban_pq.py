from pyquery import PyQuery as pq
import requests
import re,json,time
import csv,codecs
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
	board = doc('#content')
	for item in board('li').items():
		yield {
			'index': item('em').text(),
			'title': item('.title').text(),
            'score': item('.star').text(),
			'stuff': item('.bd p:first-child').text().splitlines()[0],
			'tags':  item('.bd p:first-child').text().splitlines()[1],
			'quote': item('.quote').text()
                        }
		
def write_to_file(content):
	with codecs.open('douban_top250.csv', 'a', 'utf_8_sig') as csvfile:
		fieldnames = ['index', 'title', 'score', 'stuff', 'tags', 'quote']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		#writer.writeheader()
		writer.writerow(content)
	
	
def main(offset):
	url = 'https://movie.douban.com/top250?start=' + str(offset)
	html = get_one_page(url)
	for item in parse_one_page(html):
		write_to_file(item)
	
if __name__ == '__main__':
	print('Working:')
	for i in range(25):
		main(offset=i*10)
		print('*')
		time.sleep(1)
	print('\nDone!')
