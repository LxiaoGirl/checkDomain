#!/usr/bin/python 
#coding:utf-8
#author:xiaol

import urllib
import os
from multiprocessing import Pool,Manager


domainFileName = 'domain.txt'	#待验证域名文件
threadsNum = 30					#进程数
targetDomain = 'letv.com'		#主域名

def openDomainFile():
	return open(domainFileName,"r+")

def readDomain(fp):
	return fp.readlines()

def checkDomain(domain , urls):
	try:
		respose = urllib.urlopen(domain)
	except IOError:
		pass
	code = respose.getcode()
	url = respose.geturl()
	if code == 200:		
		if url[-1] != '/':
			url = url + '/'
		if url.find(targetDomain) != -1:
			urls.append(url)


def writeDomain(fp, domains):
	fp.seek(0)
	fp.truncate(0)
	for i in range(0, len(domains)):
		fp.write(domains[i]+'\n')
	fp.close()

def attackDomain(domains):
	proPool = setThreadPool()
	urls = []
	manager = Manager()
	urls = manager.list()
	if len(domains) != 0 :
		for i in range(0, len(domains)):
			if domains[i].find('http://') == -1:
				domains[i] = 'http://' + domains[i] 
			threads = proPool.apply_async(checkDomain, (domains[i], urls))
		proPool.close()
		proPool.join()
		if threads.successful():
			print "successful"
	urls = list(set(urls))
	return urls

def setThreadPool():
	return Pool(threadsNum)

def main():
	print("Start to check domains!")
	print("Please wait a minute!")
	fp = openDomainFile()
	urls = attackDomain(readDomain(fp))
	writeDomain(fp, urls)
	print("!!!OK!!!")

if __name__ == '__main__':
	main()