###############################################################################


USTREAM_KEY 	= '8C8687A40DFFF62C23AAE5E021BD2BFE'
USTREAM_URL 	= 'http://www.ustream.tv'

ICON 			= 'icon-default.png'
ART 			= 'art-default.jpg'


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
		Log('pachewy chomp ---> ' + HTML.StringFromElement(cat)) 
		title = L(cat.xpath('.//a/span')[0].text.strip())
		discoveryPath = cat.xpath('.//div[@class="subNav"]')[0].get('data-discovery')
		if discoveryPath is None:
			discoveryPath = cat.xpath('.//a')[0].get('href')

		Log('discopath -->' + discoveryPath)

		url = USTREAM_URL + discoveryPath + '?page=%s'
		oc.add(DirectoryObject(key=Callback(GetVideos, title=title, url=url),title=title))

	#	oc.add(DirectoryObject(key=Callback(ListSubcats, catclass=cat.get('class')),title=L(cat.xpath('.//a/span')[0].text.strip())))

	# 	view_group = 'InfoList',
	# 	objects = [
	# 		DirectoryObject(
	# 			key		= Callback(GetVideos, title=L('All Live Channels'), url=USTREAM_URL + '/discovery/live/all?page=%s'),
	# 			title	= L('Live Channels')
	# 		),
	# 		DirectoryObject(
	# 			key		= Callback(GetVideos, title=L('Pets & Animals'), url=USTREAM_URL + '/discovery/live/animals?page=%s'),
	# 			title	= L('Pets & Animals')
	# 		),
	# 		DirectoryObject(
	# 			key		= Callback(GetVideos, title=L('Entertainment'), url=USTREAM_URL + '/discovery/live/entertainment?page=%s'),
	# 			title	= L('Entertainment')
	# 		),



	# 		# sports
	# 		# music
	# 		# technology (Tech)
	# 		# gaming
	# 		# how-to (Education)

	# 		DirectoryObject(
	# 			key		= Callback(ListMore, title=L('Events')),
	# 			title	= L('Events...')
	# 		),
	# 		DirectoryObject(
	# 			key		= Callback(ListMore, title=L('24/7')),
	# 			title	= L('24/7...')
	# 		)

	# 		# PrefsObject(
	# 		# 	title	= L('Preferences...'),
	# 		# 	thumb	= R('icon-prefs.png')
	# 		# )
	# 	]
	# )
	

	# o = JSON.ObjectFromURL(url='http://www.ustream.tv/ajax/new/explore/all.json')
	# Log(JSON.StringFromObject(o))

	return oc

def ListSubcats(catclass):

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
# def ListMore(title):

# 	if 'Events':
# 		oc = ObjectContainer(
# 			view_group = 'InfoList',
# 			objects = [
# 				DirectoryObject(
# 					key		= Callback(GetVideos, title=L('Conference'), url=USTREAM_URL + '/discovery/live/events-conference?page=%s'),
# 					title	= L('Conference')
# 				),
# 				DirectoryObject(
# 					key		= Callback(GetVideos, title=L('Family'), url=USTREAM_URL + '/discovery/live/events-family?page=%s'),
# 					title	= L('Family')
# 				),
# 				DirectoryObject(
# 					key		= Callback(GetVideos, title=L('Politics'), url=USTREAM_URL + '/discovery/live/events-politics?page=%s'),
# 					title	= L('Conference')
# 				),
# 				DirectoryObject(
# 					key		= Callback(GetVideos, title=L('Family'), url=USTREAM_URL + '/discovery/live/events-family?page=%s'),
# 					title	= L('Conference')
# 				),
# 				DirectoryObject(
# 					key		= Callback(GetVideos, title=L('Conference'), url=USTREAM_URL + '/discovery/live/events-conference?page=%s'),
# 					title	= L('Conference')
# 				),
# 				DirectoryObject(
# 					key		= Callback(GetVideos, title=L('Conference'), url=USTREAM_URL + '/discovery/live/events-conference?page=%s'),
# 					title	= L('Conference')
# 				),
# 				DirectoryObject(
# 					key		= Callback(GetVideos, title=L('Conference'), url=USTREAM_URL + '/discovery/live/events-conference?page=%s'),
# 					title	= L('Conference')
# 				),
# 				DirectoryObject(
# 					key		= Callback(GetVideos, title=L('Conference'), url=USTREAM_URL + '/discovery/live/events-conference?page=%s'),
# 					title	= L('Conference')
# 				),
# 				DirectoryObject(
# 					key		= Callback(GetVideos, title=L('Conference'), url=USTREAM_URL + '/discovery/live/events-conference?page=%s'),
# 					title	= L('Conference')
# 				)
# 			]
# 		)

			# More -> 
			# events-conference
			# events-family
			# events-politics
			# events-sports
			# events-music
			# events-holiday
			# events-performing-arts
			# events-citizen-journalist
			# events-other



	# elif title = '24/7':
	# 	oc = ObjectContainer(
	# 		view_group = 'InfoList',
	# 		objects = [
	# 			DirectoryObject(
	# 				key		= Callback(GetVideos, title=L('Conference'), url=USTREAM_URL + '/discovery/live/events-conference?page=%s'),
	# 				title	= L('Conference')
	# 			)


	# 		# 24-7-broadcasts-traffic
	# 		# -animals
	# 		# -security
	# 		# -nature
	# 		# -lifecasting
	# 		# -business
	# 		# -other
	# 	]
	# )
	# return oc

