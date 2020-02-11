from ftplib import FTP
import platform
import subprocess
import re
import tempfile
import pathlib

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    param = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.run(command, stdout=subprocess.DEVNULL).returncode == 0

def getRemoteVersion (app_name: str, files):
    if len(files) <= 0:
        print('No filelist provided')
        return False
    
    files.sort()
    newest = files.pop()
    res = re.search(app_name + '.([0-9].[0-9]+.?[0-9]*).exe', newest)
    return(res)

def compareVersion (remote: str, local: str):
    is_newer = False
    rem = remote.split('.')
    loc = local.split('.')
    max_range = max(len(rem), len(loc))
    for idx in range(max_range):
        if rem[idx] > loc[idx]:
            is_newer = True
            break
        elif rem[idx] == loc[idx]:
            is_newer = False
        else:
            is_newer = False
            break
    return is_newer

def downloadInstaller (ftp: FTP, rem_file: str):
    tempdir = tempfile.gettempdir()
    with open(tempdir + '/' + rem_file, "wb") as dl_file:
        print ('Downloading ' + rem_file)
        result = ftp.retrbinary('RETR ' + rem_file, dl_file.write)
        if (result.find('226') != -1):
            return (tempdir + '/' + rem_file)
        else:
            return None

def executeUpdate(app_name, v_local, host, remote_path):
    # open(r'//10.224.181.205/logs/MIB3/logs/PM')
    container=list(pathlib.Path('//10.224.181.205/logs/MIB3/logs/PM').glob('*.exe'))
    print(container[0].name,container[1].name)
    for i,j in enumerate(container):
        print(re.findall("AudioAnalyzer.([0-9].[0-9].[0-9]).exe",j.name))

    # if (ping(host)):
    #     print('Update server available')
    #     with FTP(host = host) as ftp:
    #         result: str = ftp.login()
    #         if (result.find('230') != -1):
    #             ftp.cwd(remote_path)
    #             files = ftp.nlst()
    #             version = getRemoteVersion(app_name, files)
    #             v_remote = version[1]
    #             rem_file = version[0]
    #             if compareVersion(v_remote, v_local):
    #                 print('Update available, your version: ' + v_local + ' remote: ' + v_remote)
    #                 installer_exe = downloadInstaller(ftp, rem_file)
    #                 if(installer_exe != None):
    #                     print('Installer ready')
    #                     try:
    #                         subprocess.Popen([installer_exe],creationflags=subprocess.DETACHED_PROCESS)
    #                         return 0
    #                     except:
    #                         print('Could not run the installer')
    #                         return -4
    #                 else:
    #                     print('Installer not downloaded')
    #                     return -3
    #             else:
    #                 print('You are up to date :)')
    #                 return 1
    #         else:
    #             print('Invalid login')
    #             print(result)
    #             return -2
    # else:
    #     print('Host unavailable')
    #     return -1

if __name__ == "__main__":
    executeUpdate('AudioAnalyzer','0.1.3','10.224.181.205',"logs/MIB3/logs/PM")