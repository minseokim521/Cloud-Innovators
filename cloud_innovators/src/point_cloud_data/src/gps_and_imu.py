import os
import time

class Read_gps_imu_data:
    def __init__(self, data_folder, frame_interval=0.1):
        """
        클래스 초기화. 데이터 폴더 경로와 프레임 간격을 설정.
        :param data_folder: .txt 파일이 들어있는 oxts 데이터 폴더 경로
        :param frame_interval: 각 프레임을 처리할 때의 시간 간격(초 단위)
        """
        self.data_folder = data_folder
        self.frame_interval = frame_interval
        self.txt_files = self.get_txt_files()

    def get_txt_files(self):
        """
        데이터 폴더 내의 모든 .txt 파일 목록을 가져와 정렬
        :return: .txt 파일 리스트
        """
        txt_files = sorted([f for f in os.listdir(self.data_folder) if f.endswith('.txt')])
        print(f"총 {len(txt_files)}개의 .txt 파일이 있습니다.")
        return txt_files

    def load_oxts_data(self, oxts_file_path):
        """
        OXTS 파일에서 GPS 및 IMU 데이터를 읽어옴.
        :param oxts_file_path: .txt 파일 경로
        :return: GPS 및 IMU 데이터
        """
        with open(oxts_file_path, 'r') as file:
            data = file.readline().strip().split(' ')
            data = [float(i) for i in data]
            return {
                "latitude": data[0],
                "longitude": data[1],
                "altitude": data[2],
                "roll": data[3],
                "pitch": data[4],
                "yaw": data[5],
                "acceleration": data[11:14],  # IMU 가속도 X, Y, Z
                "angular_velocity": data[18:21]  # IMU 각속도 X, Y, Z
            }

    def run(self):
        """
        메인 함수. .txt 파일들을 연속적으로 읽고 처리하며, 일정한 간격으로 데이터를 출력.
        """
        for txt_file in self.txt_files:
            txt_file_path = os.path.join(self.data_folder, txt_file)
            print(f"Processing {txt_file_path}")
            
            # OXTS 파일 로드
            gps_imu_data = self.load_oxts_data(txt_file_path)
            
            # GPS 및 IMU 데이터를 출력 (여기에서 실제 처리 로직을 추가할 수 있음)
            print(f"GPS: Latitude: {gps_imu_data['latitude']}, Longitude: {gps_imu_data['longitude']}, Altitude: {gps_imu_data['altitude']}")
            print(f"IMU: Acceleration: {gps_imu_data['acceleration']}, Angular Velocity: {gps_imu_data['angular_velocity']}")
            
            # 다음 프레임 처리 전에 시간 간격 대기
            time.sleep(self.frame_interval)

# 메인 실행 부분
if __name__ == "__main__":
    # 데이터 폴더 경로 설정 (실제 경로로 변경 필요)
    data_folder = "/home/minseokim521/cloud_innovators/src/point_cloud_data/2011_09_26_drive_0009_sync/2011_09_26/2011_09_26_drive_0009_sync/oxts/data"
    
    # 클래스 인스턴스 생성 및 실행
    gps_imu_reader = Read_gps_imu_data(data_folder, frame_interval=0.1)  # 프레임 간격은 0.1초로 설정
    gps_imu_reader.run()
