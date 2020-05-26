# !/usr/bin/env python
# coding=utf-8

from Copy import Config, SVNClient
import os, sys
import subprocess
import time


# cwd = os.path.dirname(os.path.abspath(__file__))
# if cwd not in sys.path: sys.path.append(cwd)


class resultmessgae(object):
    def __init__(self):
        self.FileExistError = []
        self.OtherError = []
        self.DestNewAddFile = {}
        self.NeedCheckFile = {}
        self.NeedSVNAdd = {}
        self.IgnorFile = {}
        self.CopyAFile = {}
        self.CopyAAsset = {}
        self.CopyFileError = []
        # self.NeedSVNDel = {}

        # 这些都由 Config.py 中配置
        # A代码路径
        self.AProjectDir = r''
        # 代码路径
        self.DestProjectDir = r''
        # 代码完全以A工程为准,key为文件夹名，value表示是否整个文件夹拷贝
        self.AuthoritySrcFolderList = {}
        # 内容完全以A工程为准
        self.AuthorityContentFolderList = []
        # 包含特定文本的忽略同步
        self.IgnorName = []

    def add_checkFile(self, folder, file, destfile):
        file_time = file
        filepath = os.path.join(folder, file)
        file_mtime = 0
        dest_mtile = 0
        if os.path.exists(filepath) and os.path.isfile(filepath):
            file_mtime = os.path.getmtime(filepath)
            file_time = file

        if os.path.exists(destfile) and os.path.isfile(destfile):
            dest_mtile = os.path.getmtime(destfile)

        if file_mtime > 0 and dest_mtile > 0 and not filepath.endswith('.vcproj'):
            if file_mtime > dest_mtile:
                file_time = file_time + '\t A文件较新'

        if file_mtime > 0:
            timeArray = time.localtime(file_mtime)
            file_time = file_time + '\t' + time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        if dest_mtile > 0:
            timeArray = time.localtime(dest_mtile)
            file_time = file_time + '\t 主线时间：' + time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        self.NeedCheckFile.setdefault(folder, []).append(file_time)

    def add_newFile(self, folder, file):
        self.DestNewAddFile.setdefault(folder, []).append(file)

    def add_ignoreFile(self, folder, file):
        self.IgnorFile.setdefault(folder, []).append(file)

    def add_svnFile(self, folder, file):
        self.NeedSVNAdd.setdefault(folder, []).append(file)

    def del_svnFile(self, folder, file):
        # 非uc或uci文件不执行svn delete操作
        if os.path.isfile(file) and not file.endswith('.uc') and not file.endswith('.uci'):
            return;

        addresult, addmessage = SVNClient.delete(folder, file)
        if not addresult:
            self.OtherError.append(addmessage)

        curpath = os.path.join(folder, file)
        if os.path.isdir(curpath):
            self.OtherError.append("[%s]为文件夹，svn commit时，请留意svn delete该文件夹操作！有可能svn delete没有成功" % (curpath))

    def add_error_FileExist(file):
        self.FileExistError.append(file)

    def add_error_Other(errormessage):
        self.OtherError.append(errormessage)

    def add_copyAFile(self, folder, file):
        self.CopyAFile.setdefault(folder, []).append(file)

    def add_copyAAsset(self, folder, file):
        self.CopyAAsset.setdefault(folder, []).append(file)


def getSrcDir(result):
    srcPath = r'%s\Development\Src'
    destSrcDir = srcPath % (result.DestProjectDir.strip())
    ASrcDir = srcPath % (result.AProjectDir.strip())
    return destSrcDir, ASrcDir


def getBProjDir(result):
    srcPath = r'%s\BProj'
    destDir = srcPath % (result.DestProjectDir.strip())
    ADir = srcPath % (result.AProjectDir.strip())
    return destDir, ADir


def compareSrcFolders(result):
    destDir, ADir = getSrcDir(result)
    if os.path.exists(ADir):
        file_list = os.listdir(ADir)
        for file in file_list:
            new_path = os.path.join(ADir, file)
            # 文件
            if os.path.isfile(new_path):
                compareFile(os.path.join(destDir, file), new_path, file, result)
                # result.add_checkFile(ADir,file)
            else:
                # print('----compareSrcFolders, \t%s \t%s\t%s ' %(file,os.path.join(destDir,file),new_path))
                compareSrcFolder(os.path.join(destDir, file), new_path, file, result.AuthoritySrcFolderList, result)


