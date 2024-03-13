#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
import math
import re
# import urllib

class Spider(Spider):
	def getName(self):
		return "super"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"高妹": "高妹",
			"东京": "东京"
			
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name': k,
				'type_id': cateManual[k]
			})

		result['class'] = classes
		if (filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		if tid == "高妹":
			url = 'https://cors.notesnook.com/https://missav.com/search/%E9%AB%98%E5%A6%B9?sort=released_at&page={1}'.format(pg)
		else:
			url = 'https://cors.notesnook.com/https://missav.com/dm16/tokyohot?sort=released_at&page={1}'.format(pg)
		rsp = self.fetch(url)
		content = self.html(rsp.text)
		aList = content.xpath("//div[contains(@class,"aspect-w-16")]")
		pgc = math.ceil(numvL/12)
		videos = []
		for a in aList:
			name = a.xpath('./a/img/@alt')[0]
			pic = a.xpath('./a/img/@src')[0]
			# mark = a.xpath(".//h3")[0]
			sid = a.xpath("./a/@href")[0]
			sid = self.regStr(sid,"com/(\\S+)")
			videos.append({
				"vod_id":sid,
				"vod_name":name,
				"vod_pic":pic,
				"vod_remarks":"未知"
			})

		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = pgc
		result['limit'] = numvL
		result['total'] = numvL
		return result

	def detailContent(self,array):
		aid = array[0]
		url = "https://cors.notesnook.com/https://missav.com/{0}".format(aid)
		rsp = self.fetch(url)
		root = self.html(rsp.text)

		# pic = node.xpath("./img/@src")[0]
		title = root.xpath('//div[@class="mt-4"]/h1')[0]
		actor = root.xpath('//div[@class="space-y-2"]//div[4]/a')[0]
		# detail = node.xpath(".div[@class='cats']/p[1]")[0]
		# remarks = node.xpath("./div[@class='cats']/p[2]/a")[0]

		vod = {
			"vod_id":aid,
			"vod_name":title,
			"vod_pic":"",
			"type_name":"",
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":actor,
			"vod_director":"",
			"vod_content":""
		}
		
		vod['vod_play_from'] = 'miss'
		
		scripts = root.xpath("//script/text()")
		
		jo = ''
		for script in scripts:
			jo += str(script)
		code_data = self.regStr(jo,r'm3u8\|(.*?)\|com')
		rate_data = self.regStr(jo,r'video\|(.*?)\|source')
		if code_data and rate_data:
			code_text = code_data.group(1)
			code_text = code_text.replace('|', '-')
			code_list = code_text.split('-')
			code_list.reverse()
			f_code = '-'.join(code_list)
			f_rate = rate_data.group(1)
		
		vod['vod_play_url'] = 'https://surrit.com/' + f_code + '/' + f_rate + '/video.m3u8'
		result = {
			'list': [
				vod
			]
		}
		return result

	def searchContent(self,key,quick):
		result = {}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		url = id
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
		}
		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = header
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		action = {
			'url':'',
			'header':'',
			'param':'',
			'type':'string',
			'after':''
		}
		return [200, "video/MP2T", action, ""]