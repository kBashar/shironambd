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

	
POLITICS_INDEX = 0
CRICKET_INDEX = 1
ENTERTAINMENT_INDEX = 2
SCIENCE_INDEX = 3
CAMPUS_INDEX = 4
BUSSINESS_INDEX = 5
TECHNOLOGY_INDEX = 6
LIFESTYLE_INDEX = 7
HEALTH_INDEX = 8
ENVIRONMENT_INDEX = 9

def debug_me(data_list):
	if len(data_list):
		return data_list
	

def iter_soup_clean_text(soup):
	for news in soup:
		yield news.text.replace('&#39;', "'")

class BdNews24English(BaseCrawler):
	
	def get_lead_news(self):
		soup = self.get_soup()
		lead_news = soup.find('font',{'size':4})
		print lead_news.getString()
		
	def get_latest_news(self):
		soup = self.get_soup()
		main_box = soup.find('div',{'id':'thdivbox'})
		latest_newses = main_box.findAll('li',{'class':'latestnews'})
		latest_news = latest_newses[13:]
		for news in latest_newses:
			print news.text
		
	def get_box_news(self):
		soup = self.get_soup()
		box_soup_left = soup.findAll('div',{'id':'hmdivbox1'})
		box_soup_right = soup.findAll('div',{'id':'hmdivbox2'})
		box_left = []
		box_right = []
		for box in box_soup_left:
			box_left.append(box.find('span').text)
		
		for box in box_soup_right:
			box_right.append(box.find('span').text)
		
		return box_left+box_right
		
	def get_category_news(self):
		soup = self.get_soup()
		modules = soup.findAll('div',{'class':'module'})
		categorized_news = {}
		
		soup_politics = modules[POLITICS_INDEX].findAll('li', {'class':'latestnews'})
		soup_cricket = modules[CRICKET_INDEX].findAll('a', {'class':'latestnews'})
		soup_entertainment = modules[ENTERTAINMENT_INDEX].findAll('li', {'class':'latestnews'})
		soup_science = modules[SCIENCE_INDEX].findAll('li', {'class':'latestnews'})
		soup_campus = modules[CAMPUS_INDEX].findAll('li', {'class':'latestnews'})
		soup_bussiness = modules[BUSSINESS_INDEX].findAll('li', {'class':'latestnews'})
		soup_tech = modules[TECHNOLOGY_INDEX].findAll('li', {'class':'latestnews'})
		soup_ls = modules[LIFESTYLE_INDEX].findAll('li', {'class':'latestnews'})
		soup_health = modules[HEALTH_INDEX].findAll('li', {'class':'latestnews'})	
		politics_headlines = []
		cricket_headlines = []
		entertainment_headlines = []
		science_headlines = []
		campus_headlines = []
		bussiness_headlines = []
		tech_headlines = []
		ls_headlines = []
		health_headlines = []
		
		for news in iter_soup_clean_text(soup_politics):
			politics_headlines.append(news)
		categorized_news.update({'politics':politics_headlines})
				
		for news in iter_soup_clean_text(soup_cricket):
			cricket_headlines.append(news)
		categorized_news.update({'cricket':cricket_headlines})

			
		for news in iter_soup_clean_text(soup_entertainment):
			entertainment_headlines.append(news)
		categorized_news.update({'entertainment':entertainment_headlines})

		for news in iter_soup_clean_text(soup_science):
			science_headlines.append(news)
		categorized_news.update({'science':science_headlines})
			
		for news in iter_soup_clean_text(soup_campus):
			campus_headlines.append(news)
		categorized_news.update({'campus':campus_headlines})
	
		for news in iter_soup_clean_text(soup_bussiness):
			bussiness_headlines.append(news)
		categorized_news.update({'bussiness':bussiness_headlines})
						
		for news in iter_soup_clean_text(soup_tech):
			tech_headlines.append(news)
		categorized_news.update({'tech':tech_headlines})
		
		for news in iter_soup_clean_text(soup_ls):
			ls_headlines.append(news)
		categorized_news.update({'lifestyle':ls_headlines})

		for news in iter_soup_clean_text(soup_health):
			health_headlines.append(news)
		categorized_news.update({'health':health_headlines})
		
		import pdb;pdb.set_trace();
		
		return categorized_news

		
			

if __name__ == '__main__':
	bUrl = 'http://bdnews24.com/bangla'
	# bUrl = 'http://scrape.local/'
	bdN = BdNews24English(bUrl)
	print bdN.get_category_news()
	
	
