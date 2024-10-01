#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import String
import numpy as np
from filterpy.kalman import KalmanFilter

# Kalman 필터 초기화 함수
def initialize_kalman_filter():
    kf = KalmanFilter(dim_x=4, dim_z=2)

    # 초기 상태 (위치, 속도)
    kf.x = np.array([0., 0., 0., 0.])  # [위도, 경도, 위도 속도, 경도 속도]

    # 상태 전이 행렬 A
    dt = 1.0  # 시간 간격 (1초)
    kf.F = np.array([[1, 0, dt, 0],
                     [0, 1, 0, dt],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

    # 관측 모델 행렬 H (GPS는 위치만 측정 가능)
    kf.H = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0]])

    # 측정 노이즈 행렬 R (GPS 노이즈)
    kf.R = np.array([[0.05, 0],   # GPS 측정 오차
                     [0, 0.5]])

    # 프로세스 노이즈 행렬 Q
    kf.Q = np.eye(4) * 0.01  # IMU 데이터를 더 신뢰하기 위해 Q 값 줄임

    # 공분산 행렬 P 초기값
    kf.P *= 5

    return kf

# GPS 데이터를 수신 후 칼만 필터 적용 및 퍼블리시
def gps_callback(data):
    rospy.loginfo("GPS Data Received")

    # Kalman 필터 적용
    global kf
    z = np.array([data.latitude, data.longitude])  # GPS 위치 데이터 (위도, 경도)
    kf.predict()  # 예측 단계
    kf.update(z)  # 측정 데이터로 업데이트

    # Kalman 필터로 추정된 위치 데이터 퍼블리시
    processed_data = String()
    processed_data.data = f"Kalman Filtered GPS data: latitude({kf.x[0]}), longitude({kf.x[1]})"
    gps_pub.publish(processed_data)

def gps_data_subscriber():
    rospy.init_node('gps_data_subscriber', anonymous=True)

    # Kalman 필터 초기화
    global kf
    kf = initialize_kalman_filter()

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
