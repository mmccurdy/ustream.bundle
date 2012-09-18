####################################################################################################

USTREAM_URL 	= 'http://www.ustream.tv'
DISCOVERY_URL	= USTREAM_URL + '/discovery/live/'
CATEGORIES		= [ 
					{ 'title' :  'On Air', 'path' : 'all'},
					{ 'title' :  'News', 'path' : 'news'},
					{ 'title' :  'Pets & Animals', 'path' : 'animals'},
					{ 'title' :  'Entertainment', 'path' : 'entertainment'},
					{ 'title' :  'Sports', 'path' : 'sports'},
					{ 'title' :  'Music', 'path' : 'music'},
					{ 'title' :  'Gaming', 'path' : 'gaming'},
					{ 'title' :  'Events', 'path' : 'events'},
					{ 'title' :  'Tech', 'path' : 'technology'}
				  ]
				  
ICON 			= 'icon-default.png'
ART 			= 'art-default.jpg'
SEARCH 			= 'icon-search.png'

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

	discoveryCats=[]
	for cat in html.xpath('//ul[@class="categories"]/li[contains(@class,"cat")]'):
		title = cat.xpath('.//a/span')[0].text.strip()
		try:
			discoveryPath = cat.xpath('.//div[@class="subNav"]')[0].get('data-discovery')
			if discoveryPath is None:
				try:		
					discoveryPath = cat.xpath('.//a')[0].get('href')
				except:
					pass
			url = USTREAM_URL + discoveryPath + '?page=%s'
			discoveryCats.append({'title' : title, 'url':url})
		except:
			pass
	# Use a hard-coded cat list for non-US and other sites that use a slightly different nav
	# since obtaining these otherwise would be a second page load per category.
	if len(discoveryCats) < 3:
		discoveryCats = []
		for cat in CATEGORIES:
			discoveryCats.append({ 'title' : cat['title'] , 'url' : DISCOVERY_URL + cat['path'] + '?page=%s' })
	for cat in discoveryCats:
		oc.add(DirectoryObject(key=Callback(GetVideos, title=cat['title'], url=cat['url']), title=cat['title']))

	oc.add(SearchDirectoryObject(
		identifier="com.plexapp.plugins.ustream",
		title="Search for Live Channels",
		prompt="Search USTREAM for...",
		thumb=R(SEARCH),
		art=R(ART)
	))

	return oc

####################################################################################################
def GetVideos(title, url, page=1, cacheTime=CACHE_1HOUR):

	oc = ObjectContainer(title2='%s - %d' % (title, page), view_group='InfoList')

	html = HTML.ElementFromURL(url % page, cacheTime=cacheTime)

	for video in html.xpath('//ul[contains(@class,"recordedShowThumbsV4")]/li'):
		thumbUrl = video.xpath('.//a/span[@class="img"]/img')[0].get('src')
		if 'images/blank' in thumbUrl:
			try:
				thumbUrl = video.xpath('.//img')[0].get('src')
				if thumbUrl.startswith('data:image'):
					thumbUrl = video.xpath('.//img')[0].get('data-lazyload')
				elif 'images/blank' in thumbUrl:
					thumbUrl = video.xpath('.//a/span[@class="img"]/img')[0].get('rel')
			except:
				thumbUrl = None
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