def compareBProjFolders(result):
    destDir, ADir = getBProjDir(result)
    if os.path.exists(ADir):
        file_list = os.listdir(ADir)
        for file in file_list:
            new_path = os.path.join(ADir, file)
            # 文件
            if os.path.isfile(new_path):
                compareFile(os.path.join(destDir, file), new_path, file, result)
            else:
                # print('----compareBProjFolders, \t%s \t%s\t%s ' %(file,os.path.join(destDir,file),new_path))
                compareBProjFolder(os.path.join(destDir, file), new_path, file, result.AuthorityContentFolderList,
                                   result)


def read_file_lines(fname, result):
    try:
        lines = []
        # with open(fname,'r',encoding='utf8') as f:
        with open(fname, 'rb') as f:
            # text = f.readline()
            text = f.read()
            if text != '':
                lines.append(text.strip())
        f.close()
        return lines

    except Exception as e:
        print(e)
        result.add_error_Other('Open File %s Error' % (fname))
    raise Exception('Open File %s Error' % (fname))


def getFileTime(inFilePath):
    timeArray = time.localtime(os.path.getmtime(inFilePath))
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def compareFile(indestFilePath, inAFilePath, infilename, result):
    # print('----compareFile, \t%s\t%s ' %(indestFilePath,inAFilePath))
    bNeedCheck = False
    bNewAdd = False
    for tIngorName in result.IgnorName:
        if len(tIngorName) > 0 and tIngorName in infilename:
            split_list = inAFilePath.split('\\')
            folerPath = os.sep.join(split_list[0:-2])
            result.add_ignoreFile(folerPath, split_list[-1])
            # print('----compareFile---IgnorFile, \t%s \t%s ' %(folerPath,split_list[-1]))
            return

    if not os.path.exists(inAFilePath):
        result.add_error_FileExist('A工程：%s' % (inAFilePath))

    if not os.path.exists(indestFilePath):
        bNewAdd = True
        copyResult = copy_dir_file(inAFilePath, indestFilePath)
        if copyResult.returncode == 0:
            result.add_svnFile(os.path.dirname(indestFilePath), infilename)
            result.add_copyAFile(os.path.dirname(indestFilePath), infilename)
        else:
            errStr = copyResult.stderr.decode('gbk')
            errStr = errStr.rstrip('\r\n')
            Atime = getFileTime(inAFilePath)
            desttime = getFileTime(indestFilePath)
            result.CopyFileError.append('%s\t%s\t%s\tA工程时间：%s' % (errStr, indestFilePath, desttime, Atime))
    else:
        destSize = os.path.getsize(indestFilePath)
        ASize = os.path.getsize(inAFilePath)
        if destSize != ASize:
            bNeedCheck = True
        else:
            destText = read_file_lines(indestFilePath, result)
            AText = read_file_lines(inAFilePath, result)
            destLen = len(destText)
            ALen = len(AText)
            if destLen != ALen:
                bNeedCheck = True
            else:
                for i in range(destLen):
                    if destText[i] != AText[i]:
                        bNeedCheck = True
                        break

    if bNeedCheck == True:
        folerPath = os.path.dirname(inAFilePath)
        result.add_checkFile(folerPath, infilename, indestFilePath)
        # print('----compareFile---NeedCheck, \t%s \t%s ' %(folerPath,infilename))
    if bNewAdd == True:
        folerPath = os.path.dirname(inAFilePath)
        result.add_newFile(folerPath, os.path.basename(inAFilePath))
        # print('----compareFile---NewAdd, \t%s \t%s ' %(folerPath,infilename))


