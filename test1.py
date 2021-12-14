import os
import sys

# 判断是否为源码文件
def isCodeFile(filePath):
    if filePath.endswith(".java"):
        return True
    else:
        return False

# 生成文件内容
def produceFileContent(filePath,map1,map2):
    print("🔧正在生成文件内容--> " + filePath)

    if isCodeFile(filePath) == False:
        # print("⚠️ 此文件不是源码文件，忽略处理 ... --> " + filePath)
        return

    with open(filePath, mode="r", encoding="utf-8") as oldFile:
        for line in oldFile:
            if line == ("    }" + '\n'): #函数的结尾
                print("当前函数生成的路径参数:")
                paramcontent = ""
                for item in map1:
                    if map1[item] > 1:
                        # print(str(item) + "  " + str(map1[item]))
                        map1[item] = 1
                        paramcontent = paramcontent + ("@RequestParam(value = \"" + item + "\", required = false)")
                        paramcontent = paramcontent + " " + map2[item] + " " + item + ","
                paramcontent = paramcontent.strip(',')  #去掉最后一个 ,
                print(paramcontent)
                print("当前函数生成的result:")
                result = "";
                for item in map2:
                    result = result + "result.add(\"" + item + "\"," + item + ")" + ";" + "\n"
                result = result + "return result;"
                print(result)
            else:
                for item in map1:
                    if item in line:
                        map1[item] = map1[item] + 1
    print("✅文件内容生成完成！--> " + filePath)
    print("---------------------------------------")
    return

#获取成员变量
#例:
# map1 = {'a1':0,'a2':0,'a3':0,'a4':0}  用于判断函数中是否出现该成员变量
# map2 = {'a1':'int','a2':'int','a3':'int','a4':'int'} 用于记录成员变量类型
# map = [map1,map2]
# filter 可能出现的变量类型 用于排除service的影响
def getMap(filePath):
    map = []
    map1 = {}
    map2 = {}
    filter = ['int','long']
    if isCodeFile(filePath) == False:
        # print("⚠️ 此文件不是源码文件，忽略处理 ... --> " + filePath)
        return
    print("🔧正在获取成员变量信息--> " + filePath)
    with open(filePath, mode="r", encoding="utf-8") as oldFile:
        for line in oldFile:
            line = line.strip() #去掉首位空格
            liebiao = line.split() #根据空格分割
            if "private" in liebiao and len(liebiao) == 3: #成员变量判断条件
                log = "" #日志信息
                type = liebiao[1]
                param = liebiao[2].strip(';')
                log = log + "变量类型:" + type + "变量名:" + param
                print(log)
                if type in filter: #主要用于排除service的影响
                    map1[param] = 0
                    map2[param] = type
    print("✅成员变量信息获取完成!--> " + filePath)
    map.append(map1)
    map.append(map2)
    if len(map[0]) > 0:
        print("当前成员变量信息:")
        print(map1)
        print(map2)
    else:
        print(filePath + "不包含成员变量")
        print("---------------------------------------")
    return map


# 遍历路径，获得所有文件
def foreachPath(currentPath):
    for root, dirs, files in os.walk(currentPath , topdown=False):
        for file in files:
            filePath = os.path.join(root, file)
            map = getMap(filePath)
            if map != None and len(map[0]) > 0:
                produceFileContent(filePath, map[0], map[1])

# 入口
def main():
    currentPath = input("\n请输入需要处理的文件目录：\n")
    print("需要处理的文件目录为:" + currentPath)
    foreachPath(currentPath)

main()