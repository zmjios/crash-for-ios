#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'zengmingjian'

import os
import sys
import commands

def crashFileValid(excuteFile,dsymFile):
	excuteCmd =  "dwarfdump --uuid " + excuteFile + "/" + excuteFile[0:len(excuteFile) - 4]
	print excuteCmd
	dsymCmd = "dwarfdump --uuid " + dsymFile
	lines1 = os.popen(excuteCmd).readlines()
	lines2 = os.popen(dsymCmd).readlines()
	for line in lines1:
		uuidString1 = line.split(' ')[1]
	for line in lines2:
		uuidString2 = line.split(' ')[1]
	if (uuidString1 == uuidString2):
		print ("uuidString = " + uuidString1)
		return True
	else:
		print ("uuidString1 = " + uuidString1)
		print ("uuidString2 = " + uuidString2)
		print("!!!!!dsym 文件 和 可执行app文件不匹配！！！！！")
		return False

#解析设置环境
def setEnvironment():
	os.environ["DEVELOPER_DIR"]="/Applications/Xcode.app/Contents/Developer/"  #DISPLAY是环境变量名，：0.0是要设置的值
	os.system('$DEVELOPER_DIR')
	
#检测是否存在symbolicatecrash工具，如果不存在，则在xcode拷贝到当前目录
def getSymbolicatecrashTool():
	currentDir = os.getcwd()
	symbolDir = "/Applications/Xcode.app/Contents/SharedFrameworks/DTDeviceKitBase.framework/Versions/A/Resources/symbolicatecrash"
	for root,dirs,files in os.walk(currentDir):
		if os.path.exists(root + "/" + "symbolicatecrash"):
			print("=================")
			setEnvironment()
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
	if (crashFileValid(appName, dsymName) == False):
		return

	for crashFile in crashList:
		if crashFile.endswith(".crash"):
			print crashFile
			print dsymName
			os.system("./symbolicatecrash "+ crashFile + " " + dsymName + " >> " + crashFile.replace(".crash",".log"))
		elif crashFile.endswith(".ips"):
			os.system("./symbolicatecrash "+ crashFile + " " + dsymName +" >> " + crashFile.replace(".ips",".log"))

def startPaser():
	getSymbolicatecrashTool()
	parseCrashLog()


if __name__ == '__main__':
	startPaser()






		