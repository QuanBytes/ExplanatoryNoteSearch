# ExplanatoryNoteSearch
# 使用方法

####目前已支持格式

```objective-c
// 注释
```
```objective-c
// 注释
// 注释
// 注释
```

```objective-c
 /**
  注释
*/ 
```
```javascript
<!-- 注释-->
```
```javascript
<!-- 注释
     注释-->
```
iOS中```xib```,```storyboard```内的文本
```
text="注释"
title="注释"
```
iOS中```#pragma mark```注释
```
#pragma mark 注释
```

####安装xlrd和xlwt模块 ####

主要用于Excel的读写

	读 
	
	```shell
	pip install xlrd
	```
	写 
	```shell
	pip install xlwt
	```

####设置自己平台需要搜索文件类型  ####

打开` note_helper.py` 添加自己平台需要搜索的文件后缀名

```python
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
```

####设置需要过滤的文件 ####

打开` note_helper.py` 添加自己需要过滤的文件名

```python
#忽略掉的文件，填入文件夹或者文件的名称，log.txt最好不要删除，过滤掉日志文件
def ignorefileName():
    return ['log.txt']
```

####运行脚本  ####

1、将` note_helper.py`放入 需要搜索的文件夹 所在 **同层级**
2、` cd`到当前目录下
3、打开终端

#####查找  #####

```python
#查找
python3 note_helper.py search 
```
或者

```python
#查找
python3 note_helper.py s  
```

会生成```result.xls```文件

#####替换  #####

将翻译好的```result.xls```文件替换源文件
```python
#替换
python3 note_helper.py replace
```
或者
```python
#替换
python3 note_helper.py r
```



