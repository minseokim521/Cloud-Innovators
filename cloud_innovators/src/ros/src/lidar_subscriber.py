#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

# LiDAR 데이터를 수신 후 퍼블리시
def lidar_callback(data):
    rospy.loginfo("LiDAR Data Received")
    # LiDAR 데이터를 가공하여 퍼블리시할 데이터를 생성
    processed_data = String()
    processed_data.data = f"LiDAR data: ranges({data.ranges[:10]})"  # Ranges 배열에서 첫 10개만 출력
    lidar_pub.publish(processed_data)  # 가공된 데이터를 퍼블리시

def lidar_data_subscriber():
    rospy.init_node('lidar_data_subscriber', anonymous=True)
    
    # LiDAR 데이터를 퍼블리시할 토픽 설정
    global lidar_pub
    lidar_pub = rospy.Publisher('/processed/lidar', String, queue_size=10)

    # LiDAR 데이터를 구독
    rospy.Subscriber('/sensor_data/lidar', LaserScan, lidar_callback)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        lidar_data_subscriber()
    except rospy.ROSInterruptException:
        pass
