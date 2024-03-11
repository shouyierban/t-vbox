#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
import math
import re

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
			"全部": "tall"
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
		url = 'https://supjav.com/zh/tag/{0}/page/{1}'.format(tid, pg)
		rsp = self.fetch(url)

		content = self.html(rsp.text)
		aList = content.xpath("//div[@class='post']")
		pgc = math.ceil(numvL/24)
		videos = []
		for a in aList:
			name = a.xpath('./a/@title')[0]
			pic = a.xpath('./a/img/@src')[0]
			mark = a.xpath(".//h3")[0]
			sid = a.xpath("./a/@href")[0]
			sid = self.regStr(sid,"/zh/(\\S+).html")
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
		url = "https://supjav.com/zh/{0}.html".format(aid)
		rsp = self.fetch(url)
		root = self.html(rsp.text)
		node = root.xpath("//div[@class='post-meta clearfix']")[0]
		
		pic = node.xpath("./img/@src")[0]
		title = node.xpath('./img/@alt')[0]
		detail = node.xpath(".div[@class='cats']/p[1]")[0]
		remarks = node.xpath("./div[@class='cats']/p[2]/a")[0]

		vod = {
			"vod_id":tid,
			"vod_name":title,
			"vod_pic":pic,
			"type_name":"",
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":remarks,
			"vod_actor":"",
			"vod_director":"",
			"vod_content":"detail"
		}
		
		vod['vod_play_from'] = 'tv'
		
		vod['vod_play_url'] = "https://ss394.asongu.com/stream/"
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
			'authority': 'ss394.asongu.com',
			'accept': '*/*',
			'accept-language': 'zh-CN,zh;q=0.9',
			'cache-control': 'no-cache',
			'origin': 'https://emturbovid.com',
			'pragma': 'no-cache',
			'referer': 'https://emturbovid.com/',
			'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
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