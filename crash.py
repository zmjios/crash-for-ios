#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8
#author = zengmingjian

import os

def crashFileValid(fileName):
	st,out=commands.getstatusoutput("dwarfdump --uuid IHexin.app.dSYM/")
	return True

#解析设置环境
def setEnvironment():
	os.system("export DEVELOPER_DIR=" + "/Applications/Xcode.app/Contents/Developer/")
	os.system("export PATH=" + "$PATH:/Applications/Xcode.app/Contents/SharedFrameworks/DTDeviceKitBase.framework/Versions/A/Resources")

#检测是否存在symbolicatecrash工具，如果不存在，则在xcode拷贝到当前目录
def getSymbolicatecrashTool():
	currentDir = os.getcwd()
	symbolDir = "/Applications/Xcode.app/Contents/SharedFrameworks/DTDeviceKitBase.framework/Versions/A/Resources/symbolicatecrash"
	for root,dirs,files in os.walk(currentDir):
		if os.path.exists(root + "/" + "symbolicatecrash"):
			return
		else:
			os.system("cp " + symbolDir + " " + currentDir)
			setEnvironment()
			break

#遍历当前目录，解析文件
def parseCrashLog():
	dirList = os.listdir(os.getcwd())
	print dirList
	crashList = []
	dsymName = ""
	appName = ""
	for d in dirList:
		if d.endswith(".crash") or d.endswith(".ips"):
			crashList.append(d)
		if d.endswith(".dSYM"):
			dsymName = d
		if d.endswith(".app"):
			appName = d
	#不存在dsym文件
	if dsymName == "":
		print "error:请将dsym文件考到当前目录!!!!!"
		return
	if appName == "":
		print "error:请将app文件考到当前目录!!!!"
		return

	#检测dsym文件 和app文件是否匹配

	for crashFile in crashList:
		if crashFile.endswith(".crash"):
			print crashFile
			print dsymName
			os.system("./symbolicatecrash "+ crashFile + " " + dsymName + " >> " + crashFile.replace(".crash",".log"))
		elif crashFile.endswith(".ips"):
			os.system("./symbolicatecrash "+ crashFile + " " + dsymName +" >> " + crashFile.replace(".ips",".log"))

def start():
	getSymbolicatecrashTool()
	parseCrashLog()


if __name__ == '__main__':
	start()






		