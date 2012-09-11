###############################################################################


USTREAM_KEY 	= '8C8687A40DFFF62C23AAE5E021BD2BFE'
USTREAM_URL 	= 'http://www.ustream.tv'

ICON 			= 'icon-default.png'
ART 			= 'art-default.jpg'
SEARCH 			= 'search-default.png'


####################################################################################################
def Start():

	Plugin.AddPrefixHandler('/video/ustream', MainMenu, 'USTREAM', ICON, ART)
	Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = 'USTREAM'
	DirectoryObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:12.0) Gecko/20100101 Firefox/12.0'
	HTTP.Headers['Referer'] = 'http://www.ustream.tv'


####################################################################################################
def MainMenu():

	oc = ObjectContainer()
	html = HTML.ElementFromURL(USTREAM_URL)

	for cat in html.xpath('//ul[@class="categories"]/li[contains(@class,"cat")]'):
		title = L(cat.xpath('.//a/span')[0].text.strip())
		discoveryPath = cat.xpath('.//div[@class="subNav"]')[0].get('data-discovery')
		if discoveryPath is None:
			discoveryPath = cat.xpath('.//a')[0].get('href')
		url = USTREAM_URL + discoveryPath + '?page=%s'
		oc.add(DirectoryObject(key=Callback(GetVideos, title=title, url=url),title=title))

	oc.add(SearchDirectoryObject(identifier="com.plexapp.plugins.ustream", title="Search for Live Channels", prompt="Search USTREAM for...", thumb=R(SEARCH), art=R(ART)))

	return oc

####################################################################################################
def ListSubcats(catclass):
	# Not used at the moment...

	Log('catclass is --> ' + catclass)

	oc = ObjectContainer()
	html = HTML.ElementFromURL(USTREAM_URL)

	cat = html.xpath('//li[@class="' + catclass + '"]')[0]
	Log(HTML.StringFromElement(cat))
	for subcat in cat.xpath('.//div[@class="subNav"]'):
		Log('Subcat --->' + HTML.StringFromElement(subcat))
		title = subcat.text
		catUrl = subcat.get('href')
		oc.add(DirectoryObject(key=Callback(GetVideos, title=title, url=catUrl)),title=L(title))

	return oc

####################################################################################################
def GetVideos(title, url, page=1, cacheTime=CACHE_1HOUR):

	oc = ObjectContainer(title2='%s - %d' % (title, page), view_group='InfoList')


	html = HTML.ElementFromURL(url % page, cacheTime=cacheTime)

	for video in html.xpath('//ul[contains(@class,"recordedShowThumbsV4")]/li'):
		thumbUrl = video.xpath('.//a/span[@class="img"]/img')[0].get('src')
		if 'images/blank' in thumbUrl:
			thumbUrl = video.xpath('.//a/span[@class="img"]/img')[0].get('rel')
		oc.add(VideoClipObject(
			url=USTREAM_URL + video.xpath('.//a')[0].get('href'),
			title=video.xpath('.//h4/a')[0].text.strip() + ' (' + video.xpath('.//a[@class="username"]')[0].text.strip() + ')',
			summary='',
			duration=0,
			thumb=Resource.ContentsOfURLWithFallback(thumbUrl, fallback='icon-default.png')
		))

	oc.add(DirectoryObject(
		key = Callback(GetVideos, title=title, url=url, page=page+1, cacheTime=cacheTime),
		title = L('More...')
	))

	return oc
