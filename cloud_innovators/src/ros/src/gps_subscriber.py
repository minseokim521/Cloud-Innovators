#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import String

# GPS 데이터를 수신 후 퍼블리시
def gps_callback(data):
    rospy.loginfo("GPS Data Received")
    # GPS 데이터를 가공하여 퍼블리시할 데이터를 생성
    processed_data = String()
    processed_data.data = f"GPS data: latitude({data.latitude}), longitude({data.longitude}), altitude({data.altitude})"
    gps_pub.publish(processed_data)  # 가공된 데이터를 퍼블리시

def gps_data_subscriber():
    rospy.init_node('gps_data_subscriber', anonymous=True)
    
    # GPS 데이터를 퍼블리시할 토픽 설정
    global gps_pub
    gps_pub = rospy.Publisher('/processed/gps', String, queue_size=10)

    # GPS 데이터를 구독
    rospy.Subscriber('/sensor_data/gps', NavSatFix, gps_callback)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        gps_data_subscriber()
    except rospy.ROSInterruptException:
        pass
