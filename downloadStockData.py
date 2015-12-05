# -*- coding: utf-8 -*-

# need repair
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import urllib.request
from bs4 import BeautifulSoup

import os
import datetime

from time import sleep

def makeDataFolder():
	if os.path.isdir("datafolder") is False:
		os.mkdir("datafolder")
	createDatafile()
	os.chdir("datafolder")

def createDatafile():
	strToday = "{0:%Y%m%d}".format(datetime.datetime.today())
	strTodayPath = "datafolder/datafile" + strToday
	dataFile = open(strTodayPath, "w")
	dataFile.close()

def getStockData(stockNo):
	datarow = "stockNo=" + stockNo + ":"
	html = ""

	site = urllib.request.urlopen("http://stocks.finance.yahoo.co.jp/stocks/detail/?code=" + stockNo + ".T")
	charset = site.info().get('content-type').split('=')[1]
	for sline in site.readlines():
		html = html + sline.decode(charset)
	soup = BeautifulSoup(html)

	td1 = soup.table.tr.td
	td2 = td1.next_sibling.next_sibling
	datarow = datarow + "stoksprice=" + td2.string + ":" 

	lineFiclearfixs = soup.find_all("div", {"class":"lineFi clearfix"})
	for lineFiclearfix in lineFiclearfixs:
		# Get Value
		stronglineFi = lineFiclearfix.find("strong")
		if stronglineFi.find("a") is None:
			value = stronglineFi.string
		else:
			ddString = stronglineFi.find("dd").string
			value = stronglineFi.find("a").string + ddString
		# Get id value of class="tips yjSt"
		idvalue = lineFiclearfix.find("span", {"class":"tips yjSt"}).get("id")
		# add taple of the value and id to the list for return value
		
		if idvalue == "nehabaseigen":
			continue	
		datarow = datarow + idvalue + "=" + value + ":"

	lineFiyjMSclearfixs = soup.find_all("div", {"class":"lineFi yjMS clearfix"})
	for lineFiyjMSclearfix in lineFiyjMSclearfixs:
		# Get Value
		stronglineFiyjMS = lineFiyjMSclearfix.find("strong")
		ddString = ''
		if stronglineFiyjMS.find("a") is None:
			value = stronglineFiyjMS.string # + ddString
		else:
			value = stronglineFiyjMS.find("a").string  # + ddString
		# Get id value of class="tips yjSt"
		idvalue = lineFiyjMSclearfix.find("span", {"class":"tips yjSt"}).get("id")
		if idvalue == "shinyoubaizann" or idvalue =="shinyoubaizann_zensyuuhi" or idvalue == "shinyouuriage" or idvalue == "saiteikounyuudaikin" or idvalue == "nenshoraitakane" or idvalue == "nensyoraiyasune" or idvalue == "shinyouuriage_zensyuuhi":
			continue	

		datarow = datarow + idvalue + "=" + value + ":"
	
	strToday = "{0:%Y%m%d}".format(datetime.datetime.today())
	strTodayPath = "datafile" + strToday
	dataFile = open(strTodayPath, "a")
	dataFile.writelines(datarow + "\n")
	dataFile.close()

import smtplib
from email.mime.text import MIMEText
from email.header import Header
utf8 = 'utf-8'

def sendresultmail(title, contents):
	smtp = smtplib.SMTP('smtp.mail.yahoo.co.jp',25)
	smtp.login('yumedamail@yahoo.co.jp','zaq1xsw2')
	msg = MIMEText(contents, 'plain', utf8)
	msg['Subject'] = str(Header(title, utf8))
	smtp.sendmail('yumedamail@yahoo.co.jp','umeda.yasushi@nidec.com',msg.as_string())
	smtp.close()

def getDiskUsage(path):
	s = os.statvfs(path)
	avail = s.f_bsize * s.f_bavail
	total = s.f_bsize * s.f_blocks
	return avail / total * 100

if __name__ == '__main__':
	mailtitle = u""
	mailcontents = u""
	# download stock data
	stockNolistFile = open("stockNolist","r")
	try:
		line = stockNolistFile.readline()
		makeDataFolder()
		while line !="":
			stockNo = line.split(",")[0]
			getStockData(stockNo)
			sleep(0.3)
			line = stockNolistFile.readline()
		#send mail success result and disk usage
		mailtitle = u'batch process success'
		mailcontents = u'the batch process succeed. disk remain usage:' & getDiskUsage('.')
	except Exception:
	#send mail failed result
		mailtitle = u'batch process fail'
		mailcontents = u'the batch process failed. Please check again'
	finally:
		stockNolistFile.close()
		sendresultmail(mailtitle, mailcontents)
