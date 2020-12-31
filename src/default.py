# -*- coding: utf-8 -*-

import sys
import urllib
import common
from searcher import GlobalSearch

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc


if __name__ == "__main__":
	searchstring = None

	try:
		params = dict(arg.split("=") for arg in sys.argv[1].split("&"))
		searchstring = params.get("searchstring")
		searchstring = urllib.unquote_plus(searchstring)
	except:
		keyboard = xbmc.Keyboard('', common.translate(32101), False)
		keyboard.doModal()
		if keyboard.isConfirmed():
			searchstring = keyboard.getText()

	if searchstring:
		search = GlobalSearch("GlobalSearch.xml", common.AddonPath(), searchstring=searchstring)
		search.show()
		del search
