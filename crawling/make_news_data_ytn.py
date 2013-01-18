#encoding: cp949
###########################################################
'''
last updated: 2010-06-19
author: Hye-Jin Min
description: naver product name crwawling  
[update]
2010-06-19
1.get_api_result()에서 image url 추가 
'''
###########################################################

import urllib
import re
import time 

def find_news(search_word,display_num):
	open_api_url = "http://search.ytn.co.kr/ytn/index.php?page=%d&more=&site=ytn&type=ytn&q=%s&x=0&y=0&searchAdUrl="

	full_url = open_api_url % (display_num, urllib.quote(search_word)) 
	print full_url
	f = urllib.urlopen(full_url)
	html = f.read()
#	print html
#	html = (html.decode('utf-8')).encode('cp949')
	f.close()
	return display_result(html)

#api에서 주는 rss의 link 페이지 읽어서 cat_id, nv_mid찾기 
def display_result(html):
	news_dict = {}
	p = re.compile(r'<div class="searchMain">.*?</ul>(.*?)</div>', re.DOTALL)
	print p.search(html).groups()[0]
	
	p2 = re.findall(r'<')
	p2 = re.compile(r'<div class="searchMain">.*?</ul>(.*?)</div>', re.DOTALL)
 	
	return news_dict

def find_news_contents(link):
	try:
		f = urllib.urlopen(link)
	except IOError:
		return [], ''

	html = f.read()
	f.close()

	m = re.search(r'<div class="article-contents">',html)
	if m is None:
		return [], ''
	html = html[m.end():]

	m2 =  re.search(r'<div id="power-link2">',html)
	html = html[:m2.end()]

	html = re.sub(r'<div id="power-link2">','',html)
	html = re.sub(r'<img src="(.*)"/>','',html)
	html = re.sub(r'<div(.*)>', '',html)
	html = re.sub(r'</div>', '',html)
	html = re.sub(r'<table(.*)>', '',html)
	html = re.sub(r'</table>', '',html)
	html = re.sub(r'<td(.*)>', '',html)
	html = re.sub(r'</td>', '',html)
	html = re.sub(r'<!-- FLASH_BANNER -->', '',html)
	html = re.sub(r'<!--(.*)-->', '',html)
	html = re.sub(r'<SPAN(.*)>', '',html)
	html = re.sub(r'</SPAN>', '',html)
	html = re.sub(r'<tr>', '',html)
	html = re.sub(r'</tr>', '',html)
	html = re.sub(r'<p>', '',html)
	html = re.sub(r'<P>', '',html)
	html = re.sub(r'<p(.*)>', '',html)
	html = re.sub(r'<P(.*)>', '',html)
	html = re.sub(r'</p>', '',html)
	html = re.sub(r'</P>', '',html)
#	html = re.sub(r'<br />', '\n',html)
	html = re.sub(r'<br />', '\t',html)
	html = re.sub(r'<br>', '',html)
	html = re.sub(r'<center>', '',html)
	html = re.sub(r'</center>', '',html)
	html = re.sub(r'<strong>', '',html)
	html = re.sub(r'</strong>', '',html)
	html = re.sub(r'<ul(.*)>', '',html)
	html = re.sub(r'<li>', '',html)
	html = re.sub(r'<b>', '',html)
	html = re.sub(r'</b>', '',html)
	html = re.sub(r'<a href(.*)>', '',html)
	html = re.sub(r'<A href(.*)>', '',html)
	html = re.sub(r'</a>', '',html)
	html = re.sub(r'</A>', '',html)
	html= re.sub(r'\r\n', '',html)
	html = re.sub(r'<a target(.*)>', '',html)
	html = re.sub(r'&nbsp;', '',html)
	html = re.sub(r'&quot;', "'",html)
	html = re.sub(r'&lt;', "<",html)
	html = re.sub(r'&gt;', ">",html)
	html = re.sub(r'<font color=(.*)(.*)</font>', "",html)
	html = re.sub(r'<script(.*)(.*)</script>', "",html)
	html = (html.decode('utf-8')).encode('cp949')
	html = html.strip()

	highlight_list = []
	if re.search('<h4>(.*)</h4>', html):
		highlights =  re.search('<h4>(.*)</h4>', html).groups()
		highlight_list = (highlights[0].strip()).split('\t')
		html = re.sub('<h4>(.*)</h4>','', html)
		
	return highlight_list, html	
	
def write_file(title, news_link, h_list, contents,f):
	f.write('<news>\n')
	f.write(('<title>%s</title>\n') % title)
	f.write(('<link>%s</link>\n') % news_link)
	f.write(('<h_list>\n'))
	for h in h_list:
		f.write(('<h>%s</h>\n') % h)
	f.write('</h_list>\n')
	f.write('<contents>\n')
	f.write(contents)
	f.write('\n')
	f.write('</contents>\n')
	f.write('</news>')

def get_news(keyword, N,threshold):
	pageN = N/5
	news_id = 1
	for i in range(1,pageN+1):
		news_dict = find_news(keyword,i)
		for key in news_dict.keys():
			title = key
			news_link= news_dict[title]['news_link']
			h_list, contents = find_news_contents(news_link)

			'''
			for h in h_list:
				print h
			print contents
			'''

			if len(h_list) >= threshold:
				file_name = ('news_data/hani/keyword_list1/%s_%d.txt') % (keyword, news_id)
				f = open(file_name,'w')
				print ('%s:%s') % (keyword,title)
				write_file(title, news_link, h_list, contents,f)
				f.close()
				news_id = news_id+1

		time.sleep(3)

if __name__ == '__main__' : 
	keyword = '종합소득세'
	keyword = '학교폭력'
	keyword = '환율 붕괴'
	keyword = '지하철'
#	keyword = '태풍'
#	keyword = '자살'
	keyword = '미래창조'
	
	N = 10			
	h_threshold = 2 
	get_news(keyword, N,h_threshold)

