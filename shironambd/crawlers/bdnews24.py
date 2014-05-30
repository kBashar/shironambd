#!/usr/bin/env python
# encoding: utf-8
"""
bdnews24.py

Created by Caveman on 2012-12-12.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os

from base import BaseCrawler
from datetime import datetime
from utils import build_news_object

import setup_django
from shironambd.home.models import News

BASE_URL = 'http://bdnews24.com/bangla'
TOTAL_MOST_READ = 7
TOTAL_RECENT_STORIES = 7


NEWS_CATEGORIES = ['health','science','environment',
				'lifestyle','politics','sport','economy']

SOURCE_NAME = 'BDNEWS24.COM'

def iter_soup_build_news(soup):
	# import pdb;pdb.set_trace();
	try:
		link = soup.find('a')['href']
	except TypeError:
		link = soup['href']

	title = soup.text.replace('&#39;', "'")

	news = News()
	news.link = link
	news.title = title
	# news.published_at ??
	news.created_at = datetime.now()
	# print news
	return news
		


class BdNews24(BaseCrawler):
	
	def __inti__(self):
		print "Called!"
		self.get_lead_news()
		self.get_latest_news()
		self.get_most_read()
		self.get_recent_stories()
		self.get_categorized_news()
		
	def get_tab_soup(self):
		soup = self.get_soup()
		tab_soup = soup.find('div', {'id':'tabs-2'})
		return tab_soup

	def get_lead_news(self, is_categorized=False):
		soup = self.get_soup()
		coulumns = soup.findAll('div', {'class':'column-1'})
		others_lead = coulumns[1].findAll('h3')
		for news in others_lead:
			if is_categorized != True:
				self.do_save(build_news_object(news, SOURCE_NAME), ['lead_news'])
			else:
				yield build_news_object(news, SOURCE_NAME)
		
	def get_latest_news(self):
		soup = self.get_soup()
		latest_news_class = 'x340x230x240x170 '
		latests_soup = soup.find('div',{'class':latest_news_class})
		latest_newses = latests_soup.findAll('li')
		for news in latest_newses:

			self.do_save(iter_soup_build_news(news), ['latest_news'])
					
	def get_most_read(self):
		tab_soup = self.get_tab_soup()
		raw_newses_titles = tab_soup.findAll('li')[3:TOTAL_MOST_READ+3]
		for news in raw_newses_titles:
			self.do_save(build_news_object(news, SOURCE_NAME), ['most_read'])

	def get_recent_stories(self):
		tab_soup = self.get_tab_soup()
		raw_newses_titles = tab_soup.findAll('li')[TOTAL_MOST_READ+3:]
		for news in raw_newses_titles:
			self.do_save(build_news_object(news, SOURCE_NAME), ['recent_stories'])
		
	def get_categorized_news(self):
		for category in NEWS_CATEGORIES:
			self.url = BASE_URL+category 
			print 'GETTING ...%s NEWS' % category
			for news in self.get_lead_news(is_categorized=True):
				self.do_save(news, category=category)