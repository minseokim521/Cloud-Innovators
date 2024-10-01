#!/usr/bin/env python

import rospy
import os
from sensor_msgs.msg import NavSatFix

# 폴더 내 모든 txt 파일에서 GPS 데이터를 읽고 NavSatFix 메시지로 변환하는 함수
def read_gps_from_txt(folder_path):
    # 폴더 내 모든 .txt 파일 목록을 가져옴
    txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])
    
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        with open(file_path, 'r') as f:
            for line in f:
                data = line.strip().split()
                # 위도, 경도, 고도 정보 추출
                latitude = float(data[0])
                longitude = float(data[1])
                altitude = float(data[2])
                yield latitude, longitude, altitude

# GPS 데이터를 퍼블리시하는 함수
def gps_publisher():
    rospy.init_node('gps_publisher', anonymous=True)

    # GPS 데이터를 퍼블리시할 Publisher 설정
    gps_pub = rospy.Publisher('/sensor_data/gps', NavSatFix, queue_size=10)

    # 텍스트 파일들이 저장된 폴더 경로
    folder_path = '/home/minseokim521/cloud_innovators/src/point_cloud_data/2011_09_26_drive_0009_sync/2011_09_26/2011_09_26_drive_0009_sync/oxts/data'

    rate = rospy.Rate(10)  # 10Hz로 퍼블리시

    # 폴더 내 모든 txt 파일에서 데이터를 읽어옴
    for latitude, longitude, altitude in read_gps_from_txt(folder_path):
        # NavSatFix 메시지 생성 및 데이터 할당
        navsat_msg = NavSatFix()
        navsat_msg.header.stamp = rospy.Time.now()
        navsat_msg.latitude = latitude
        navsat_msg.longitude = longitude
        navsat_msg.altitude = altitude

        # 퍼블리시
        gps_pub.publish(navsat_msg)

        rate.sleep()  # 10Hz로 퍼블리시

if __name__ == '__main__':
    try:
        gps_publisher()
    except rospy.ROSInterruptException:
        pass
