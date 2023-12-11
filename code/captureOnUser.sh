#!/bin/bash

# 스크립트가 종료되기 전에 SIGINT 시그널을 수신하면 clean_exit() 실행해서 프로그램 종료
trap "clean_exit" SIGINT
clean_exit() {
  echo -e "\nStopping capture and exiting safely\n"
  sudo pkill -2 tcpdump
  exit 1
}

# output pcap 파일이 저장될 directory 설정 
output_path="C:\Users\swu\Desktop\output"

# 현재 시간을 가져와서 output file 이름으로 설정 
current_time=$(date +'%Y-%m-%d_%H-%M-%S')

output_file="${output_path}captured_traffic_${current_time}.pcap"

# 캡쳐할 시간 설정 (초 단위)
capture_duration=300  # 5분 = 300초

# 파일명에 시간을 포함하여 설정
output_file="captured_traffic_${current_time}.pcap"

# tcpdump 실행하여 트래픽 캡쳐
sudo tcpdump -U -i wlan0 -w $output_file -G $capture_duration -Z root &


# 시작 시간 기록
start_time=$(date +%s)


sudo pkill -2 tcpdump
clean_exit
