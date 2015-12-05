# -*- coding: utf-8 -*-

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages')

import urllib.request
from bs4 import BeautifulSoup


fileStockNolist = open("stockNolist","w")


sitelist = ('1000','2000','3000','4000','5000','6000','7000','8000','9000')

for siteNo in sitelist:
	site = urllib.request.urlopen("http://otamesix.com/meigara/code" + siteNo + ".html")
	html = ""
	charset = 'UTF-8' #site.info().get('content-type').split('=')[1]
	for sline in site.readlines():
		html = html + sline.decode(charset)
	soup = BeautifulSoup(html)

	datatable = soup.find("table", {"class":"dsc1item"})
	for tr in datatable.find_all("tr"):
		stockNo = tr.find("th").string
		companyName = tr.find_all("td")[0].string
		companyType = tr.find_all("td")[1].string
		# print("***************************")
		# print(stockNo)
		# print(companyName)
		# print(companyType)
		fileStockNolist.writelines(stockNo + "," + companyName + "," + companyType + "\n")

fileStockNolist.close()