# 比对A工程和主线代码文件夹，添加或删除svn文件
def AddSVN_CodeFolderFile(indestFolderPath, inAFolderPath, result):
    destfiles_dict = {}
    destdirs_dict = {}
    if os.path.exists(indestFolderPath):
        for root, dirs, files in os.walk(indestFolderPath):
            destfiles_dict[root] = files
            destdirs_dict[root] = dirs

    for root, dirs, files in os.walk(inAFolderPath):

        destFolderPath = indestFolderPath
        pathsplits = root.strip().split(inAFolderPath)
        appendpath = pathsplits[1]
        if appendpath:
            appendpath = appendpath[1:]
            destFolderPath = os.path.join(indestFolderPath, appendpath)

        destdirs = destdirs_dict[destFolderPath]
        for Adir in dirs:
            if not destdirs or not Adir in destdirs:
                result.add_svnFile(destFolderPath, Adir)
        if destdirs:
            for destdir in destdirs:
                if not destdir in dirs:
                    result.del_svnFile(destFolderPath, destdir)

        destFiles = destfiles_dict[destFolderPath]
        for Afile in files:
            if not destFiles or not Afile in destFiles:
                result.add_svnFile(destFolderPath, Afile)
        if destFiles:
            for destfile in destFiles:
                if not destfile in files:
                    result.del_svnFile(destFolderPath, destfile)


def compareSrcFolder(indestFolderPath, inAFolderPath, inFolderName, inAuthorityFolderList, result):
    print('----compareSrcFolder, \t%s \t%s\t%s ' % (inFolderName, indestFolderPath, inAFolderPath))
    # 忽略指定文件同步
    for tIngorName in result.IgnorName:
        if len(tIngorName) > 0 and tIngorName in inFolderName:
            result.add_ignoreFile(inAFolderPath, inFolderName)
            print('----compareSrcFolder---IgnorFolder, \t%s ' % (inAFolderPath))
            return

    # 完全信任A工程
    bCopyAFile = False
    if inFolderName in inAuthorityFolderList.keys():
        # 拷贝整个文件夹，先删除主线对应文件夹
        if inAuthorityFolderList[inFolderName]:
            AddSVN_CodeFolderFile(indestFolderPath, inAFolderPath, result)
            if os.path.exists(indestFolderPath):
                delResult = del_dir_file(indestFolderPath)
                if delResult.returncode != 0:
                    errStr = delResult.stderr.decode('gbk')
                    errStr = errStr.rstrip('\r\n')
                    result.CopyFileError.append('删除文件夹错误：请留意该文件夹拷贝，必要时手工拷贝！ %s\t%s' % (errStr, indestFolderPath))
                    # shutil.move(inAFolderPath,indestFolderPath)
            copyResult = copy_dir_file(inAFolderPath, indestFolderPath)
            if copyResult.returncode == 0:
                result.add_copyAFile(os.path.dirname(indestFolderPath), inFolderName)
            else:
                errStr = copyResult.stderr.decode('gbk')
                errStr = errStr.rstrip('\r\n')
                Atime = getFileTime(inAFolderPath)
                desttime = getFileTime(indestFolderPath)
                result.CopyFileError.append('%s\t%s\t%s\tA工程时间：%s' % (errStr, indestFolderPath, desttime, Atime))
            return
        else:
            bCopyAFile = True

    for root, dirs, files in os.walk(inAFolderPath):
        pathsplits = root.strip().split(inAFolderPath)
        appendpath = pathsplits[1]
        if appendpath:
            appendpath = appendpath[1:]
        for file in files:
            AFilePath = os.path.join(root, file)
            destFilePath = ''
            if appendpath:
                destFilePath = os.path.join(indestFolderPath, appendpath, file)
                # print('----compareSrcFolder, 111  %s'%(destFilePath))
            else:
                destFilePath = os.path.join(indestFolderPath, file)
                # print('----compareSrcFolder, 222  %s  %s  %s'%(indestFolderPath,file))

            if bCopyAFile and file.endswith('.uc'):
                if not os.path.exists(destFilePath):
                    result.add_svnFile(os.path.dirname(destFilePath), file)
                copyResult = copy_dir_file(AFilePath, destFilePath)
                if copyResult.returncode == 0:
                    result.add_copyAFile(os.path.dirname(AFilePath), file)
                else:
                    errStr = copyResult.stderr.decode('gbk')
                    errStr = errStr.rstrip('\r\n')
                    Atime = getFileTime(AFilePath)
                    desttime = getFileTime(destFilePath)
                    result.CopyFileError.append('%s\t%s\t%s\tA工程时间：%s' % (errStr, destFilePath, desttime, Atime))
            else:
                compareFile(destFilePath, AFilePath, file, result)

    return


