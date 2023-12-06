#!/bin/bash

# 스크립트가 종료되기 전에 SIGINT 시그널을 수신하면 clean_exit() 실행해서 프로그램 종료
trap "clean_exit" SIGINT
clean_exit() {
  echo -e "\nStopping capture and exiting safely\n"
  sudo pkill -2 tcpdump
  exit 1
}

# wav파일(random voice) & output pcap 파일이 저장될 directory 설정 
folder_path="/home/aisec/Desktop/Zoom_fingerprinting--main/random_voice/"
output_path="/home/aisec/Desktop/Zoom_fingerprinting--main/output_files/"

# 현재 시간을 가져와서 output file 이름으로 설정 
current_time=$(date +'%Y-%m-%d_%H-%M-%S')

# 캡쳐할 시간 설정 (초 단위)
capture_duration=300  # 5분 = 300초

# 파일명에 시간을 포함하여 설정
output_file="${output_path}captured_traffic_${current_time}.pcap"

# tcpdump 실행하여 트래픽 캡쳐
sudo tcpdump -U -i wlan0 -w $output_file -G $capture_duration -Z root &

# 시작 시간 기록
start_time=$(date +%s)

while true; do
    # 현재 시간 기록
    current_time=$(date +%s)

    # 5분(300초)이 지나면 스크립트 종료
    if ((current_time - start_time >= 300)); then
        break
    fi

    # 해당 폴더에서 무작위로 WAV 파일 선택
    random_wav=$(ls $folder_path/*.wav | shuf -n 1)

    # 선택된 WAV 파일 실행
    paplay "$random_wav"

    # 무작위 대기 시간 생성 (5~20초 사이)
    random_sleep=$(shuf -i 5-20 -n 1)
    echo "다음 WAV 파일까지 대기 시간: $random_sleep 초"
    sleep $random_sleep
done

sudo pkill -2 tcpdump
clean_exit
