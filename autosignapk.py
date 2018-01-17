import os
import subprocess
import sys
import zipfile
import shutil

keystore="D:\\autosign\\xxxx.keystore"
storepass="xxxxxx"
keypass="xxxxxx"
alias="xxxxxx"
originpath = "D:\\autosign\\originpacks\\"
targetpath = "D:\\autosign\\signedpacks\\"
old_sign = "META-INF"


L=[]
Lname=[]
Lsigned = []

#对APK包进行签名
def signApk(src, target):
  signedCmd="jarsigner -verbose -keystore "+keystore+" -storepass "+storepass +" -keypass "+keypass+" -signedjar "+target+" "+src+" "+alias
  print("-----signApk-----"+signedCmd)
  subprocess.call(signedCmd)
  #print("-----signedApk:"+target)
  Lsigned.append(target)

#获取目标路径下所有文件名
def listdir(path, list_name):
  for file in os.listdir(path):
    file_path = os.path.join(path, file)
    #print("file:"+file)
    if os.path.isdir(file_path):
      listdir(file_path, list_name)
    elif os.path.splitext(file_path)[1]=='.apk':
      list_name.append(file_path)
      #print("--"+file_path)
      Lname.append(file)
      #print("--"+file)

#删除原有包中的签名信息
def deloldsign(file):
  zin = zipfile.ZipFile ("%s%s"%(originpath,file), 'r')
  zout = zipfile.ZipFile("%snew_%s"%(originpath,file),'w')
  for item in zin.infolist():
    #print("item.filename:"+item.filename)
    buffer = zin.read(item.filename)
    if not(item.filename.startswith(old_sign)):
      zout.writestr(item, buffer)
  zout.close()
  zin.close()
  #新的压缩文件替换原有文件
  shutil.move("%snew_%s"%(originpath,file),"%s%s"%(originpath,file)) 

if __name__=="__main__":
  print("-----")
  listdir(originpath,L)
  for i in Lname:
    deloldsign(i)
  for i in L:
    #deloldsign(Lname[L.index(i)])
    signApk("%s"%i,"%ssign_%s"%(targetpath,Lname[L.index(i)]))
  for i in Lsigned:
    print("----signedApk: "+i)