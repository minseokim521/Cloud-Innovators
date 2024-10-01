#!/usr/bin/env python

import rospy
import os
import numpy as np
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs.point_cloud2 as pc2
from std_msgs.msg import Header

# .bin 파일에서 LiDAR 데이터를 읽어 PointCloud2 메시지로 변환하는 함수
def read_lidar_from_bin(file_path):
    # bin 파일을 읽어서 N x 4 형태의 포인트 클라우드 데이터로 변환 (x, y, z, reflectance)
    point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    
    # PointCloud2 메시지를 생성하고 데이터 할당
    header = Header()
    header.stamp = rospy.Time.now()
    header.frame_id = 'velodyne'

    fields = [
        PointField('x', 0, PointField.FLOAT32, 1),
        PointField('y', 4, PointField.FLOAT32, 1),
        PointField('z', 8, PointField.FLOAT32, 1),
        PointField('intensity', 12, PointField.FLOAT32, 1),
    ]

    # PointCloud2 메시지 생성
    point_cloud_msg = pc2.create_cloud(header, fields, point_cloud)
    return point_cloud_msg

# LiDAR 데이터를 퍼블리시하는 함수
def lidar_publisher():
    rospy.init_node('lidar_publisher', anonymous=True)

    # LiDAR 데이터를 퍼블리시할 Publisher 설정
    lidar_pub = rospy.Publisher('/sensor_data/lidar', PointCloud2, queue_size=10)

    # bin 파일들이 저장된 폴더 경로
    folder_path = '/home/minseokim521/cloud_innovators/src/point_cloud_data/2011_09_26_drive_0009_sync/2011_09_26/2011_09_26_drive_0009_sync/velodyne_points/data'

    rate = rospy.Rate(10)  # 10Hz로 퍼블리시

    # 폴더 내 모든 bin 파일에서 데이터를 읽어옴
    bin_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.bin')])

    for bin_file in bin_files:
        file_path = os.path.join(folder_path, bin_file)
        
        # bin 파일에서 LiDAR 데이터를 읽어 PointCloud2 메시지로 변환
        point_cloud_msg = read_lidar_from_bin(file_path)
        
        # 퍼블리시
        lidar_pub.publish(point_cloud_msg)
        
        rate.sleep()  # 10Hz로 퍼블리시

if __name__ == '__main__':
    try:
        lidar_publisher()
    except rospy.ROSInterruptException:
        pass
