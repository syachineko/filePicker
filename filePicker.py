#!/usr/bin/python

# やりたいこと
# 特定のホストに対して、全部のディレクトリをSCPで取得
# -t分前のファイルをとってこれるように
# 
# 

# モジュール読み込み
import sys          # ファイル動作に必要
import scp          # SCPに必要
import paramiko     # SCPに必要
import configparser # コンフィグ読み込みに必要
import os

# コンフィグ読み込み
config = configparser.ConfigParser() # object作成
config.read('targetList.ini',encoding='utf-8') # 読み込み
cnf=config['SETTINGS']

# 初期設定読み込み
hosts = cnf["ipLists"].split(":")
user  = cnf["user"]
pswd  = cnf["pswd"]
HOME_DIR = cnf["homeDir"]
WORK_DIR = cnf["workDir"]
SUMMARY  = cnf["summaryFileName"]
indexList = []

# フォルダ作成
try:
  os.mkdir(WORK_DIR)
except Exception as err:
  pass

# 引数チェック
args = sys.argv # 引数でやりたいのはさかのぼり時間、フォルダ名
print("X分前:", args[1], "ファイルパス:" , args[2])
TIME = args[1]
FILE_PATH = args[2]

# ホストに接続
print("---START GET FILE---")
try:
  for ip in hosts:

    # フォルダとリストの作成
    indexItem = ip

    # SSH/SCP接続
    with paramiko.SSHClient() as ssh:
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(hostname=ip, port=22, username=user, password=pswd)

      # lsで対象ファイルをピックアップする
      stdin, stdout, stderr = ssh.exec_command('find '+HOME_DIR+' -mmin -'+TIME+' -type f')
      fileList = []
      for i in stdout:
        fileList.append(i.strip())

      # scp clientオブジェクト生成
      with scp.SCPClient(ssh.get_transport()) as scp:
        
        # 取得したファイル数分だけSCPで取得する
        for fileName in fileList:
          print("get file from "+fileName)
          scp.get(fileName,'./'+WORK_DIR)
          indexItem += " "+fileName

    # リストを作る
    indexList.append(indexItem)
    indexItem = ""

# 例外処理
except Exception as err:
  print("GET FILE ERROR!! : ", err)

# サマリファイルを作成する
output = "---SUMMARY---\n"

for i in range(len(indexList)):
  itemList = list(indexList[i].split())
  output += str(i+1)+" : "+itemList[0]+"\n"

  for j in range(1,len(itemList)):
    output += itemList[j]+"\n"

# 画面出力およびファイルへの書き込み
print(output)
with open(SUMMARY, mode='w') as f:
    f.write(output)

# 終了
print("---END PGM---")

