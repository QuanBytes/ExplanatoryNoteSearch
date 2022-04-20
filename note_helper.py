#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import os
import re
import io
import shutil
import sys
from typing import final
import xlrd
import xlwt
import string

#写入需要搜索的文件的后缀名
#iOS平台
def is_iOS_Valid_file_name():
    return ['.h','.m','.mm','.c','.txt','.xib','.storyboard']

#Android平台
def is_Android_Valid_file_name():
    return ['.java','.kt','xml']

#web平台
def is_Web_Valid_file_name():
    return ['.js','.html']

#忽略掉的文件，填入文件夹或者文件的名称，log.txt最好不要删除，过滤掉日志文件
def ignorefileName():
    return ['Pods','log.txt','SVGKit','ZegoLiveRoomSDK','ZegoExpressEngineSDK']


script_path = os.path.dirname(os.path.realpath(__file__))
#结果文本目录
resultFilePath = "{}/{}".format(script_path, 'result.txt')
logFilePath = "{}/{}".format(script_path, 'log.txt')
#Excel
excelName = 'result.xls'
excelPath = "{}/{}".format(script_path, excelName)

fw = open(logFilePath, 'w')

def clean_cahce():
    fw.write('清理掉上一次结果 \n')
    result = open(resultFilePath,'w')
    result.truncate(0)
    result.close()
    log = open(logFilePath,'w')
    log.truncate(0)
    log.close()

#遍历当前文件夹
def get_filelist_path(rootdir):
    filelist = [] #文件集合.
    for root,dirs,files in os.walk(rootdir):
        for file in files:
            filePath = os.path.join(root,file)
            isignore = False
            iscontain = False
            for ignorename in ignorefileName():
                if ignorename in filePath:
                    isignore = True
                    fw.write(filePath + ' 被指定忽略！！！ \n')
                    break

            if isignore == False and check_valid(filePath):
                filelist.append(filePath)
    return filelist

def check_valid(filePath):
    isValidFile = False
    for txt in is_iOS_Valid_file_name():
        if filePath.lstrip().endswith(txt,0,len(filePath)):
            # global isValidFile
            isValidFile = True
            break
            
    for txt in is_Android_Valid_file_name():
        if filePath.lstrip().endswith(txt,0,len(filePath)):
            isValidFile = True
            break
            
    for txt in is_Web_Valid_file_name():
        if filePath.lstrip().endswith(txt,0,len(filePath)):
            isValidFile = True
            break
        
    return isValidFile
    
