#!/usr/bin/env python
# coding=utf-8

# 从A拷贝到B
# A代码路径
AProjectDir=r''

#B代码路径
DestProjectDir = r''
#代码完全以A为准,True表示拷贝整个文件夹，False遍历文件夹中的文件，将文件拷贝，如XXXDir只是包含了完整文件夹中的个别文件
AuthoritySrcFolderList={'XXXDir':True,}

#内容完全以A为准
AuthorityContentFolderList={ }

#包含特定文本的忽略同步
IgnorName = []