# 预处理需要将以下部分删除:
# private static final long serialVersionUID = -1895422056734170612L;
# private static final Logger LOGGER = Logger.getLogger(AccountRFMModelAjaxAction.class);
# protected void ajaxExecute()
# public int getCode()
# public Map<String, Object> getMsg()
# public String getAccountid()
# public void setAccountid(String accountid)
# 对于内部类的get set方法不删除


import os
import sys

#找到内部类的边界  需要输入起始行以及列表 传入的是出现的当前索引
def findEnd(i,lines):
    res = 0
    while i < len(lines):
        line = lines[i]
        if line == ("    }" + '\n'):
            res = i#返回的是行号
            break
        else:
            i = i + 1

    return res

# 判断是否为源码文件
def isCodeFile(filePath):
    if filePath.endswith(".java"):
        return True
    else:
        return False

# 预处理
def Pretreatment(filePath):

    num = 0 #当前行数
    if isCodeFile(filePath) == False:
        print("⚠️ 此文件不是源码文件，忽略处理--> " + filePath)
        return False
    print("🔧正在打开源码文件--> " + filePath)
    with open(filePath, mode="r", encoding="utf-8") as oldFile, open("%s.bak" % filePath, mode="w", encoding="utf-8") as newFile:
        lines = [line for line in oldFile] #获取每行文本并增加到列表
        while num < len(lines):
            line = lines[num]
            line = line.strip() #去掉首位空格
            liebiao = line.split() #根据空格分割
            if "public" in liebiao and "class" in liebiao and "extends" in liebiao: #改类的名字和继承
                #增加注解
                line = "@Slf4j\n" + "@RestController\n" + "@RequestMapping()\n"
                newFile.write(line)
                if "AjaxAction" in liebiao[2]:
                    liebiao[2] = liebiao[2].replace("AjaxAction","Controller")
                elif "Action" in liebiao[2]:
                    liebiao[2] = liebiao[2].replace("Action","Controller")
                liebiao[4] = "MidasBaseController"
                line = " ".join(liebiao)
                newFile.write(line)
                print("当前行号为" + str(num) + ": 修改类名后:" + line)
            elif "static" in liebiao and "final" in liebiao: #删除常量
                print("当前行号为" + str(num) + ": 待删除变量:" + line)
            elif "public" in liebiao and "void" in liebiao and "{" in liebiao and str(liebiao[2][0:3]) == "set": #删set方法
                print("当前行号为" + str(num) + ": 删除set方法:" + line)
                end = findEnd(num, lines)
                num = end
            elif "public" in liebiao and str(liebiao[2][0:3]) == "get": #删get方法
                print("当前行号为" + str(num) + ": 删除get方法:" + line)
                end = findEnd(num, lines)
                num = end
            elif "public" in liebiao and "static" in liebiao and "class" in liebiao:  # 遇见内部类需要忽略处理
                print("当前行号为" + str(num) + ": 遇到内部类:" + line)
                end = findEnd(num, lines)
                while num <= end:
                    newFile.write(lines[num])
                    num += 1
            elif "@Override" in liebiao:  #必须保证下面对应的是以下三个方法
                nextline = lines[num + 1]
                nextline = nextline.strip()
                nextliebiao = nextline.split()
                print("当前行号为" + str(num) + ": 判断注解是否该删除:" + line)
                if "ajaxExecute()" in nextliebiao or "getMsg()" in nextliebiao or "getCode()" in nextliebiao:
                    print("当前行号为" + str(num + 1) + ": 待删除重写函数:" + nextline)
                    end = findEnd(num + 1, lines)
                    num = end
                else:
                    print("当前行号为" + str(num) + ": 该注解不该删除:" + line)
                    newFile.write(lines[num])
            else:
                newFile.write(lines[num])
            num += 1
    os.remove(filePath)
    os.rename("%s.bak" % filePath, filePath)
    return True


# 遍历路径，获得所有文件
def foreachPath(currentPath):

    num1 = 0 #文件总数
    num2 = 0 #java文件个数
    for root, dirs, files in os.walk(currentPath , topdown=False):
        for file in files:
            filePath = os.path.join(root, file)
            num1 += 1
            if Pretreatment(filePath) == True:
                num2 += 1

    return [num1,num2]

# 预处理入口
def main():
    currentPath = input("\n请输入需要处理的文件目录：\n")
    print("需要处理的文件目录为:" + currentPath)
    filenum = foreachPath(currentPath)
    print("共有" + str(filenum[0]) + "个文件!")
    print("已处理" + str(filenum[1]) + "个java文件!")

main()