#搜索符合条件的文本
def searchText(file):
    filePath = os.path.join(file)
    fw.write('\n正在查找的文件 \n'+ filePath)
    # if os.path.exists(filePath):
    #     raise Exception(filePath,' NOT EXISIT !!!')

    #过滤掉不符合编码的文件
    if check_valid(filePath) == False:
        return []

    # // 空格
    STATE_ONE = 0   
    # /**
    # */  
    STATE_TWO = 0
    #<!-- 
    #-->
    STATE_THREE = 0
    #找出xib，storyboard 中的中文
    STATE_FOUR = 0  
    #找出 #pragma mark 后的中文
    STATE_FIVE = 0
	
    textlist = [] #存放满足条件的字符串数组
    tempText = '' #临时存储满足条件的字符串
    

    with io.open(filePath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.lstrip().startswith('/***/',0,len(line)):
                continue
            
            if line.lstrip().startswith('//',0,len(line)):
                tempText = line.strip()
                textlist.append(tempText)
                tempText = ''
                continue
                            
#             if line.lstrip().startswith('//',0,len(line)) or STATE_ONE == 1:
#                  STATE_ONE = 1
#                  tempText = tempText + line
#                  #去掉空格
#                  if line.lstrip().startswith('//',0,len(line)) == False and STATE_ONE == 1:
#                      STATE_ONE = 0
#                      tempText = tempText.rstrip(line)
#                      textlist.append(tempText)
#                      tempText = ''

            if line.lstrip().startswith('/**',0,len(line)) or STATE_TWO == 1:
                STATE_TWO = 1
                tempText = tempText + line
                if line.rstrip().endswith('*/',0,len(line)) and STATE_TWO == 1:
                    STATE_TWO = 0
                    textlist.append(tempText)
                    tempText = ''
                continue

            if line.lstrip().startswith('<!--',0,len(line)) or STATE_THREE == 1:
                STATE_THREE = 1
                tempText = tempText + line
                if line.rstrip().endswith('-->',0,len(line)) and STATE_THREE == 1:
                    STATE_THREE = 0
                    textlist.append(tempText)
                    tempText = ''
                continue
            
            if 'text="' in line:
                tempText = re.search('text="(.*?)"',line)[1]
                if tempText is not None and len(tempText) > 0:
                    textlist.append(tempText)
                    tempText = ''
                continue

            if 'title="' in line:
                tempText = re.search('title="(.*?)"',line)[1]
                if tempText is not None and len(tempText) > 0:
                    textlist.append(tempText)
                    tempText = ''
                continue
                
            if line.lstrip().startswith('#pragma mark',0,len(line)):
               tempText = line.strip()
               textlist.append(tempText)
               tempText = ''
               continue
               
    return textlist


#找到满足条件的文本并写入TXT
def writeText(fileList):
    if len(fileList) == 0:
        raise Exception('NOT FILE IN CURRENT DIR !!!')

  

    #写入文本
    result = open(resultFilePath,'w')
    
    for filePath in fileList:
        textlist = searchText(filePath)
        if textlist is None:
            continue
        fw.write('\n --- 找到的文本列表 --- \n')
        for text in textlist:
            fw.write(text)
            result.write(text)
            result.write('\n')

    result.close()
    
#找到满足条件的文本并写入EXCEL
def writeEXCEL(fileList):
    if len(fileList) == 0:
        raise Exception('NOT FILE IN CURRENT DIR !!!')

    workbook = xlwt.Workbook(encoding= 'ascii')
    
    for filePath in fileList:
        textlist = searchText(filePath)
        if textlist == [] or len(textlist) == 0:
            continue
        fw.write('\n --- 找到的文本列表 --- \n')
        
        sheetName =  os.path.basename(filePath)

        file_splite_list = filePath.split('/')
        if len(file_splite_list) > 1 :
            sheetName = file_splite_list[-1]

        fw.write('\n --- sheetName --- \n' + sheetName  + '\n')

        try:
            worksheet = workbook.add_sheet(sheetName)
            i = 0
            for text in textlist:
                if len(text):
                    fw.write(text + '\n')
                    worksheet.write(i,0, text)
                    i = i + 1
        except :
            fw.write(sheetName + '文件名异常过滤\n')
        finally :
            fw.write('\n')

    try:
        workbook.save(excelName)
    except :
        fw.write('没有可用sheet\n')
    finally :
        fw.write('\n')

def replaceEXCEL(fileList):
    if len(fileList) == 0:
        raise Exception('NOT FILE IN CURRENT DIR !!!')
    
    workbook = xlrd.open_workbook(excelPath)

    fw.write('\n --- 所有的sheetName --- \n')

    sheetNames = workbook.sheet_names()

    for i in range(len(sheetNames)):
        each_sheet = workbook.sheet_by_index(i)
        fw.write('\n --- 当前匹配的sheetName --- \n')
        fw.write(each_sheet.name + '\n')
     
        for filePath in fileList:
      
            input = open(filePath, 'r', encoding='utf-8')
            content = input.read()
            input.close()

            output = open(filePath, 'w', encoding='utf-8')
        
            for rx in range(each_sheet.nrows):
                if each_sheet.ncols > 1 and each_sheet.name in filePath:
                    col1 = each_sheet.cell_value(rowx=rx, colx=0)
                    col2 = each_sheet.cell_value(rowx=rx, colx=1)
                    if len(col2):
                        fw.write('\n 替换前'+ content + '\n')
                        fw.write('源数据 ' + col1)
                        fw.write('替换后的数据 ' + col2)
                        content = content.replace(col1,col2)
                        fw.write('\n 替换后'+ content + '\n')
                        fw.write('\n --- 替换完毕 --- \n')
                    
            output.write(content)
            output.close()

if __name__ == "__main__":

    currentFilePath = "{}".format(script_path)

    build = sys.argv[1]
    
    #清空result
    clean_cahce()

    #遍历所有文件
    fileList = get_filelist_path(currentFilePath)

    fw.write('所有文件 \n ' )

    for path in fileList:
        fw.write (path + '\n')

    if build == 'search' or build == 's':
        #写入txt
        # writeText(fileList)

        #写入Excel
        writeEXCEL(fileList)

    if build == 'replace' or build == 'r':
        #替换文本
        replaceEXCEL(fileList)
    
    fw.close()
    
     


   

