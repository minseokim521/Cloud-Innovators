#!/usr/bin/env python

import rospy
import numpy as np
import open3d as o3d
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs.point_cloud2 as pc2
from std_msgs.msg import Header

# Voxel Grid Filter 적용 함수
def apply_voxel_grid_filter(points, voxel_size=0.2):
    """
    Voxel Grid 필터를 적용하여 포인트 클라우드 데이터를 다운샘플링합니다.
    :param points: 포인트 클라우드 데이터 (N x 3 배열)
    :param voxel_size: Voxel 크기 (단위: meter)
    :return: 다운샘플링된 포인트 클라우드 배열
    """
    # Open3D 포인트 클라우드 객체로 변환
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])  # x, y, z 좌표 사용

    # Voxel Grid 필터 적용
    downsampled_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
    
    return np.asarray(downsampled_pcd.points)

# LiDAR 데이터를 수신 후 Voxel Grid Filter 적용 및 퍼블리시
def lidar_callback(data):
    rospy.loginfo("LiDAR Data Received")

    # PointCloud2 메시지를 N x 3 포인트 클라우드로 변환
    points = np.array([point[:3] for point in pc2.read_points(data, field_names=("x", "y", "z"), skip_nans=True)])

    # Voxel Grid Filter 적용
    filtered_points = apply_voxel_grid_filter(points, voxel_size=0.2)
    
    # 필터링된 포인트 클라우드를 PointCloud2 형식으로 변환
    header = Header()
    header.stamp = rospy.Time.now()
    header.frame_id = "velodyne"

    fields = [
        PointField('x', 0, PointField.FLOAT32, 1),
        PointField('y', 4, PointField.FLOAT32, 1),
        PointField('z', 8, PointField.FLOAT32, 1),
    ]

    # PointCloud2 메시지 생성
    filtered_point_cloud_msg = pc2.create_cloud(header, fields, filtered_points)
    
    # 필터링된 데이터를 퍼블리시
    lidar_pub.publish(filtered_point_cloud_msg)

def lidar_data_subscriber():
    rospy.init_node('lidar_data_subscriber', anonymous=True)
    
    # LiDAR 데이터를 퍼블리시할 토픽 설정
    global lidar_pub
    lidar_pub = rospy.Publisher('/processed/lidar', PointCloud2, queue_size=10)

    # LiDAR 데이터를 구독
    rospy.Subscriber('/sensor_data/lidar', PointCloud2, lidar_callback)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        lidar_data_subscriber()
    except rospy.ROSInterruptException:
        pass
