import os
import numpy as np
from filterpy.kalman import KalmanFilter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# OXTS 파일에서 GPS와 IMU 데이터를 로드하는 함수
def load_oxts_data(oxts_folder_path):
    gps_data = []
    imu_data = []

    # .txt 파일 목록을 불러옴
    oxts_files = sorted([f for f in os.listdir(oxts_folder_path) if f.endswith('.txt')])

    for oxts_file in oxts_files:
        file_path = os.path.join(oxts_folder_path, oxts_file)

        # 파일에서 데이터를 읽어옴
        with open(file_path, 'r') as f:
            line = f.readline().strip().split()
            line = [float(x) for x in line]

            # GPS 데이터 (위도, 경도) 추출
            latitude = line[0]  # 위도
            longitude = line[1]  # 경도
            gps_data.append([latitude, longitude])

            # IMU 데이터 (가속도, 각속도) 추출
            acceleration_x = line[11]  # x축 가속도
            acceleration_y = line[12]  # y축 가속도
            angular_velocity_z = line[18]  # z축 각속도
            imu_data.append([acceleration_x, acceleration_y, angular_velocity_z])

    return np.array(gps_data), np.array(imu_data)

# Kalman 필터 초기화 함수
def initialize_kalman_filter():
    kf = KalmanFilter(dim_x=4, dim_z=2)

    # 초기 상태 (위치, 속도)
    kf.x = np.array([gps_data[0][0], gps_data[0][1], 0., 0.])  # [위도, 경도, 위도 속도, 경도 속도]

    # 상태 전이 행렬 A
    dt = 1.0  # 시간 간격 (1초, 실제 데이터 주기에 맞춰 조정 가능)
    kf.F = np.array([[1, 0, dt, 0],
                     [0, 1, 0, dt],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

    # 관측 모델 행렬 H (GPS는 위치만 측정 가능)
    kf.H = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0]])

    # 측정 노이즈 행렬 R (GPS 노이즈)
    kf.R = np.array([[0.05, 0],   # GPS 측정 오차 (위치 오차) 
                     [0, 0.5]])   # R 값을 줄여서 GPS 데이터를 더 신뢰하게 만듦

    # 프로세스 노이즈 행렬 Q (IMU의 가속도 노이즈)
    kf.Q = np.eye(4) * 0.01 # IMU 데이터를 더 신뢰하기 위해 Q 값 줄임

    # 공분산 행렬 P 초기값
    kf.P *= 5   # P 값을 줄여 초기 상태에 대한 신뢰도를 높임

    return kf

# 칼만 필터로 GPS와 IMU 데이터를 처리하는 함수
def apply_kalman_filter(gps_data, imu_data):
    kf = initialize_kalman_filter()

    # 결과를 저장할 리스트
    estimated_positions = []

    for i in range(len(gps_data)):
        # IMU 데이터로 예측 단계 수행 (IMU는 속도를 제공함)
        if i > 0:
            velocity = imu_data[i]  # IMU로부터 속도 및 각속도 가져오기
            kf.predict()

        # GPS 데이터로 측정 갱신
        z = gps_data[i]  # GPS로부터 위치 데이터 (위도, 경도) 가져오기
        kf.update(z)

        # 추정된 위치 저장
        estimated_positions.append(kf.x[:2])

    return estimated_positions

# RMSE 계산 함수
def calculate_rmse(gps_data, estimated_positions):
    rmse = np.sqrt(mean_squared_error(gps_data, estimated_positions))
    return rmse

# 데이터 경로 설정
oxts_folder_path = "/home/minseokim521/cloud_innovators/src/point_cloud_data/2011_09_26_drive_0009_sync/2011_09_26/2011_09_26_drive_0009_sync/oxts/data"

# OXTS 데이터 로드
gps_data, imu_data = load_oxts_data(oxts_folder_path)

# 칼만 필터 적용
estimated_positions = apply_kalman_filter(gps_data, imu_data)

# RMSE 계산
rmse_value = calculate_rmse(gps_data, estimated_positions)
print(f"Root Mean Square Error (RMSE): {rmse_value}")

# 결과 시각화
gps_positions = np.array(gps_data)
estimated_positions = np.array(estimated_positions)

plt.figure(figsize=(10, 8))  # 그래프 크기 조절

# GPS 데이터 (빨간색 점으로 표시, 점 크기 조정)
plt.scatter(gps_positions[:, 0], gps_positions[:, 1], c='red', label="GPS Data", s=50)

# 칼만 필터 추정 데이터 (파란색 선으로 표시)
plt.plot(estimated_positions[:, 0], estimated_positions[:, 1], 'bo-', label="Kalman Filter Estimate")

# 축 범위 조정 (위도: 49.0 부근, 경도: 8.42~8.44 부근)
plt.xlim([49.0, 49.02])  # 위도 범위
plt.ylim([8.436, 8.442])  # 경도 범위

plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Kalman Filter: GPS and IMU Data')
plt.legend()
plt.grid(True)  # 그리드 추가
plt.show()
