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
        print("\n줌 링크 :",{response_data["join_url"]})

create_meeting(MEETING_TOPIC, MEETING_DURATION, TIMEZONE)


