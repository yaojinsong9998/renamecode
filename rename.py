
import os
import sys
# 判断是否为源码文件
def isCodeFile(filePath):

    if filePath.endswith(".java"):
        return True
    else:
        return False

# 替换文件后缀名
def renameFile(filePath, old1, old2, new):
    print("🔧 正在更改文件名 ... --> " + filePath)

    if isCodeFile(filePath) == False:
        print("⚠️ 此文件不是源码文件，忽略处理 ... --> " + filePath)
        return False

    pathArr = filePath.split("/")
    fileName = pathArr[-1]
    print(pathArr)

    if old1 in fileName:
        newFilePath = filePath
        tmpName = fileName.replace(old1, new)
        print("newFilePath = " + newFilePath)
        newFilePath = newFilePath.replace(fileName, tmpName)
        os.rename(filePath, newFilePath)
    elif old2 in fileName:
        newFilePath = filePath
        tmpName = fileName.replace(old2, new)
        print("newFilePath = " + newFilePath)
        newFilePath = newFilePath.replace(fileName, tmpName)
        os.rename(filePath, newFilePath)
    print("✅ 文件名称处理完成！ --> " + filePath)
    return True


def foreachPath(currentPath):
    num1 = 0  # 文件总数
    num2 = 0  # java文件个数
    old1 = "AjaxAction"
    old2 = "Action"
    new = "Controller"
    # 遍历路径，获得所有文件
    for root, dirs, files in os.walk(currentPath, topdown=False):
        for file in files:
            filePath = os.path.join(root, file)
            num1 += 1
            if renameFile(filePath, old1, old2, new) == True:
                num2 += 1
    return [num1,num2]
def main():
    currentPath = input("\n请输入需要处理的文件目录：\n")
    print("需要处理的文件目录为:" + currentPath)
    filenum = foreachPath(currentPath)
    print("共有" + str(filenum[0]) + "个文件!")
    print("已处理" + str(filenum[1]) + "个java文件!")

main()