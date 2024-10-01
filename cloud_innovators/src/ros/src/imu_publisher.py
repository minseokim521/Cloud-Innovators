#!/usr/bin/env python

import rospy
import os
from sensor_msgs.msg import Imu
from std_msgs.msg import Header

# 폴더 내 모든 txt 파일에서 IMU 데이터를 읽고 Imu 메시지로 변환하는 함수
def read_imu_from_txt(folder_path):
    # 폴더 내 모든 .txt 파일 목록을 가져옴
    txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])
    
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        with open(file_path, 'r') as f:
            for line in f:
                data = line.strip().split()
                # 가속도 및 각속도 정보 추출
                linear_acceleration_x = float(data[11])
                linear_acceleration_y = float(data[12])
                angular_velocity_z = float(data[18])
                yield linear_acceleration_x, linear_acceleration_y, angular_velocity_z

# IMU 데이터를 퍼블리시하는 함수
def imu_publisher():
    rospy.init_node('imu_publisher', anonymous=True)

    # IMU 데이터를 퍼블리시할 Publisher 설정
    imu_pub = rospy.Publisher('/sensor_data/imu', Imu, queue_size=10)

    # 텍스트 파일들이 저장된 폴더 경로
    folder_path = '/home/minseokim521/cloud_innovators/src/point_cloud_data/2011_09_26_drive_0009_sync/2011_09_26/2011_09_26_drive_0009_sync/oxts/data'

    rate = rospy.Rate(10)  # 10Hz로 퍼블리시

    # 폴더 내 모든 txt 파일에서 데이터를 읽어옴
    for linear_acceleration_x, linear_acceleration_y, angular_velocity_z in read_imu_from_txt(folder_path):
        # Imu 메시지 생성 및 데이터 할당
        imu_msg = Imu()
        imu_msg.header = Header()
        imu_msg.header.stamp = rospy.Time.now()
        
        # 가속도 데이터 설정 (단위는 m/s^2)
        imu_msg.linear_acceleration.x = linear_acceleration_x
        imu_msg.linear_acceleration.y = linear_acceleration_y
        imu_msg.linear_acceleration.z = 0  # z축 값이 없는 경우 0으로 설정
        
        # 각속도 데이터 설정 (단위는 rad/s)
        imu_msg.angular_velocity.x = 0  # x축 값이 없는 경우 0으로 설정
        imu_msg.angular_velocity.y = 0  # y축 값이 없는 경우 0으로 설정
        imu_msg.angular_velocity.z = angular_velocity_z

        # 퍼블리시
        imu_pub.publish(imu_msg)

        rate.sleep()  # 10Hz로 퍼블리시

if __name__ == '__main__':
    try:
        imu_publisher()
    except rospy.ROSInterruptException:
        pass