def compareBProjFolder(indestFolderPath, inAFolderPath, inFolderName, inAuthorityFolderList, result):
    print('----compareBProjFolder, \t%s \t%s\t%s ' % (inFolderName, indestFolderPath, inAFolderPath))
    # 忽略指定文件同步
    for tIngorName in result.IgnorName:
        if len(tIngorName) > 0 and tIngorName in inFolderName:
            result.add_ignoreFile(inAFolderPath, inFolderName)
            print('----compareBProjFolder---IgnorFolder, \t%s ' % (inAFolderPath))
            return

    # 完全信任A工程
    bAAuthority = False
    if inFolderName in inAuthorityFolderList.keys():
        bAAuthority = True
        # 资源文件需要逐个拷贝，不能全部移植，因为A工程资源文件只包含特定地图相关资源
        if not os.path.exists(indestFolderPath):
            copyResult = copy_dir_file(inAFolderPath, indestFolderPath)
            if copyResult.returncode == 0:
                result.add_svnFile(os.path.dirname(indestFolderPath), inFolderName)
                result.add_copyAAsset(os.path.dirname(indestFolderPath), inFolderName)
            else:
                errStr = copyResult.stderr.decode('gbk')
                errStr = errStr.rstrip('\r\n')
                Atime = getFileTime(inAFolderPath)
                desttime = getFileTime(indestFolderPath)
                result.CopyFileError.append('%s\t%s\t%s\tA工程时间：%s' % (errStr, indestFolderPath, desttime, Atime))
            return

    for root, dirs, files in os.walk(inAFolderPath):
        bIngore = False
        for tIngorName in result.IgnorName:
            if len(tIngorName) > 0 and tIngorName in root:
                result.add_ignoreFile(os.path.dirname(root), os.path.basename(root))
                bIngore = True
                break
        if bIngore:
            continue

        pathsplits = root.strip().split(inAFolderPath)
        appendpath = pathsplits[1]
        destFilePath = ''
        destParentPath = ''
        if appendpath:
            curappendpath = appendpath[1:]
            destParentPath = os.path.join(indestFolderPath, curappendpath)
            # print('----compareBProjFolder, 111  %s'%(destFilePath))
        else:
            destParentPath = indestFolderPath
            # print('----compareBProjFolder, 222  %s  %s  %s'%(indestFolderPath,file))

            # 去除首位空格
            destParentPath = destParentPath.strip()
            # 去除尾部 \ 符号
            destParentPath = destParentPath.rstrip('\\')

        destBProjdir, ABProjdir = getBProjDir(result)
        pathsplits = root.strip().split(ABProjdir)
        appendpath = pathsplits[1]
        appendpath = appendpath.lstrip('\\')
        if appendpath and (appendpath in inAuthorityFolderList.keys()) and inAuthorityFolderList[appendpath]:
            AddSVN_CodeFolderFile(destParentPath, root, result)
            if os.path.exists(destParentPath):
                delResult = del_dir_file(destParentPath)
                if delResult.returncode != 0:
                    errStr = delResult.stderr.decode('gbk')
                    errStr = errStr.rstrip('\r\n')
                    result.CopyFileError.append('删除文件夹错误：请留意该文件夹拷贝，必要时手工拷贝！ %s\t%s' % (errStr, destParentPath))
                    # shutil.move(inAFolderPath,indestFolderPath)
            copyResult = copy_dir_file(root, destParentPath)
            if copyResult.returncode == 0:
                result.add_copyAAsset(os.path.dirname(destParentPath), os.path.basename(destParentPath))
            else:
                errStr = copyResult.stderr.decode('gbk')
                errStr = errStr.rstrip('\r\n')
                Atime = getFileTime(root)
                desttime = getFileTime(destParentPath)
                result.CopyFileError.append('%s\t%s\t%s\tA工程时间：%s' % (errStr, destParentPath, desttime, Atime))
            continue

        for file in files:
            bIngore = False
            for tIngorName in result.IgnorName:
                if len(tIngorName) > 0 and tIngorName in file:
                    result.add_ignoreFile(root, file)
                    bIngore = True
                    print('----compareBProjFolder---IgnorFile, \t%s ' % (os.path.join(root, file)))
                    break

            if bIngore:
                continue

            AFilePath = os.path.join(root, file)

            if not os.path.exists(destParentPath):
                os.makedirs(destParentPath)
                (destParentPath_parent, tempfilename) = os.path.split(destParentPath)
                result.add_svnFile(destParentPath_parent, tempfilename)

            destFilePath = os.path.join(destParentPath, file)

            if bAAuthority or file.endswith('.upk') or file.endswith('.udk') or file.endswith('.bik'):
                # 直接拷贝资源文件
                # if os.path.exists(destFilePath):
                #       os.remove(destFilePath)
                # shutil.copy2(AFilePath,destParentPath)
                if not os.path.exists(destFilePath):
                    result.add_svnFile(destParentPath, file)
                copyResult = copy_dir_file(AFilePath, destFilePath)
                if copyResult.returncode == 0:
                    result.add_copyAAsset(destParentPath, file)
                else:
                    errStr = copyResult.stderr.decode('gbk')
                    # 去除尾部 \n 符号
                    errStr = errStr.rstrip('\r\n')
                    Atime = getFileTime(AFilePath)
                    desttime = getFileTime(destFilePath)
                    result.CopyFileError.append('%s\t%s\t%s\tA工程时间：%s' % (errStr, destFilePath, desttime, Atime))

            else:
                compareFile(destFilePath, AFilePath, file, result)

    return


