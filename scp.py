import os
import paramiko
import sys
import pysftp as sftp
from ftplib import FTP

server = "172.16.250.248:122"
username = "root"
password = ""


ftp = FTP(server).login(passwd=password,user=username)
print("czlonek")
#cnopts = sftp.CnOpts()
#cnopts.hostkeys = None
#s = sftp.Connection(host=server, username=username, password=password, cnopts=cnopts)
#
#
#localpath = "C:/YA_MIB3/libs/common/audio_datasets/CL33_V020_MQB"
#remotepath = "/datastorage/dataset_storage/"
#s.put(localpath, remotepath)
#
#s.close()

'''
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()

ssh.connect(server, username, password)
sftp = ssh.open_sftp()

sftp.put(localpath, remotepath)
sftp.close()
ssh.close()
'''