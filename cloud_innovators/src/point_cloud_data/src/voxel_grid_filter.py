import os
import numpy as np
import open3d as o3d
import time

# 포인트 클라우드 데이터 로드
def load_point_cloud(bin_file_path):
    # .bin 파일에서 포인트 클라우드 데이터를 로드 (예: KITTI 데이터)
    points = np.fromfile(bin_file_path, dtype=np.float32).reshape(-1, 4)
    
    # Open3D 포인트 클라우드 객체로 변환
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])  # x, y, z 좌표만 사용
    return pcd

# Voxel Grid Filter 적용
def apply_voxel_grid_filter(pcd, voxel_size=0.2):
    """
    Voxel Grid 필터를 적용하여 포인트 클라우드 데이터를 다운샘플링합니다.
    :param pcd: Open3D 포인트 클라우드 객체
    :param voxel_size: Voxel 크기 (단위: meter)
    :return: 다운샘플링된 포인트 클라우드 객체
    """
    print(f"원래 포인트 수: {len(pcd.points)}")
    
    # Voxel 크기를 설정하여 다운샘플링
    downsampled_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
    
    print(f"다운샘플링된 포인트 수: {len(downsampled_pcd.points)}")
    return downsampled_pcd

# 연속적인 포인트 클라우드 시각화
def visualize_continuous_point_clouds(bin_folder_path, voxel_size=0.2, frame_interval=0.1):
    """
    지속적으로 포인트 클라우드를 시각화하는 함수.
    :param bin_folder_path: .bin 파일들이 저장된 폴더 경로
    :param voxel_size: Voxel 크기 (단위: meter)
    :param frame_interval: 각 프레임을 처리할 때의 시간 간격(초 단위)
    """
    # Visualizer 창 생성
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # 데이터 폴더 내의 모든 .bin 파일 목록을 가져옴
    bin_files = sorted([f for f in os.listdir(bin_folder_path) if f.endswith('.bin')])

    # 첫 번째 파일 로드
    bin_file_path = os.path.join(bin_folder_path, bin_files[0])
    pcd = load_point_cloud(bin_file_path)
    downsampled_pcd = apply_voxel_grid_filter(pcd, voxel_size=voxel_size)

    vis.add_geometry(pcd)
    vis.add_geometry(downsampled_pcd)

    # 각 파일에 대해 연속적으로 처리
    for bin_file in bin_files:
        bin_file_path = os.path.join(bin_folder_path, bin_file)
        print(f"Processing {bin_file_path}")

        # .bin 파일 로드 및 처리
        pcd = load_point_cloud(bin_file_path)
        downsampled_pcd = apply_voxel_grid_filter(pcd, voxel_size=voxel_size)

        # 포인트 클라우드 업데이트
        vis.update_geometry(pcd)
        vis.update_geometry(downsampled_pcd)

        # 시각화 업데이트
        vis.poll_events()
        vis.update_renderer()

        # 다음 프레임 처리 전에 시간 간격 대기
        time.sleep(frame_interval)

    vis.destroy_window()

if __name__ == "__main__":
    # .bin 파일들이 저장된 폴더 경로 설정 (실제 경로로 변경 필요)
    bin_folder_path = "/home/minseokim521/cloud_innovators/src/point_cloud_data/2011_09_26_drive_0009_sync/2011_09_26/2011_09_26_drive_0009_sync/velodyne_points/data"
    
    # 연속적인 포인트 클라우드 시각화 실행
    visualize_continuous_point_clouds(bin_folder_path, voxel_size=0.2, frame_interval=0.1)  # 프레임 간격 0.1초 설정
