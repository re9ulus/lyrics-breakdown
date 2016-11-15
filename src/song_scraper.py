from bs4 import BeautifulSoup
import requests


class SongScrapper():

	def __init__(self):
		self.main_url = 'Not set in base class'

	def get_list_of_songs(self, artist):
		raise Exception('Method not implemented in base class')

	def parse_song(self, song_url):
		raise Exception('Method not implemented in base class')


class LyricsFreakScrapper(SongScrapper):

	def __init__(self):
		self.main_url = 'http://www.lyricsfreak.com/'

	def get_list_of_songs(self, artist):
		url = self.main_url + 'b/' + artist
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')
		html_items = soup.find_all('td', {'class': 'colfirst'})
		song_urls = {}
		for item in html_items:
			try:
				link = item.find('a').get('href')
				name = item.find('a').get('title')
				name = name.replace('Lyrics', '').strip()
				song_urls[name] = self.main_url + link
			except Exception, e:
				print('Can\'t parse song link: {}'.format(e))
		return song_urls

	def parse_song(self, song_url):
		resp = ''
		try:
			r = requests.get(song_url)
			soup = BeautifulSoup(r.content, 'html.parser')
			t = soup.find(id='content_h')
			resp = t.get_text(separator='\n')
		except Exception, e:
			print('Can\'t parse song from html: {}'.format(e))
		return resp


if __name__ == '__main__':

	scrapper = LyricsFreakScrapper()
	songs = scrapper.get_list_of_songs('beatles')

	for name, url in songs.items():
		print(name)
		song_lyrics = scrapper.parse_song(url)
		if not song_lyrics:
			continue
		try:
			with open('../data/beatles/{}.txt'.format(name), 'w+') as f:
				f.write(song_lyrics)
		except Exception, e:
			print('Can not write {0} lyrics to file: {1}'.format(name, e))
		print('\n==\n')
