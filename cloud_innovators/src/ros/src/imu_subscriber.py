#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import String
import numpy as np
from filterpy.kalman import KalmanFilter

# Kalman 필터 초기화 함수 (IMU용)
def initialize_kalman_filter():
    kf = KalmanFilter(dim_x=6, dim_z=3)

    # 초기 상태 (가속도 및 각속도)
    kf.x = np.array([0., 0., 0., 0., 0., 0.])  # [가속도 x, 가속도 y, 가속도 z, 각속도 x, 각속도 y, 각속도 z]

    # 상태 전이 행렬 A
    dt = 1.0  # 시간 간격 (1초)
    kf.F = np.array([[1, 0, 0, dt, 0, 0],
                     [0, 1, 0, 0, dt, 0],
                     [0, 0, 1, 0, 0, dt],
                     [0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0, 1]])

    # 관측 모델 행렬 H (IMU는 가속도 및 각속도 측정 가능)
    kf.H = np.array([[1, 0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0]])

    # 측정 노이즈 행렬 R (IMU 측정 노이즈)
    kf.R = np.array([[0.1, 0, 0],
                     [0, 0.1, 0],
                     [0, 0, 0.1]])

    # 프로세스 노이즈 행렬 Q (IMU 데이터 노이즈)
    kf.Q = np.eye(6) * 0.01

    # 공분산 행렬 P 초기값
    kf.P *= 5

    return kf

# IMU 데이터를 수신 후 칼만 필터 적용 및 퍼블리시
def imu_callback(data):
    rospy.loginfo("IMU Data Received")

    # Kalman 필터 적용
    global kf
    z = np.array([data.linear_acceleration.x, data.linear_acceleration.y, data.linear_acceleration.z])  # 가속도 데이터
    kf.predict()  # 예측 단계
    kf.update(z)  # 측정 데이터로 업데이트

    # Kalman 필터로 추정된 IMU 데이터 퍼블리시
    processed_data = String()
    processed_data.data = f"Kalman Filtered IMU data: acceleration({kf.x[0]}, {kf.x[1]}, {kf.x[2]})"
    imu_pub.publish(processed_data)

def imu_data_subscriber():
    rospy.init_node('imu_data_subscriber', anonymous=True)

    # Kalman 필터 초기화
    global kf
    kf = initialize_kalman_filter()

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
