# -*- coding: utf-8 -*-

import sys
import urllib
import commons
from searcher import GlobalSearchDialog

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
		keyboard = xbmc.Keyboard('', commons.translate(32101), False)
		keyboard.doModal()
		if keyboard.isConfirmed():
			searchstring = keyboard.getText()

	if searchstring:
		search = GlobalSearchDialog("GlobalSearchDialog.xml", commons.AddonPath(), searchstring=searchstring)
		search.show()
		del search
