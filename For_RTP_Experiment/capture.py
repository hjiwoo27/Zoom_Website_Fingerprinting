import os
import subprocess
import signal
import time
import psutil

def clean_exit(signum, frame):
    print("\nStopping capture and exiting safely\n")
    # Find and terminate the tcpdump process
    for process in psutil.process_iter(['pid', 'name']):
        if 'dumpcap.exe' in process.info['name']:
            os.kill(process.info['pid'], signal.SIGINT)
    exit(1)

# 스크립트가 종료되기 전에 SIGINT 시그널을 수신하면 clean_exit() 실행해서 프로그램 종료
signal.signal(signal.SIGINT, clean_exit)

# wav 파일(random voice) 및 output pcap 파일이 저장될 directory 설정
output_path = "C:/Users/ghdwl/Desktop/"

# 현재 시간을 가져와서 output file 이름으로 설정
current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
output_file = f"{output_path}captured_traffic_{current_time}.pcap"

# 캡쳐할 시간 설정 (초 단위)
capture_duration = 300  # 5분 = 300초

# 파일명에 시간을 포함하여 설정
output_file = f"captured_traffic_{current_time}.pcap"

# Wireshark의 dumpcap.exe 파일 경로 설정
dumpcap_path = r"C:\Program Files\Wireshark\dumpcap.exe"

# tcpdump 실행하여 트래픽 캡쳐
subprocess.Popen([dumpcap_path, "-i", "Wi-Fi", "-w", output_file, "-a", f"duration:{capture_duration}"])

# 시작 시간 기록
start_time = time.time()

while True:
    # 현재 시간 기록
    current_time = time.time()

    # 5분(300초)이 지나면 스크립트 종료
    if current_time - start_time >= 300:
        break

clean_exit(0, 0)
