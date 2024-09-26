#!/usr/bin/env python3

# merged.py
import rospy
from std_msgs.msg import String
import json

# 전역 변수로 각 센서 데이터를 저장할 변수를 선언합니다.
imu_data = None
lidar_data = None
gps_data = None

# IMU 데이터 콜백 함수
def imu_callback(data):
    global imu_data
    imu_data = data.data  # 가공된 IMU 데이터를 저장

# LiDAR 데이터 콜백 함수
def lidar_callback(data):
    global lidar_data
    lidar_data = data.data  # 가공된 LiDAR 데이터를 저장

# GPS 데이터 콜백 함수
def gps_callback(data):
    global gps_data
    gps_data = data.data  # 가공된 GPS 데이터를 저장

# 데이터 병합 함수
def merge_and_publish():
    if imu_data is not None and lidar_data is not None and gps_data is not None:
        # 병합된 데이터 생성
        merged_data = {
            "processed_imu": imu_data,
            "processed_lidar": lidar_data,
            "processed_gps": gps_data
        }
        # 병합된 데이터를 JSON 형태로 퍼블리시
        merged_msg = String()
        merged_msg.data = json.dumps(merged_data)
        merged_pub.publish(merged_msg)  # 병합된 데이터를 새로운 토픽에 퍼블리시
        rospy.loginfo("Merged Data Published")

def merged_data_node():
    rospy.init_node('merged_data_node', anonymous=True)

    # 각각의 가공된 센서 데이터를 구독합니다.
    rospy.Subscriber('/processed/imu', String, imu_callback)
    rospy.Subscriber('/processed/lidar', String, lidar_callback)
    rospy.Subscriber('/processed/gps', String, gps_callback)

    # 병합된 데이터를 퍼블리시할 새로운 토픽 설정
    global merged_pub
    merged_pub = rospy.Publisher('/processed/merged', String, queue_size=10)

    # 병합된 데이터를 주기적으로 퍼블리시하기 위해 10Hz 주기로 루프를 설정
    rate = rospy.Rate(10)  # 10Hz
    while not rospy.is_shutdown():
        merge_and_publish()
        rate.sleep()

if __name__ == '__main__':
    try:
        merged_data_node()
    except rospy.ROSInterruptException:
        pass