####################################################################################################
def GetVideos(title, url, page=1, cacheTime=CACHE_1HOUR):

	oc = ObjectContainer(title2='%s - %d' % (title, page), view_group='InfoList')


	html = HTML.ElementFromURL(url % page, cacheTime=cacheTime)

	for video in html.xpath('//ul[contains(@class,"recordedShowThumbsV4")]/li'):
		# oc.add(URLService.MetadataObjectForURL(USTREAM_URL + video.get('href')))

		thumbUrl = video.xpath('.//a/span[@class="img"]/img')[0].get('src')
		if 'images/blank' in thumbUrl:
			Log('we got a blank one')
			thumbUrl = video.xpath('.//a/span[@class="img"]/img')[0].get('rel')

		Log('using thumb URL --->' + video.xpath('.//a/span[@class="img"]/img')[0].get('src')) 
		oc.add(VideoClipObject(
			url=USTREAM_URL + video.xpath('.//a')[0].get('href'),
			title=video.xpath('.//h4/a')[0].text + '(' + video.xpath('.//a[@class="username"]')[0].text.strip() + ')',
			summary='',
			duration=0,
			thumb=Resource.ContentsOfURLWithFallback(thumbUrl, fallback='icon-default.png')
		))


	# JSON approach (valid URL's seem to be giving 404's for some reason...)
	
	# json = JSON.ObjectFromURL(url % page)
	# data = HTML.ElementFromURL(json.data)

	# for video in html.xpath('//li'):
	# 	oc.add(VideoClipObject(
	# 		url=USTREAM_URL + '/' + video.xpath('.').get('data-mediaType') + '/' + video.xpath('.').get('data-mediaId'),
	# 		title=video.xpath('.//div[@class="titleOwner"]/h3')[0].text,
	# 		summary='',
	# 		duration='',
	# 		thumb=video.xpath('.//div[@class="img"]/img')[0].get('src')
	# 	))



###### VIMEO STUFF BELOW HERE #######

		# if len(video.xpath('.//div[contains(@class, "private")]')) > 0 or len(video.xpath('.//span[@class="processing"]')) > 0:
		# 	continue

		# video_id = video.xpath('.//a')[0].get('href').rsplit('/',1)[1]
		# video_title = video.xpath('.//p[@class="title"]/a/text()')[0].strip()
		# video_summary = video.xpath('.//p[@class="description"]/text()')[0].strip()
		# video_duration = TimeToMs(video.xpath('.//div[@class="duration"]/text()')[0])
		# video_thumb = video.xpath('.//img')[0].get('src').replace('_150.jpg', '_640.jpg')

		# oc.add(VideoClipObject(
		# 	url = '%s/%s' % (VIMEO_URL, video_id),
		# 	title = video_title,
		# 	summary = video_summary,
		# 	duration = video_duration,
		# 	thumb = Resource.ContentsOfURLWithFallback(video_thumb, fallback='icon-default.png')
		# ))

#	if len(html.xpath('//a[@rel="next"]')) > 0:
	oc.add(DirectoryObject(
		key = Callback(GetVideos, title=title, url=url, page=page+1, cacheTime=cacheTime),
		title = L('More...')
	))

	return oc
