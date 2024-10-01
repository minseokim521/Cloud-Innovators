#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String
import json
import sensor_msgs.point_cloud2 as pc2

# 전역 변수로 각 센서 데이터를 저장할 변수를 선언합니다.
imu_data = None
lidar_data = None
gps_data = None

# IMU 데이터 콜백 함수
def imu_callback(data):
    global imu_data
    imu_data = data.data  # 가공된 IMU 데이터를 저장

# LiDAR 데이터 콜백 함수 (PointCloud2 형식)
def lidar_callback(data):
    global lidar_data
    # LiDAR 데이터를 처리 (여기서는 포인트 수를 계산해 저장하는 방식 예시)
    points = [p for p in pc2.read_points(data, field_names=("x", "y", "z"), skip_nans=True)]
    lidar_data = f"PointCloud with {len(points)} points"  # 포인트 클라우드 데이터 크기만 예시로 저장

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
            "processed_lidar": lidar_data,  # PointCloud2 데이터의 일부 정보만 저장
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
    rospy.Subscriber('/processed/lidar', PointCloud2, lidar_callback)  # PointCloud2 형식으로 변경
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
