# -*- coding: utf-8 -*-

import sys
import common
from searcher import GlobalSearch

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc


if __name__ == "__main__":
	searchstring = None

	if len(sys.argv) > 1:
		params = dict(arg.split("=") for arg in sys.argv[1].split("&"))
		if searchstring is not None and searchstring != '':
			searchstring = params.get("searchstring")
			searchstring = common.urlunquote(searchstring)

	if searchstring is None or searchstring == '':
		# close busydialog - if is open and running
		common.runBuiltinCommand("Dialog.Close(busydialog)")
		# get search string from input
		keyboard = xbmc.Keyboard('', common.translate(32101), False)
		keyboard.doModal()
		if keyboard.isConfirmed():
			searchstring = keyboard.getText()

	if searchstring is not None and searchstring != '':
		search = GlobalSearch("GlobalSearch.xml", common.AddonPath(), searchstring=searchstring)
		search.show()
		del search
