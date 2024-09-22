#!/usr/bin/env python

import rospy
import rosbag
from sensor_msgs.msg import LaserScan

def lidar_publisher():
    rospy.init_node('lidar_publisher', anonymous=True)
    
    # LiDAR 데이터를 퍼블리시할 Publisher 설정
    lidar_pub = rospy.Publisher('/sensor_data/lidar', LaserScan, queue_size=10)
    
    # rosbag 파일 열기
    bag = rosbag.Bag('/home/minseokim521/cloud_innovators/src/ros/Team_Hector_MappingBox_RoboCup_2011_Rescue_Arena.bag')

    rate = rospy.Rate(10)  # 10Hz로 퍼블리시

    # rosbag에서 LiDAR 메시지 읽기
    for topic, msg, t in bag.read_messages():
        if topic == '/scan':  # LiDAR 데이터 토픽
            lidar_pub.publish(msg)
        
        rate.sleep()  # 다음 메시지 대기

    bag.close()

if __name__ == '__main__':
    try:
        lidar_publisher()
    except rospy.ROSInterruptException:
        pass
