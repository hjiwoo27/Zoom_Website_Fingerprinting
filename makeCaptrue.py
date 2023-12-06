#pip install paramiko

import paramiko

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

# 라즈베리파이 1에서 코드 실행
command_pi1 = "python3 /path/to/your/code_pi1.py"  # 라즈베리파이 1의 코드 경로
ssh_connect_execute(pi1_ip, pi1_username, pi1_password, command_pi1)

# 라즈베리파이 2에서 코드 실행
command_pi2 = "python3 /path/to/your/code_pi2.py"  # 라즈베리파이 2의 코드 경로
ssh_connect_execute(pi2_ip, pi2_username, pi2_password, command_pi2)
