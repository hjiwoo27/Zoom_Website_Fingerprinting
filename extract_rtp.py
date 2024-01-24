import struct

def extract_rtp_header(udp_payload):
    # UDP 페이로드에서 처음 12바이트를 RTP 헤더로 추출
    rtp_header = udp_payload[:12]

    # RTP 헤더 추출
    if len(udp_payload) >= 12:
        return rtp_header
    else:
        return None

def extract_ssrc_from_rtp_header(rtp_header):
    # RTP 헤더의 8~11바이트에서 SSRC 추출
    ssrc_bytes = rtp_header[8:12]

    # 바이트를 정수로 변환
    ssrc = struct.unpack('!I', ssrc_bytes)[0]

    return ssrc

# 16진수 페이로드를 bytes로 변환
hex_payload = ""
udp_payload_example = bytes.fromhex(hex_payload)

# RTP 헤더 추출
rtp_header_extracted = extract_rtp_header(udp_payload_example)

# RTP 헤더에서 SSRC 추출
if rtp_header_extracted:
    ssrc_id = extract_ssrc_from_rtp_header(rtp_header_extracted)
    print("Extracted SSRC ID:", ssrc_id)
else:
    print("Failed to extract RTP Header.")
