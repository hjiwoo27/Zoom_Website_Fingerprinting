import pyshark

def extract_ssrc(packet):
    try:
        if 'rtp' in packet:
            #print("rtp")
            return packet.rtp.ssrc
        else:
            #print("no")
            return None
    except AttributeError:
        return None

def analyze_pcap(pcap_file):
    # 각 SSRC 값의 개수를 저장할 딕셔너리
    ssrc_counts = {}

    # pcap 파일을 열고 RTP 패킷의 SSRC 값을 추출하여 딕셔너리에 저장
    capture = pyshark.FileCapture(pcap_file)
    for packet in capture:
        ssrc = extract_ssrc(packet)
        print(ssrc)
        if ssrc is not None:
            if ssrc in ssrc_counts:
                ssrc_counts[ssrc] += 1
            else:
                ssrc_counts[ssrc] = 1

    # 결과 출력
    print("SSRC 값 종류 및 개수:")
    for ssrc, count in ssrc_counts.items():
        print(f"SSRC: {ssrc}, 개수: {count}")

# pcap 파일 경로 설정
pcap_file = "C:/Users/ghdwl/Desktop/새 폴더/captured_traffic_2024-02-06_23-06-11.pcap."

# pcap 파일 분석 및 결과 출력
analyze_pcap(pcap_file)

