#pip install paramiko

import paramiko
import requests

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
pi1_ip = '192.168.76.61'
pi1_username = 'aisec'
pi1_password = 'aisec'

pi2_ip = '192.168.76.62'
pi2_username = 'aisec'
pi2_password = 'aisec'

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



# user 2에서 코드 실행
command_pi2 = "python openZoom.py zoom_url"  # user 2의 코드 경로
ssh_connect_execute(pi2_ip, pi2_username, pi2_password, command_pi2)

# 라즈베리파이 1에서 코드 실행
command_pi1 = "python3 /path/to/your/code_pi1.py"  # 라즈베리파이 1의 코드 경로
ssh_connect_execute(pi1_ip, pi1_username, pi1_password, command_pi1)

# user 2에서 코드 실행
command_pi2 = "python captureOnUser.sh"  # user 2의 코드 경로
ssh_connect_execute(pi2_ip, pi2_username, pi2_password, command_pi2)