def exe_cmd_raw_noCheck(cmd, path=None):
    if path:
        print('cd ', path)
        os.chdir(path)
    print(cmd)
    sys.stdout.flush()
    returncode = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # s = returncode.stdout.decode('gbk')
    # s1 = returncode.stderr.decode('gbk')
    return returncode


def del_dir_file_os(path, result):
    # 使用os命令，递归删除文件
    try:
        if not os.path.exists(path):
            return
        if os.path.isfile(path):
            os.remove(path)
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
    except Exception as e:
        result.add_error_Other(e)


def del_dir_file(FilePath):
    s = FilePath.replace('/', '\\')
    if os.path.islink(s) or os.path.isfile(s):
        return exe_cmd_raw_noCheck('del /f /s /q \"%s\"' % s)
    elif os.path.isdir(s):
        return exe_cmd_raw_noCheck('rd /s /q \"%s\"' % s)


def copy_dir_file(SrcDirFile, DestDir):
    src = SrcDirFile.replace('/', '\\')
    dest = DestDir.replace('/', '\\')

    if os.path.islink(src) or os.path.isfile(src):
        copyResult = exe_cmd_raw_noCheck('copy /Y %s %s' % (src, dest))
        if copyResult.returncode != 0:
            # 文件有可能是加锁的
            if 'BProj\Content\Avatar\WeaponItem' in DestDir:
                addresult, addmessage = SVNClient.getlock(os.path.dirname(dest), os.path.basename(dest))
                if addresult:
                    copyResult = exe_cmd_raw_noCheck('copy /Y %s %s' % (src, dest))
        return copyResult

    elif os.path.isdir(src):
        if dest[-1:] != '\\': dest += '\\'
        return exe_cmd_raw_noCheck('xcopy %s %s /y /h /e /f /c' % (src, dest))


def start_cmd(cmd, path=None, bWaitEnd=True):
    if path:
        print('cd ', path)
        os.chdir(path)
    print(cmd)
    p = subprocess.Popen(cmd)
    if bWaitEnd:
        p.wait()
        return p.returncode;
    return None


def print_dict_result(resultFile, result_dict):
    index = 1
    indexA = 1
    for key in result_dict.keys():
        resultFile.write('%s\t%s\n' % (index, key))
        index = index + 1
        indexA = 1
        for file in result_dict[key]:
            if indexA < 10:
                resultFile.write('\t(%s)\t%s\n' % (indexA, file))
            else:
                resultFile.write('\t(%s)\t%s\n' % (indexA, file))
            indexA = indexA + 1


def print_list_result(resultFile, result_list):
    index = 1
    for file in result_list:
        resultFile.write('%s\t%s\n' % (index, file))
        index = index + 1


