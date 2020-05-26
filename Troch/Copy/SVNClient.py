#!/usr/bin/env python
# coding=utf-8

import subprocess
import os.path

def update(svn_work_path):
    if not os.path.exists(svn_work_path):
        print('svn工作路径：%s 不存在，退出程序' % svn_work_path)
        return False
    args = 'cd /d ' + svn_work_path + ' & svn update'
    with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        output = proc.communicate()
        print('执行svn update命令输出：%s' % str(output))
        if not output[1]:
            print('svn update命令执行成功' )
            return [True,'执行成功']
        else:
            print('svn update命令执行失败:%s' % str(output))
            return  [False, str(output)]

def add(folderpath, file):
    if not os.path.exists(os.path.join(folderpath,file)):
        return [False,'svn add 工作路径：%s 不存在，退出程序' % os.path.join(folderpath,file)]
    args = 'cd /d ' + folderpath + ' & svn add ' + file
    with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        output = proc.communicate()
        #print('执行svn add命令输出：%s' %  str(output))
        if not output[1]:
            #print('svn add命令执行成功' )
            return [True,'执行成功']
        else:
            errorinfo = str(output[1])
            if errorinfo:
                findindex = errorinfo.find('is already under version control')
                if findindex != -1:
                    #print('svn add命令执行成功' )
                    return [True,'执行成功']

            #print('svn add命令执行失败:%s' % str(output))
            return  [False, 'svn add命令执行失败:%s' % str(output)]
def delete(folderpath, file):
    if not os.path.exists(os.path.join(folderpath,file)):
        return [False,'svn delete 工作路径：%s 不存在，退出程序' % os.path.join(folderpath,file)]
    args = 'cd /d ' + folderpath + ' & svn delete ' + file
    with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        output = proc.communicate()
        #print('执行svn add命令输出：%s' %  str(output))
        if not output[1]:
            #print('svn add命令执行成功' )
            return [True,'执行成功']
        else:
            errorinfo = str(output[1])
            if errorinfo:
                findindex = errorinfo.find('is not a working copy')
                if findindex != -1:
                    #print('svn add命令执行成功' )
                    return [True,'执行成功']
                elif errorinfo.find('is not under version control') != -1:
                    return [True,'执行成功']
            #print('svn add命令执行失败:%s' % str(output))
            return  [False, 'svn delete 命令执行失败:%s' % str(output)]

def commit(path):
    if not os.path.exists(path):
        print('svn commit 工作路径：%s 不存在，退出程序' % path)
        return False
    args = 'cd /d ' + path + ' & svn commit -m'
    with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        output = proc.communicate()
        print('执行svn commit命令输出：%s' % str(output))
        if not output[1]:
            print('svn commit命令执行成功' )
            return [True,'执行成功']
        else:
            print('svn commit命令执行失败,正在重试:%s' % str(output))
            return  [False, str(output)]

def getlock(folderpath, file):
    if not os.path.exists(os.path.join(folderpath,file)):
        return [False,'svn lock 工作路径：%s 不存在，退出程序' % os.path.join(folderpath,file)]
    args = 'cd /d ' + folderpath + ' & svn lock ' + file
    with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        output = proc.communicate()
        #print('执行svn add命令输出：%s' %  str(output))
        if not output[1]:
            #print('svn add命令执行成功' )
            return [True,'执行成功']
        else:
            errorinfo = str(output[1])
            if errorinfo:
                findindex = errorinfo.find('is already under version control')
                if findindex != -1:
                    #print('svn add命令执行成功' )
                    return [True,'执行成功']

            #print('svn add命令执行失败:%s' % str(output))
            return  [False, 'svn lock 命令执行失败:%s' % str(output)]