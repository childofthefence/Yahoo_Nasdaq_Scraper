#!/usr/bin/env python
import re
import sys
import logging


class StocksFromYahooNasdaqAndCrypto:
	stock_name = ''
	urls = ''
	stock_main_url = ''
	stock_history = ''
	name_main = ''
	name_history = ''
	stocks_dict = {}
	stocks_history_dict = {}
	stock_list = 'stock-location.txt'
	
	logging.basicConfig(
		filename='YahooFinancialLog.log', level=logging.DEBUG, format='%(asctime)s - StocksFromYahooClass - %(message)s')
	
	def main(self):
		
		try:
			logging.debug('Start of main method')
			while True:
				stocks = StocksFromYahooNasdaqAndCrypto()
				stocks.open_and_find_sources()
				value_to_display = int(input(
					'\nPress 1 for main page\nPress 2 for history page\nPress 3 to add stock\nPress 0 to exit\nInput: '))
				
				stocks.choose_value(value_to_display)
				
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			logging.error(message)
			
	def open_and_find_sources(self):
		
		try:
			logging.debug('open_and_find_sources called')
			f = open(self.stock_list, 'r')
			
			for lines in f:
				
				if lines.startswith('*'):
					self.stock_name, self.urls = lines.split('==')
					self.stock_main_url, self.stock_history = self.urls.split(',')
					self.stocks_dict[self.stock_name] = self.stock_main_url
					self.stocks_history_dict[self.stock_name] = self.stock_history
			
			f.close()
		
		except FileNotFoundError:
			logging.error('file not found error')
	
	def display_urls(self):
		
		logging.debug('display_urls called')
		for key, values in self.stocks_dict.items():
			print('stock name: {}'.format(key) + '\nstock url: {}'.format(values))
	
	def display_history_pages(self):
		
		logging.debug('display_history_pages called')
		for key, values in self.stocks_history_dict.items():
			print('stock name: {}'.format(key) + '\nstock history url: {}'.format(values))
	
	def choose_value(self, x):
		
		try:
			if x == 1:
				self.display_urls()
			elif x == 2:
				self.display_history_pages()
			elif x == 3:
				user_input = input('Type stock alias: ')
				if not self.check_if_stock_in_file(user_input):
					self.append_stock_to_textfile(user_input)
			elif x == 0:
				logging.info('System exiting')
				sys.exit()
			else:
				raise ValueError
				
		except ValueError:
			
			logging.error('Not a valid entry')
			sys.exit()
	
	def append_stock_to_textfile(self, name):
		
		logging.debug('append_stock_to_textfile called')
		logging.debug('Adding ' + name + ' to list')
		f = open('stock-location.txt', 'a')
		self.name_main = 'https://finance.yahoo.com/quote/' + name + '/?p=' + name
		self.name_history = 'https://finance.yahoo.com/quote/' + name + '/history?p=' + name
		f.write('\n*' + name + '==' + self.name_main + ',' + self.name_history)
		f.close()
	
	def check_if_stock_in_file(self, name):
		
		bool_found = False
		f = open('stock-location.txt', 'r')
		for lines in f:
			
			if lines.startswith('*' + name):
				bool_found = True
		
		return bool_found


if __name__ == '__main__':
	
	StocksFromYahooNasdaqAndCrypto.main(StocksFromYahooNasdaqAndCrypto())