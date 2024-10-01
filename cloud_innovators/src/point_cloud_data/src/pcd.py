import os
import numpy as np
import open3d as o3d
import time

class Read_pcd_data:
    def __init__(self, data_folder, frame_interval=0.1):
        """
        클래스 초기화. 데이터 폴더 경로와 프레임 간격을 설정.
        :param data_folder: .bin 파일이 들어있는 데이터 폴더 경로
        :param frame_interval: 각 프레임을 처리할 때의 시간 간격(초 단위)
        """
        self.data_folder = data_folder
        self.frame_interval = frame_interval
        self.bin_files = self.get_bin_files()

    def get_bin_files(self):
        """
        데이터 폴더 내의 모든 .bin 파일 목록을 가져와 정렬
        :return: .bin 파일 리스트
        """
        bin_files = sorted([f for f in os.listdir(self.data_folder) if f.endswith('.bin')])
        print(f"총 {len(bin_files)}개의 .bin 파일이 있습니다.")
        return bin_files

    def load_bin_file(self, bin_file_path):
        """
        .bin 파일을 로드하여 포인트 클라우드 데이터로 변환
        :param bin_file_path: .bin 파일 경로
        :return: 포인트 클라우드 데이터 (x, y, z, reflectance)
        """
        points = np.fromfile(bin_file_path, dtype=np.float32).reshape(-1, 4)
        return points

    def process_point_cloud(self, points):
        """
        포인트 클라우드 데이터를 처리하는 함수 (필터링 등 추가 가능)
        :param points: 포인트 클라우드 데이터
        :return: 처리된 포인트 클라우드 데이터
        """
        # 예시로, z축 값이 -2미터에서 2미터 사이에 있는 포인트만 남김
        filtered_points = points[(points[:, 2] > -2) & (points[:, 2] < 2)]
        return filtered_points

    def visualize_continuous(self):
        """
        연속적으로 포인트 클라우드를 시각화하는 함수. 창을 한 번만 띄우고 포인트 클라우드를 업데이트함.
        """
        vis = o3d.visualization.Visualizer()
        vis.create_window()

        # 첫 번째 포인트 클라우드를 로드하여 추가
        bin_file_path = os.path.join(self.data_folder, self.bin_files[0])
        points = self.load_bin_file(bin_file_path)
        points = self.process_point_cloud(points)
        
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points[:, :3])
        vis.add_geometry(pcd)

        for bin_file in self.bin_files[1:]:
            bin_file_path = os.path.join(self.data_folder, bin_file)
            print(f"Processing {bin_file_path}")

            # .bin 파일 로드 및 처리
            points = self.load_bin_file(bin_file_path)
            points = self.process_point_cloud(points)

            # 기존 포인트 클라우드 업데이트
            pcd.points = o3d.utility.Vector3dVector(points[:, :3])
            vis.update_geometry(pcd)
            vis.poll_events()
            vis.update_renderer()

            # 다음 프레임 처리 전에 시간 간격 대기
            time.sleep(self.frame_interval)

        vis.destroy_window()

# 메인 실행 부분
if __name__ == "__main__":
    # 데이터 폴더 경로 설정 (실제 경로로 변경 필요)
    data_folder = "/home/minseokim521/cloud_innovators/src/point_cloud_data/2011_09_26_drive_0009_sync/2011_09_26/2011_09_26_drive_0009_sync/velodyne_points/data"    
    # 클래스 인스턴스 생성 및 실행
    pcd_reader = Read_pcd_data(data_folder, frame_interval=0.1)  # 프레임 간격은 0.1초로 설정
    pcd_reader.visualize_continuous()
