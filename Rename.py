#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 文件名：Rename.py
# 创建者：walker

import os
import sys
# 判断是否为源码文件
def isCodeFile(filePath):

    if filePath.endswith(".txt"):
        return True
    else:
        return False

# 替换文件内容
def replaceFileContent(filePath, oldString, newString):
    print("🔧 正在处理文件内容 ... --> " + filePath)

    if isCodeFile(filePath) == False:
        print("⚠️ 此文件不是源码文件，忽略处理 ... --> " + filePath)
        return

    with open(filePath, mode="r", encoding="utf-8") as oldFile, open("%s.bak" % filePath, mode="w", encoding="utf-8") as newFile:
        for line in oldFile:
            if oldString in line:
                line = line.replace(oldString, newString)
            newFile.write(line)
    os.remove(filePath)
    os.rename("%s.bak" % filePath, filePath)
    print("✅ 文件内容处理完成！ --> " + filePath)
    return

# 替换文件名称前缀
def renameFilePrefix(filePath, oldPrefix, newPrefix):
    print("🔧 正在处理文件名称前缀 ... --> " + filePath)

    if isCodeFile(filePath) == False:
        print("⚠️ 此文件不是源码文件，忽略处理 ... --> " + filePath)
        return

    pathArr = filePath.split("/")
    fileName = pathArr[-1]
    print(pathArr)

    if oldPrefix in fileName:
        newFilePath = filePath
        tmpName = fileName.replace(oldPrefix, newPrefix)
        print("newFilePath = " + newFilePath)
        newFilePath = newFilePath.replace(fileName, tmpName)
        print(tmpName + ">>" + fileName + ">>" + newFilePath)

        os.rename(filePath, newFilePath)

    print("✅ 文件名称前缀处理完成！ --> " + filePath)
    return

print("\n   RenameFile--python \n")
print("##############################################\n\n ⚠️️【脚本操作有破坏源码文件的风险，请务必备份后再继续运行】⚠️️ \n\n##############################################")

# 获得处理路径
currentPath = os.getcwd()
currentPath = input("\n请输入需要处理的文件目录：\n")

print("需要处理的文件目录为:" + currentPath)
path_confirm = input("确认：Y/N\n")

if "y" in path_confirm.lower():
    print("y")
else:
    print("请重新运行脚本，并输入正确路径!")
    sys.exit()

# 替换文件内容
oldString = input("请输入文件内容需要替换的字符串,按回车结束:")
newString = input("请输入文件内容替换后的字符串,按回车结束:")

# 遍历路径，获得所有文件
for root, dirs, files in os.walk(currentPath , topdown=False):
    for file in files:
        filePath = os.path.join(root, file)
        replaceFileContent(filePath, oldString, newString)

# 替换文件名前缀
replacePrefix_confirm = input("是否需要替换文件名前缀(Y/N)\n")

if "y" in replacePrefix_confirm.lower():
    oldPrefix = input("请输入文件名称需要替换的前缀,按回车结束:")
    newPrefix = input("请输入文件名称替换后的前缀,按回车结束:")
    # 遍历路径，获得所有文件
    for root, dirs, files in os.walk(currentPath , topdown=False):
        for file in files:
            filePath = os.path.join(root, file)
            renameFilePrefix(filePath, oldPrefix, newPrefix)
    print("脚本运行完毕！")
else:
    print("脚本运行完毕！")
    sys.exit()
