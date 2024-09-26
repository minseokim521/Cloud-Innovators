#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import String

# IMU 데이터를 수신 후 퍼블리시
def imu_callback(data):
    rospy.loginfo("IMU Data Received")
    # IMU 데이터를 가공하여 퍼블리시할 데이터를 생성
    processed_data = String()
    processed_data.data = f"IMU data: orientation({data.orientation.x}, {data.orientation.y}, {data.orientation.z})"
    imu_pub.publish(processed_data)  # 가공된 데이터를 퍼블리시

def imu_data_subscriber():
    rospy.init_node('imu_data_subscriber', anonymous=True)
    
    # IMU 데이터를 퍼블리시할 토픽 설정
    global imu_pub
    imu_pub = rospy.Publisher('/processed/imu', String, queue_size=10)

    # IMU 데이터를 구독
    rospy.Subscriber('/sensor_data/imu', Imu, imu_callback)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        imu_data_subscriber()
    except rospy.ROSInterruptException:
        pass
