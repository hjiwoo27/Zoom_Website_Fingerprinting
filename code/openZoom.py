'''
import webbrowser

def join_zoom_meeting(meeting_link):
    webbrowser.open(meeting_link)

# Zoom 회의 링크를 받았다고 가정하고 해당 링크를 변수에 저장합니다.
received_zoom_link = "https://us05web.zoom.us/j/85374442964?pwd=9zWcheAMa95naQLZ8ibcLGnsDBreeV.1"

join_zoom_meeting(received_zoom_link)
'''


import webbrowser
import sys

def process_zoom_link(zoom_link):
    # Zoom 링크를 웹 브라우저로 열기
    webbrowser.open(zoom_link)

if __name__ == "__main__":
    # 명령어로부터 전달된 매개변수 확인
    if len(sys.argv) > 1:
        # 첫 번째 매개변수로 전달된 Zoom 링크 사용
        zoom_link = sys.argv[1]
        process_zoom_link(zoom_link)
    else:
        print("Zoom 링크가 전달되지 않았습니다.")
