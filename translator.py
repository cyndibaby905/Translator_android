import sys
from xml.etree import ElementTree as ET
import sys
import os
import codecs
import urllib2
import json

def getPage(words,src,dest):
	url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22" + words +"%22%20and%20target%3D%22" + dest + "%22%20and%20source%3D%22" + src +"%22%3B&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
	headers = { 'User-Agent' : 'Mozilla/5.0' }
	req = urllib2.Request(url, None, headers)
	response = urllib2.urlopen(req)
	return response.read()

def parseJsonResult(resultStr):
	result = json.loads(resultStr)
	resultArray = result['query']['results']['json']['json'][0]['json']
	str=""
	if type(resultArray) is dict:
		str+=resultArray['json'][0]
	else:
		for subDict in resultArray:
			str+=subDict['json'][0]	
	return str

if __name__ == '__main__':
	fileName = "strings.xml"
	destLanguage = "zh"
	srcLanguage = "en"
	if len(sys.argv) >= 4:
		fileName = sys.argv[1]
		srcLanguage = sys.argv[2]
		destLanguage = sys.argv[3]
	
	if not (os.path.exists("values-" + destLanguage)):
		os.mkdir("values-" + destLanguage)
			
	
	fdest = open("values-" + destLanguage + "/" + fileName, "w")
	fdest.write("""<?xml version="1.0" encoding="utf-8"?>""" +"\n")
	doc = ET.parse(fileName)
	resources = doc.getroot()
    
	for perString in resources.findall('string'):
		print "%s:%s" % (perString.attrib['name'],perString.text)
		namesPage = getPage(urllib2.quote(perString.text.encode('utf8')),srcLanguage,destLanguage)
		result = json.loads(namesPage)
		perString.text = parseJsonResult(namesPage)
	doc.write(fdest, 'utf-8')
	fdest.close();