#!/usr/bin/env python

import rospy
import rosbag
from sensor_msgs.msg import NavSatFix
from gps_common.msg import GPSFix

def gpsfix_to_navsatfix(gps_msg):
    navsat_msg = NavSatFix()
    navsat_msg.header = gps_msg.header
    navsat_msg.latitude = gps_msg.latitude
    navsat_msg.longitude = gps_msg.longitude
    navsat_msg.altitude = gps_msg.altitude
    # 필요한 변환 추가
    return navsat_msg

def gps_publisher():
    rospy.init_node('gps_publisher', anonymous=True)
    
    # GPS 데이터를 퍼블리시할 Publisher 설정
    gps_pub = rospy.Publisher('/sensor_data/gps', NavSatFix, queue_size=10)
    
    # rosbag 파일 열기
    bag = rosbag.Bag('/home/minseokim521/cloud_innovators/src/ros/Team_Hector_MappingBox_RoboCup_2011_Rescue_Arena.bag')

    rate = rospy.Rate(10)  # 10Hz로 퍼블리시

    # rosbag에서 GPS 메시지 읽기
    for topic, msg, t in bag.read_messages():
        if topic == '/fix':  # GPS 데이터 토픽 (gps_common/GPSFix)
            navsat_msg = gpsfix_to_navsatfix(msg)
            gps_pub.publish(navsat_msg)
        
        rate.sleep()  # 다음 메시지 대기

    bag.close()

if __name__ == '__main__':
    try:
        gps_publisher()
    except rospy.ROSInterruptException:
        pass
