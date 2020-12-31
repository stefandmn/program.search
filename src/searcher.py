# -*- coding: utf-8 -*-

import sys
import common
import datetime

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui


class GlobalSearch(xbmcgui.WindowXMLDialog):

	def __init__(self, *args, **kwargs):
		common.debug('%s v%s has been started' % (common.AddonName(), common.AddonVersion()))
		self.searchstring = kwargs["searchstring"].replace('(', '[(]').replace(')', '[)]').replace('+', '[+]')
		common.debug('Getting search string: %s' %self.searchstring)


	def onInit(self):
		if self.searchstring == '':
			self._close()
		else:
			self.__winid = xbmcgui.getCurrentWindowDialogId()
			xbmcgui.Window(self.__winid).setProperty('GlobalSearch.SearchString', self.searchstring)
			self._HideControls()
			self._LoadParameters()
			if self.__params == {}:
				self._LoadSettings()
			self.__found = False
			self._search()


	def _HideControls(self):
		self.getControl(119).setVisible(False)
		self.getControl(129).setVisible(False)
		self.getControl(139).setVisible(False)
		self.getControl(149).setVisible(False)
		self.getControl(159).setVisible(False)
		self.getControl(169).setVisible(False)
		self.getControl(179).setVisible(False)
		self.getControl(189).setVisible(False)
		self.getControl(219).setVisible(False)
		self.getControl(198).setVisible(False)
		self.getControl(199).setVisible(False)


	def _ResetControls(self):
		self.getControl(111).reset()
		self.getControl(121).reset()
		self.getControl(131).reset()
		self.getControl(141).reset()
		self.getControl(151).reset()
		self.getControl(161).reset()
		self.getControl(171).reset()
		self.getControl(181).reset()
		self.getControl(211).reset()


	def _LoadParameters(self):
		try:
			self.__params = dict(arg.split("=") for arg in sys.argv[1].split("&"))
		except:
			self.__params = {}
		common.debug("Loading parameters: %s" %str(self.__params))
		self.movies = common.any2bool(self.__params.get("movies", ""))
		self.tvshows = common.any2bool(self.__params.get("tvshows", ""))
		self.episodes = common.any2bool(self.__params.get("episodes", ""))
		self.musicvideos = common.any2bool(self.__params.get("musicvideos", ""))
		self.artists = common.any2bool(self.__params.get("artists", ""))
		self.albums = common.any2bool(self.__params.get("albums", ""))
		self.songs = common.any2bool(self.__params.get("songs", ""))
		self.actors = common.any2bool(self.__params.get("actors", ""))


	def _LoadSettings(self):
		self.movies = common.setting("movies")
		self.tvshows = common.setting("tvshows")
		self.episodes = common.setting("episodes")
		self.musicvideos = common.setting("musicvideos")
		self.artists = common.setting("artists")
		self.albums = common.setting("albums")
		self.songs = common.setting("songs")
		self.actors = common.setting("actors")


	def _runNewSearch(self):
		keyboard = xbmc.Keyboard('', common.translate(32101), False)
		keyboard.doModal()
		if keyboard.isConfirmed():
			self.searchstring = keyboard.getText()
			self._ResetControls()
			self.onInit()


	def _search(self):
		self.getControl(199).setVisible(True)
		self.getControl(198).setVisible(True)
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + '[/B]')
		if self.artists:
			self._doArtistSearch()
		if self.albums:
			self._doAlbumSearch()
		if self.songs:
			self._doSongSearch()
		if self.musicvideos:
			self._doMusicvideoSearch()
		if self.actors:
			self._doActorSearch()
		if self.tvshows:
			self._doTVShowSearch()
		if self.episodes:
			self._doEpisodeSearch()
		if self.movies:
			self._doMovieSearch()
		if not self.__found:
			self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(284) + '![/B]')
			self.setFocus(self.getControl(199))
		else:
			self.getControl(198).setLabel('')


	def _doMovieSearch(self):
		count = 0
		listitems = []
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + " " + xbmc.getLocalizedString(342).lower() + '[/B]')
		json_response = common.callJSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["title", "streamdetails", "genre", "studio", "year", "tagline", "plot", "plotoutline", "runtime", "fanart", "thumbnail", "file", "playcount", "rating", "mpaa", "director", "writer"], "sort": { "method": "label" }, "filter": {"field":"title","operator":"contains","value":"%s"} }, "id": 1}' % self.searchstring)
		if json_response['result'] != None and json_response['result'].has_key('movies'):
			for item in json_response['result']['movies']:
				count += 1
				movie = item['title']
				director = " / ".join(item['director'])
				writer = " / ".join(item['writer'])
				fanart = item['fanart']
				path = item['file']
				genre = " / ".join(item['genre'])
				mpaa = item['mpaa']
				playcount = str(item['playcount'])
				plot = item['plot']
				outline = item['plotoutline']
				rating = str(round(float(item['rating']), 1))
				runtime = str(int((item['runtime'] / 60.0) + 0.5))
				studio = " / ".join(item['studio'])
				tagline = item['tagline']
				thumb = item['thumbnail']
				year = str(item['year'])
				if item['streamdetails']['audio'] != []:
					audiochannels = str(item['streamdetails']['audio'][0]['channels'])
					audiocodec = str(item['streamdetails']['audio'][0]['codec'])
				else:
					audiochannels = ''
					audiocodec = ''
				if item['streamdetails']['video'] != []:
					videocodec = str(item['streamdetails']['video'][0]['codec'])
					videoaspect = float(item['streamdetails']['video'][0]['aspect'])
					if videoaspect <= 1.4859:
						videoaspect = '1.33'
					elif videoaspect <= 1.7190:
						videoaspect = '1.66'
					elif videoaspect <= 1.8147:
						videoaspect = '1.78'
					elif videoaspect <= 2.0174:
						videoaspect = '1.85'
					elif videoaspect <= 2.2738:
						videoaspect = '2.20'
					else:
						videoaspect = '2.35'
					videowidth = item['streamdetails']['video'][0]['width']
					videoheight = item['streamdetails']['video'][0]['height']
					if videowidth <= 720 and videoheight <= 480:
						videoresolution = '480'
					elif videowidth <= 768 and videoheight <= 576:
						videoresolution = '576'
					elif videowidth <= 960 and videoheight <= 544:
						videoresolution = '540'
					elif videowidth <= 1280 and videoheight <= 720:
						videoresolution = '720'
					else:
						videoresolution = '1080'
				else:
					videocodec = ''
					videoaspect = ''
					videoresolution = ''
				listitem = xbmcgui.ListItem(label=movie, iconImage='DefaultVideo.png', thumbnailImage=thumb)
				listitem.setProperty("icon", thumb)
				listitem.setProperty("fanart", fanart)
				listitem.setProperty("genre", genre)
				listitem.setProperty("plot", plot)
				listitem.setProperty("plotoutline", outline)
				listitem.setProperty("duration", runtime)
				listitem.setProperty("studio", studio)
				listitem.setProperty("tagline", tagline)
				listitem.setProperty("year", year)
				listitem.setProperty("playcount", playcount)
				listitem.setProperty("rating", rating)
				listitem.setProperty("mpaa", mpaa)
				listitem.setProperty("writer", writer)
				listitem.setProperty("director", director)
				listitem.setProperty("videoresolution", videoresolution)
				listitem.setProperty("videocodec", videocodec)
				listitem.setProperty("videoaspect", videoaspect)
				listitem.setProperty("audiocodec", audiocodec)
				listitem.setProperty("audiochannels", audiochannels)
				listitem.setProperty("path", path)
				listitems.append(listitem)
		self.getControl(111).addItems(listitems)
		if count > 0:
			self.getControl(110).setLabel(str(count))
			self.getControl(119).setVisible(True)
			if not self.__found:
				xbmc.sleep(100)
				self.setFocus(self.getControl(111))
				self.__found = True


	def _doActorSearch(self):
		count = 0
		listitems = []
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + " " + xbmc.getLocalizedString(344).lower() + '[/B]')
		json_response = common.callJSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["title", "streamdetails", "genre", "studio", "year", "tagline", "plot", "plotoutline", "runtime", "fanart", "thumbnail", "file", "playcount", "rating", "mpaa", "director", "writer"], "sort": { "method": "label" }, "filter": {"field":"actor","operator":"contains","value":"%s"} }, "id": 1}' % self.searchstring)
		if json_response['result'] != None and json_response['result'].has_key('movies'):
			for item in json_response['result']['movies']:
				count += 1
				movie = item['title']
				director = " / ".join(item['director'])
				writer = " / ".join(item['writer'])
				fanart = item['fanart']
				path = item['file']
				genre = " / ".join(item['genre'])
				mpaa = item['mpaa']
				playcount = str(item['playcount'])
				plot = item['plot']
				outline = item['plotoutline']
				rating = str(round(float(item['rating']), 1))
				runtime = str(int((item['runtime'] / 60.0) + 0.5))
				studio = " / ".join(item['studio'])
				tagline = item['tagline']
				thumb = item['thumbnail']
				year = str(item['year'])
				if item['streamdetails']['audio'] != []:
					audiochannels = str(item['streamdetails']['audio'][0]['channels'])
					audiocodec = str(item['streamdetails']['audio'][0]['codec'])
				else:
					audiochannels = ''
					audiocodec = ''
				if item['streamdetails']['video'] != []:
					videocodec = str(item['streamdetails']['video'][0]['codec'])
					videoaspect = float(item['streamdetails']['video'][0]['aspect'])
					if videoaspect <= 1.4859:
						videoaspect = '1.33'
					elif videoaspect <= 1.7190:
						videoaspect = '1.66'
					elif videoaspect <= 1.8147:
						videoaspect = '1.78'
					elif videoaspect <= 2.0174:
						videoaspect = '1.85'
					elif videoaspect <= 2.2738:
						videoaspect = '2.20'
					else:
						videoaspect = '2.35'
					videowidth = item['streamdetails']['video'][0]['width']
					videoheight = item['streamdetails']['video'][0]['height']
					if videowidth <= 720 and videoheight <= 480:
						videoresolution = '480'
					elif videowidth <= 768 and videoheight <= 576:
						videoresolution = '576'
					elif videowidth <= 960 and videoheight <= 544:
						videoresolution = '540'
					elif videowidth <= 1280 and videoheight <= 720:
						videoresolution = '720'
					else:
						videoresolution = '1080'
				else:
					videocodec = ''
					videoaspect = ''
					videoresolution = ''
				listitem = xbmcgui.ListItem(label=movie, iconImage='DefaultVideo.png', thumbnailImage=thumb)
				listitem.setProperty("icon", thumb)
				listitem.setProperty("fanart", fanart)
				listitem.setProperty("genre", genre)
				listitem.setProperty("plot", plot)
				listitem.setProperty("plotoutline", outline)
				listitem.setProperty("duration", runtime)
				listitem.setProperty("studio", studio)
				listitem.setProperty("tagline", tagline)
				listitem.setProperty("year", year)
				listitem.setProperty("playcount", playcount)
				listitem.setProperty("rating", rating)
				listitem.setProperty("mpaa", mpaa)
				listitem.setProperty("writer", writer)
				listitem.setProperty("director", director)
				listitem.setProperty("videoresolution", videoresolution)
				listitem.setProperty("videocodec", videocodec)
				listitem.setProperty("videoaspect", videoaspect)
				listitem.setProperty("audiocodec", audiocodec)
				listitem.setProperty("audiochannels", audiochannels)
				listitem.setProperty("path", path)
				listitems.append(listitem)
		self.getControl(211).addItems(listitems)
		if count > 0:
			self.getControl(210).setLabel(str(count))
			self.getControl(219).setVisible(True)
			if not self.__found:
				xbmc.sleep(100)
				self.setFocus(self.getControl(211))
				self.__found = True


	def _doTVShowSearch(self):
		count = 0
		listitems = []
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + " " + xbmc.getLocalizedString(20343).lower() + '[/B]')
		json_response = common.callJSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["title", "genre", "studio", "premiered", "plot", "fanart", "thumbnail", "playcount", "year", "mpaa", "episode", "rating", "art"], "sort": { "method": "label" }, "filter": {"field": "title", "operator": "contains", "value": "%s"} }, "id": 1}' % self.searchstring)
		if json_response['result'] != None and json_response['result'].has_key('tvshows'):
			for item in json_response['result']['tvshows']:
				count += 1
				tvshow = item['title']
				episode = str(item['episode'])
				fanart = item['fanart']
				genre = " / ".join(item['genre'])
				mpaa = item['mpaa']
				playcount = str(item['playcount'])
				plot = item['plot']
				premiered = item['premiered']
				rating = str(round(float(item['rating']), 1))
				studio = " / ".join(item['studio'])
				thumb = item['thumbnail']
				banner = item['art'].get('banner', '')
				poster = item['art'].get('poster', '')
				tvshowid = str(item['tvshowid'])
				path = path = 'videodb://tvshows/titles/' + tvshowid + '/'
				year = str(item['year'])
				listitem = xbmcgui.ListItem(label=tvshow, iconImage='DefaultVideo.png', thumbnailImage=thumb)
				listitem.setProperty("icon", thumb)
				listitem.setProperty("art(banner)", banner)
				listitem.setProperty("art(poster)", poster)
				listitem.setProperty("episode", episode)
				listitem.setProperty("mpaa", mpaa)
				listitem.setProperty("year", year)
				listitem.setProperty("fanart", fanart)
				listitem.setProperty("genre", genre)
				listitem.setProperty("plot", plot)
				listitem.setProperty("premiered", premiered)
				listitem.setProperty("studio", studio)
				listitem.setProperty("rating", rating)
				listitem.setProperty("playcount", playcount)
				listitem.setProperty("path", path)
				listitem.setProperty("id", tvshowid)
				listitems.append(listitem)
		self.getControl(121).addItems(listitems)
		if count > 0:
			self.getControl(120).setLabel(str(count))
			self.getControl(129).setVisible(True)
			if not self.__found:
				xbmc.sleep(100)
				self.setFocus(self.getControl(121))
				self.__found = True


	def _getSeasons(self):
		count = 0
		listitems = []
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + " " + xbmc.getLocalizedString(20343).lower() + '[/B]')
		json_response = common.callJSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetSeasons", "params": {"properties": ["showtitle", "season", "fanart", "thumbnail", "playcount", "episode"], "sort": { "method": "label" }, "tvshowid":%s }, "id": 1}' % self.tvshowid)
		if json_response['result'] != None and json_response['result'].has_key('seasons'):
			for item in json_response['result']['seasons']:
				count += 1
				tvshow = item['showtitle']
				episode = str(item['episode'])
				fanart = item['fanart']
				path = 'videodb://tvshows/titles/' + self.tvshowid + '/' + str(item['season']) + '/'
				season = item['label']
				playcount = str(item['playcount'])
				thumb = item['thumbnail']
				listitem = xbmcgui.ListItem(label=season, iconImage='DefaultVideo.png', thumbnailImage=thumb)
				listitem.setProperty("icon", thumb)
				listitem.setProperty("episode", episode)
				listitem.setProperty("fanart", fanart)
				listitem.setProperty("tvshowtitle", tvshow)
				listitem.setProperty("playcount", playcount)
				listitem.setProperty("path", path)
				listitems.append(listitem)
		self.getControl(131).addItems(listitems)
		if count > 0:
			self.foundseasons = 'true'
			self.getControl(130).setLabel(str(count))
			self.getControl(139).setVisible(True)
			if not self.__found:
				xbmc.sleep(100)
				self.setFocus(self.getControl(131))
				self.__found = True


	def _doEpisodeSearch(self):
		count = 0
		listitems = []
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + " " + xbmc.getLocalizedString(20360).lower() + '[/B]')
		json_response = common.callJSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "properties": ["title", "streamdetails", "plot", "firstaired", "runtime", "season", "episode", "showtitle", "thumbnail", "fanart", "file", "playcount", "director", "rating"], "sort": { "method": "title" }, "filter": {"field": "title", "operator": "contains", "value": "%s"} }, "id": 1}' % self.searchstring)
		if json_response['result'] != None and json_response['result'].has_key('episodes'):
			for item in json_response['result']['episodes']:
				count += 1
				episode = item['title']
				tvshowname = item['showtitle']
				director = " / ".join(item['director'])
				fanart = item['fanart']
				episodenumber = "%.2d" % float(item['episode'])
				path = item['file']
				plot = item['plot']
				runtime = str(int((item['runtime'] / 60.0) + 0.5))
				premiered = item['firstaired']
				rating = str(round(float(item['rating']), 1))
				seasonnumber = '%.2d' % float(item['season'])
				playcount = str(item['playcount'])
				thumb = item['thumbnail']
				fanart = item['fanart']
				if item['streamdetails']['audio'] != []:
					audiochannels = str(item['streamdetails']['audio'][0]['channels'])
					audiocodec = str(item['streamdetails']['audio'][0]['codec'])
				else:
					audiochannels = ''
					audiocodec = ''
				if item['streamdetails']['video'] != []:
					videocodec = str(item['streamdetails']['video'][0]['codec'])
					videoaspect = float(item['streamdetails']['video'][0]['aspect'])
					if videoaspect <= 1.4859:
						videoaspect = '1.33'
					elif videoaspect <= 1.7190:
						videoaspect = '1.66'
					elif videoaspect <= 1.8147:
						videoaspect = '1.78'
					elif videoaspect <= 2.0174:
						videoaspect = '1.85'
					elif videoaspect <= 2.2738:
						videoaspect = '2.20'
					else:
						videoaspect = '2.35'
					videowidth = item['streamdetails']['video'][0]['width']
					videoheight = item['streamdetails']['video'][0]['height']
					if videowidth <= 720 and videoheight <= 480:
						videoresolution = '480'
					elif videowidth <= 768 and videoheight <= 576:
						videoresolution = '576'
					elif videowidth <= 960 and videoheight <= 544:
						videoresolution = '540'
					elif videowidth <= 1280 and videoheight <= 720:
						videoresolution = '720'
					else:
						videoresolution = '1080'
				else:
					videocodec = ''
					videoaspect = ''
					videoresolution = ''
				listitem = xbmcgui.ListItem(label=episode, iconImage='DefaultVideo.png', thumbnailImage=thumb)
				listitem.setProperty("icon", thumb)
				listitem.setProperty("episode", episodenumber)
				listitem.setProperty("plot", plot)
				listitem.setProperty("rating", rating)
				listitem.setProperty("director", director)
				listitem.setProperty("fanart", fanart)
				listitem.setProperty("season", seasonnumber)
				listitem.setProperty("duration", runtime)
				listitem.setProperty("tvshowtitle", tvshowname)
				listitem.setProperty("premiered", premiered)
				listitem.setProperty("playcount", playcount)
				listitem.setProperty("videoresolution", videoresolution)
				listitem.setProperty("videocodec", videocodec)
				listitem.setProperty("videoaspect", videoaspect)
				listitem.setProperty("audiocodec", audiocodec)
				listitem.setProperty("audiochannels", audiochannels)
				listitem.setProperty("path", path)
				listitems.append(listitem)
		self.getControl(141).addItems(listitems)
		if count > 0:
			self.getControl(140).setLabel(str(count))
			self.getControl(149).setVisible(True)
			if not self.__found:
				xbmc.sleep(100)
				self.setFocus(self.getControl(141))
				self.__found = True


	def _doMusicvideoSearch(self):
		count = 0
		listitems = []
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + " " + xbmc.getLocalizedString(20389).lower() + '[/B]')
		json_response = common.callJSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMusicVideos", "params": {"properties": ["title", "streamdetails", "runtime", "genre", "studio", "artist", "album", "year", "plot", "fanart", "thumbnail", "file", "playcount", "director"], "sort": { "method": "label" }, "filter": {"field": "title", "operator": "contains", "value": "%s"} }, "id": 1}' % self.searchstring)
		if json_response['result'] != None and json_response['result'].has_key('musicvideos'):
			for item in json_response['result']['musicvideos']:
				count += 1
				musicvideo = item['title']
				album = item['album']
				artist = " / ".join(item['artist'])
				director = " / ".join(item['director'])
				fanart = item['fanart']
				path = item['file']
				genre = " / ".join(item['genre'])
				plot = item['plot']
				studio = " / ".join(item['studio'])
				thumb = item['thumbnail']
				playcount = str(item['playcount'])
				year = str(item['year'])
				if year == '0':
					year = ''
				if item['streamdetails']['audio'] != []:
					audiochannels = str(item['streamdetails']['audio'][0]['channels'])
					audiocodec = str(item['streamdetails']['audio'][0]['codec'])
				else:
					audiochannels = ''
					audiocodec = ''
				if item['streamdetails']['video'] != []:
					videocodec = str(item['streamdetails']['video'][0]['codec'])
					videoaspect = float(item['streamdetails']['video'][0]['aspect'])
					if videoaspect <= 1.4859:
						videoaspect = '1.33'
					elif videoaspect <= 1.7190:
						videoaspect = '1.66'
					elif videoaspect <= 1.8147:
						videoaspect = '1.78'
					elif videoaspect <= 2.0174:
						videoaspect = '1.85'
					elif videoaspect <= 2.2738:
						videoaspect = '2.20'
					else:
						videoaspect = '2.35'
					videowidth = item['streamdetails']['video'][0]['width']
					videoheight = item['streamdetails']['video'][0]['height']
					if videowidth <= 720 and videoheight <= 480:
						videoresolution = '480'
					elif videowidth <= 768 and videoheight <= 576:
						videoresolution = '576'
					elif videowidth <= 960 and videoheight <= 544:
						videoresolution = '540'
					elif videowidth <= 1280 and videoheight <= 720:
						videoresolution = '720'
					else:
						videoresolution = '1080'
					duration = str(datetime.timedelta(seconds=int(item['streamdetails']['video'][0]['duration'])))
					if duration[0] == '0':
						duration = duration[2:]
				else:
					videocodec = ''
					videoaspect = ''
					videoresolution = ''
					duration = ''
				listitem = xbmcgui.ListItem(label=musicvideo, iconImage='DefaultVideo.png', thumbnailImage=thumb)
				listitem.setProperty("icon", thumb)
				listitem.setProperty("album", album)
				listitem.setProperty("artist", artist)
				listitem.setProperty("fanart", fanart)
				listitem.setProperty("director", director)
				listitem.setProperty("genre", genre)
				listitem.setProperty("plot", plot)
				listitem.setProperty("duration", duration)
				listitem.setProperty("studio", studio)
				listitem.setProperty("year", year)
				listitem.setProperty("playcount", playcount)
				listitem.setProperty("videoresolution", videoresolution)
				listitem.setProperty("videocodec", videocodec)
				listitem.setProperty("videoaspect", videoaspect)
				listitem.setProperty("audiocodec", audiocodec)
				listitem.setProperty("audiochannels", audiochannels)
				listitem.setProperty("path", path)
				listitems.append(listitem)
		self.getControl(151).addItems(listitems)
		if count > 0:
			self.getControl(150).setLabel(str(count))
			self.getControl(159).setVisible(True)
			if not self.__found:
				xbmc.sleep(100)
				self.setFocus(self.getControl(151))
				self.__found = True


	def _doArtistSearch(self):
		count = 0
		listitems = []
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + " " + xbmc.getLocalizedString(133).lower() + '[/B]')
		json_response = common.callJSON('{"jsonrpc": "2.0", "method": "AudioLibrary.GetArtists", "params": {"properties": ["genre", "description", "fanart", "thumbnail", "formed", "disbanded", "born", "yearsactive", "died", "mood", "style"], "sort": { "method": "label" }, "filter": {"field": "artist", "operator": "contains", "value": "%s"}, "allroles":true }, "id": 1}' % self.searchstring)
		if json_response['result'] != None and json_response['result'].has_key('artists'):
			for item in json_response['result']['artists']:
				count += 1
				artist = item['label']
				artistid = str(item['artistid'])
				path = 'musicdb://artists/' + artistid + '/'
				born = item['born']
				description = item['description']
				died = item['died']
				disbanded = item['disbanded']
				fanart = item['fanart']
				formed = item['formed']
				genre = " / ".join(item['genre'])
				mood = " / ".join(item['mood'])
				style = " / ".join(item['style'])
				thumb = item['thumbnail']
				yearsactive = " / ".join(item['yearsactive'])
				listitem = xbmcgui.ListItem(label=artist, iconImage='DefaultArtist.png', thumbnailImage=thumb)
				listitem.setProperty("icon", thumb)
				listitem.setProperty("artist_born", born)
				listitem.setProperty("artist_died", died)
				listitem.setProperty("artist_formed", formed)
				listitem.setProperty("artist_disbanded", disbanded)
				listitem.setProperty("artist_yearsactive", yearsactive)
				listitem.setProperty("artist_mood", mood)
				listitem.setProperty("artist_style", style)
				listitem.setProperty("fanart", fanart)
				listitem.setProperty("artist_genre", genre)
				listitem.setProperty("artist_description", description)
				listitem.setProperty("path", path)
				listitem.setProperty("id", artistid)
				listitems.append(listitem)
		self.getControl(161).addItems(listitems)
		if count > 0:
			self.getControl(160).setLabel(str(count))
			self.getControl(169).setVisible(True)
			if not self.__found:
				xbmc.sleep(100)
				self.setFocus(self.getControl(161))
				self.__found = True


	def _doAlbumSearch(self):
		count = 0
		listitems = []
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + " " + xbmc.getLocalizedString(132).lower() + '[/B]')
		json_response = common.callJSON('{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": {"properties": ["title", "description", "albumlabel", "artist", "genre", "year", "thumbnail", "fanart", "theme", "type", "mood", "style", "rating"], "sort": { "method": "label" }, "filter": {"field": "album", "operator": "contains", "value": "%s"}, "allroles":true }, "id": 1}' % self.searchstring)
		if json_response['result'] != None and json_response['result'].has_key('albums'):
			for item in json_response['result']['albums']:
				count += 1
				album = item['title']
				artist = " / ".join(item['artist'])
				albumid = str(item['albumid'])
				path = 'musicdb://albums/' + albumid + '/'
				label = item['albumlabel']
				description = item['description']
				fanart = item['fanart']
				genre = " / ".join(item['genre'])
				mood = " / ".join(item['mood'])
				rating = str(item['rating'])
				if rating == '48':
					rating = ''
				style = " / ".join(item['style'])
				theme = " / ".join(item['theme'])
				albumtype = item['type']
				thumb = item['thumbnail']
				year = str(item['year'])
				listitem = xbmcgui.ListItem(label=album, iconImage='DefaultAlbumCover.png', thumbnailImage=thumb)
				listitem.setProperty("icon", thumb)
				listitem.setProperty("artist", artist)
				listitem.setProperty("album_label", label)
				listitem.setProperty("genre", genre)
				listitem.setProperty("fanart", fanart)
				listitem.setProperty("album_description", description)
				listitem.setProperty("album_theme", theme)
				listitem.setProperty("album_style", style)
				listitem.setProperty("album_rating", rating)
				listitem.setProperty("album_type", albumtype)
				listitem.setProperty("album_mood", mood)
				listitem.setProperty("year", year)
				listitem.setProperty("path", path)
				listitem.setProperty("id", albumid)
				listitems.append(listitem)
		self.getControl(171).addItems(listitems)
		if count > 0:
			self.getControl(170).setLabel(str(count))
			self.getControl(179).setVisible(True)
			if not self.__found:
				xbmc.sleep(100)
				self.setFocus(self.getControl(171))
				self.__found = True


	def _doSongSearch(self):
		count = 0
		listitems = []
		self.getControl(198).setLabel('[B]' + xbmc.getLocalizedString(194) + " " + xbmc.getLocalizedString(134).lower() + '[/B]')
		json_response = common.callJSON('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": {"properties": ["title", "artist", "album", "genre", "duration", "year", "file", "thumbnail", "fanart", "comment", "rating", "track", "playcount"], "sort": { "method": "title" }, "filter": {"field": "title", "operator": "contains", "value": "%s"}, "allroles":true }, "id": 1}' % self.searchstring)
		if json_response['result'] != None and json_response['result'].has_key('songs'):
			for item in json_response['result']['songs']:
				count += 1
				song = item['title']
				artist = " / ".join(item['artist'])
				album = item['album']
				comment = item['comment']
				duration = str(datetime.timedelta(seconds=int(item['duration'])))
				if duration[0] == '0':
					duration = duration[2:]
				fanart = item['fanart']
				path = item['file']
				genre = " / ".join(item['genre'])
				thumb = item['thumbnail']
				track = str(item['track'])
				playcount = str(item['playcount'])
				rating = str(int(item['rating']) - 48)
				year = str(item['year'])
				listitem = xbmcgui.ListItem(label=song, iconImage='DefaultAlbumCover.png', thumbnailImage=thumb)
				listitem.setProperty("icon", thumb)
				listitem.setProperty("artist", artist)
				listitem.setProperty("album", album)
				listitem.setProperty("genre", genre)
				listitem.setProperty("comment", comment)
				listitem.setProperty("track", track)
				listitem.setProperty("rating", rating)
				listitem.setProperty("playcount", playcount)
				listitem.setProperty("duration", duration)
				listitem.setProperty("fanart", fanart)
				listitem.setProperty("year", year)
				listitem.setProperty("path", path)
				listitems.append(listitem)
		self.getControl(181).addItems(listitems)
		if count > 0:
			self.getControl(180).setLabel(str(count))
			self.getControl(189).setVisible(True)
			if not self.__found:
				xbmc.sleep(100)
				self.setFocus(self.getControl(181))
				self.__found = True


	def _playVideo(self, path):
		self._close()
		xbmc.Player().play(path)


	def _playAudio(self, path, listitem):
		self._close()
		xbmc.Player().play(path, listitem)


	def _playAlbum(self):
		self._close()
		common.callJSON('{ "jsonrpc": "2.0", "method": "Player.Open", "params": { "item": { "albumid": %d } }, "id": 1 }' % int(self.albumid))


	def _browseVideo(self, path):
		self._close()
		xbmc.executebuiltin('ActivateWindow(Videos,' + path + ',return)')


	def _browseAudio(self, path):
		self._close()
		xbmc.executebuiltin('ActivateWindow(Music,' + path + ',return)')


	def onClick(self, controlId):
		if controlId == 111:
			listitem = self.getControl(111).getSelectedItem()
			path = listitem.getProperty('path')
			self._playVideo(path)
		elif controlId == 121:
			listitem = self.getControl(121).getSelectedItem()
			path = listitem.getProperty('path')
			self._browseVideo(path)
		elif controlId == 131:
			listitem = self.getControl(131).getSelectedItem()
			path = listitem.getProperty('path')
			self._browseVideo(path)
		elif controlId == 141:
			listitem = self.getControl(141).getSelectedItem()
			path = listitem.getProperty('path')
			self._playVideo(path)
		elif controlId == 151:
			listitem = self.getControl(151).getSelectedItem()
			path = listitem.getProperty('path')
			self._playVideo(path)
		elif controlId == 161:
			listitem = self.getControl(161).getSelectedItem()
			path = listitem.getProperty('path')
			self._browseAudio(path)
		elif controlId == 171:
			listitem = self.getControl(171).getSelectedItem()
			self.albumid = listitem.getProperty('id')
			self._playAlbum()
		elif controlId == 181:
			listitem = self.getControl(181).getSelectedItem()
			path = listitem.getProperty('path')
			self._playAudio(path, listitem)
		if controlId == 211:
			listitem = self.getControl(211).getSelectedItem()
			path = listitem.getProperty('path')
			self._playVideo(path)
		elif controlId == 199:
			self._runNewSearch()


	def onAction(self, action):
		if action.getId() in (9, 10, 92, 216, 247, 257, 275, 61467, 61448):
			self._close()


	def show(self):
		self.doModal()


	def _close(self):
		self.close()
		xbmc.sleep(300)
		xbmcgui.Window(self.__winid).clearProperty('GlobalSearch.SearchString')
		common.debug('%s v%s has been terminated' % (common.AddonName(), common.AddonVersion()))
