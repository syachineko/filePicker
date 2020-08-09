#!/usr/bin/python

# やりたいこと
# 特定のホストに対して、全部のディレクトリをSCPで取得
# -t分前のファイルをとってこれるように
# 
# 

# モジュール読み込み
import sys
import scp
import paramiko

# 引数チェック
args = sys.argv # 引数でやりたいのはさかのぼり時間、フォルダ名
print("X分前:", args[1], "ファイルパス:" , args[2])
TIME = args[1]
FILE_PATH = args[2]

# 初期設定読み込み
hosts = ["192.168.3.15"] # TODO 外部ファイル化
user  = "kali"
pswd  = "kali"
HOME_DIR = "/home/kali/SyachinekoLab/"
WORK_DIR = "/box/"
indexList = []

# ホストに接続
print("---START GET FILE---")
try:
  for ip in hosts:

    # SSH/SCP接続
    with paramiko.SSHClient() as ssh:
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(hostname=ip, port=22, username=user, password=pswd)

      # lsで対象ファイルをピックアップする
      stdin, stdout, stderr = ssh.exec_command('find '+HOME_DIR+' -mmin -'+TIME+' -type f')
      fileList = []
      for i in stdout:
        fileList.append(i.strip())

      # フォルダとリストの作成
      stdin, stdout, stderr = ssh.exec_command('mkdir -p '+WORK_DIR)
      indexItem = ip

      # scp clientオブジェクト生成
      with scp.SCPClient(ssh.get_transport()) as scp:
        
        # 取得したファイル数分だけSCPで取得する
        print(fileList)
        for fileName in fileList:
          print(fileName)
          scp.get(fileName,'.'+WORK_DIR)
          indexItem += " "+fileName

    # リストを作る
    indexList.append(indexItem)
    indexItem = ""

# 例外処理
except Exception as err:
  print("GET FILE ERROR!! : ", err)

# 結果を表示する


# サマリファイルを作成する
print(indexList)
output = "---SUMMARY---\n"
output += "---EXIST IP---\n"
for i in range(len(indexList)):
  itemList = list(indexList[i].split())
  output += str(i+1)+" : "+itemList[0]+"\n"
  for j in range(1,len(itemList)):
    output += itemList[j]+"\n"

print(output)

# 終了
print("---END PGM---")

