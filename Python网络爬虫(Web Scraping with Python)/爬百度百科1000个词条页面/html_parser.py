#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import urllib.request
from http import cookiejar
from bs4 import BeautifulSoup
import urllib.parse
import re

class HtmlParser():

	def _get_new_urls(self,page_url, soup):
		new_urls = set()
		#/item/Python/407313
		links = soup.find_all('a', href=re.compile(r'/v\d+\.htm'))
		# links = soup.find_all('a', href=re.compile(r'/item/.*'))
		for link in links:
			new_url = link['href']
			new_full_url = urllib.parse.urljoin(page_url,new_url)
			new_urls.add(new_full_url)

		return new_urls

	def _get_new_data(self,page_url, soup):
		res_data = {}
		# url
		res_data['url'] = page_url
		# <dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
		# title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')

		# <div class="lemma_name"><h1 id="title" data-full-title="Python">Python</h1>
		title_node = soup.find('div', class_='lemma_name').find('h1',id='title')
		
		res_data['title'] = title_node.get_text()
		# <div class="lemma-summary">
		# summary_node = soup.find('div', class_='lemma-summary')

		# <div class="abstract"><div class="edit_abstract"></div>
		summary_node = soup.find('div', class_='abstract')
		res_data['summary'] = summary_node.get_text()

		return res_data

	def parse(self, page_url, html_cont):

		if page_url is None or html_cont is None:
			return

		soup = BeautifulSoup(html_cont, 'html.parser')
		new_urls = self._get_new_urls(page_url, soup)
		new_data = self._get_new_data(page_url, soup)
		return new_urls, new_data