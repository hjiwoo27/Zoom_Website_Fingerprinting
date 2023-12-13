#pip install paramiko

import paramiko
import requests
import webbrowser

# replace with your client ID
client_id = "QX86YwYdT2amJYaqzM9rpA" 

# replace with your account ID
account_id = "V71JeUj6SRiuTLpz4vntSA" 

# replace with your client secret
client_secret = "vR4BunfZMGznDLD6DSeKhY6rt7HFYGSK" 

auth_token_url = "https://zoom.us/oauth/token"
api_base_url = "https://api.zoom.us/v2"

MEETING_TOPIC = '회의 주제'
MEETING_DURATION = 5  # 회의 지속 시간(분)
TIMEZONE = 'Asia/Seoul'  # 원하는 타임존


# create the Zoom link function
def create_meeting(topic, duration, TIMEZONE):
        data = {
        "grant_type": "account_credentials",
        "account_id": account_id,
        "client_secret": client_secret
        }
        response = requests.post(auth_token_url, 
                                 auth=(client_id, client_secret), 
                                 data=data)
        
        if response.status_code!=200:
            print("Unable to get access token")
        response_data = response.json()
        access_token = response_data["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "topic": topic,
            "duration": duration,
            'timezone': TIMEZONE,
            "type": 2
        }

        resp = requests.post(f"{api_base_url}/users/me/meetings", 
                             headers=headers, 
                             json=payload)
        
        if resp.status_code!=201:
            print("Unable to generate meeting link")
        response_data = resp.json()
        
        content = {
                    "meeting_url": response_data["join_url"], 
                    "password": response_data["password"],
                    "meetingTime": response_data["start_time"],
                    "purpose": response_data["topic"],
                    "duration": response_data["duration"],
                    "message": "Success",
                    "status":1
        }
        print(content)
        
        
        return response_data["join_url"]

zoom_url=create_meeting(MEETING_TOPIC, MEETING_DURATION, TIMEZONE)


# 라즈베리파이 IP, 사용자 이름, 비밀번호 설정
pi1_ip = '192.168.0.47'
pi1_username = 'aisec'
pi1_password = 'aisec'


# SSH 연결 함수
def ssh_connect_execute(ip, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=ip, username=username, password=password)
        print(f"{ip}에 SSH 연결 성공")

        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())

    except paramiko.AuthenticationException:
        print(f"{ip}에 인증 실패. 사용자 이름 또는 비밀번호를 확인하세요.")
    except paramiko.SSHException as e:
        print(f"{ip}에 SSH 연결 실패:", str(e))
    finally:
        client.close()

def send_ssh_message(ip_address, username, password, message):
    # SSH 클라이언트 생성
    client = paramiko.SSHClient()

    # 호스트 키를 확인하지 않음 (실제 운영 시에는 보안을 위해 필요한 조치)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # SSH 서버에 연결
        client.connect(ip_address, username=username, password=password)

        # SSH로 명령 전송
        command = f'echo "{message}"'
        stdin, stdout, stderr = client.exec_command(command)

        # 실행 결과 출력
        print(stdout.read().decode('utf-8'))

    except paramiko.AuthenticationException as auth_error:
        print(f"인증 에러: {auth_error}")
    except paramiko.SSHException as ssh_error:
        print(f"SSH 에러: {ssh_error}")
    finally:
        # SSH 연결 닫기
        client.close()

# 노트북 정보 입력 (IP 주소, 사용자 이름, 비밀번호)
notebook_ip = '192.168.76.62'
username = 'DESKTOP-BA9F2N8/swn'
password = ''


# user 2에서 코드 실행
# 보낼 메시지
message_to_send = f"python C:/Users/swu/Desktop/output/code/openZoom.py  {zoom_url}"

# SSH 메시지 전송
send_ssh_message(notebook_ip, username, password, message_to_send)

def join_zoom_meeting(meeting_link):
    webbrowser.open(meeting_link)

received_zoom_link = zoom_url
join_zoom_meeting(received_zoom_link)

# 라즈베리파이 1에서 코드 실행
command_pi1 = "bash /home/aisec/Desktop/Zoom_fingerprinting--main/capture.sh"  # 라즈베리파이 1의 코드 경로
ssh_connect_execute(pi1_ip, pi1_username, pi1_password, command_pi1)

# 보낼 메시지
message_to_send = "python C:/Users/swu/Desktop/output/code/captureOnUser.sh"

# SSH 메시지 전송
send_ssh_message(notebook_ip, username, password, message_to_send)