def mergeACode():
    resultObj = resultmessgae()
    # 读取Config.py中的配置
    resultObj.AProjectDir = Config.AProjectDir;
    if Config.bMergeBranch == True:
        # resultObj.SVN_PATH = Config.SVN_PATH_Branch
        resultObj.DestProjectDir = Config.DestProjectDir_Branch
        resultObj.AuthoritySrcFolderList = Config.AuthoritySrcFolderList_Branch
        resultObj.AuthorityContentFolderList = Config.AuthorityContentFolderList_Branch
        resultObj.IgnorName = Config.IgnorName_Branch
    else:
        # resultObj.SVN_PATH = Config.SVN_PATH
        resultObj.DestProjectDir = Config.DestProjectDir
        resultObj.AuthoritySrcFolderList = Config.AuthoritySrcFolderList
        resultObj.AuthorityContentFolderList = Config.AuthorityContentFolderList
        resultObj.IgnorName = Config.IgnorName

    A_fullPath = os.path.dirname(resultObj.AProjectDir)
    if not os.path.exists(A_fullPath):
        resultObj.add_error_Other('没有找到A工程代码目录：%s' % (A_fullPath))
        return;

    # 先删除A工程export文件夹
    if os.path.exists(resultObj.AProjectDir):
        delResult = del_dir_file(resultObj.AProjectDir)
        if delResult.returncode != 0:
            errStr = delResult.stderr.decode('gbk')
            errStr = errStr.rstrip('\r\n')
            result.CopyFileError.append('A path export文件夹删除失败，请手工操作！ %s\t%s' % (errStr, AProjectDir))
            # del_dir_file_os(resultObj.AProjectDir,resultObj)
    # UpdateGitFile(A_fullPath)
    start_cmd('cmd.exe /c VersionExport.bat', A_fullPath)

    # dest_fullPath = resultObj.DestProjectDir
    # SVNClient.update(dest_fullPath)
    # UpdateSvnFile(dest_fullPath)

    compareSrcFolders(resultObj)
    compareBProjFolders(resultObj)

    for parent_path in resultObj.NeedSVNAdd.keys():
        for file in resultObj.NeedSVNAdd[parent_path]:
            # AddSvnFile(parent_path,file)
            addresult, addmessage = SVNClient.add(parent_path, file)
            if not addresult:
                # resultObj.add_error_Other(addmessage)
                resultObj.OtherError.append(addmessage)

            curpath = os.path.join(parent_path, file)
            if os.path.isdir(curpath):
                resultObj.OtherError.append("[%s]为文件夹，svn commit时，请留意svn add该文件夹操作！有可能svn add没有成功", curpath)

    # 将信息写入文件
    resultpath = os.path.dirname(os.path.abspath(__file__))

    resultFile = open(os.path.join(resultpath, 'result.txt'), 'w')
    resultFile.write('------------------需要手动合入的文件---------------\n')
    print_dict_result(resultFile, resultObj.NeedCheckFile)

    resultFile.write('\n\n')
    resultFile.write('------------------根据路径没有找到A工程对应文件---------------\n')
    print_list_result(resultFile, resultObj.FileExistError)

    resultFile.write('\n\n')
    resultFile.write('------------------拷贝错误---------------\n')
    print_list_result(resultFile, resultObj.CopyFileError)

    resultFile.write('\n\n')
    resultFile.write('------------------其他错误---------------\n')
    print_list_result(resultFile, resultObj.OtherError)

    resultFile.write('\n\n')
    resultFile.write('------------------主线或分支忽略合入的A工程文件---------------\n')
    print_dict_result(resultFile, resultObj.IgnorFile)

    resultFile.write('\n\n')
    resultFile.write('------------------完全拷贝A工程的代码文件---------------\n')
    print_dict_result(resultFile, resultObj.CopyAFile)

    resultFile.write('\n\n')
    resultFile.write('------------------完全拷贝A工程的资源文件---------------\n')
    print_dict_result(resultFile, resultObj.CopyAAsset)

    resultFile.write('\n\n')
    resultFile.write('------------------主线或分支新加文件---------------\n')
    print_dict_result(resultFile, resultObj.DestNewAddFile)

    resultFile.close()
    return


if __name__ == '__main__':
    mergeACode()

