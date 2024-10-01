# 3D 포인트 클라우드 데이터를 읽어들이는 코드
import numpy as np

def load_velodyne_points(file_path):
    points = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    # 각 포인트는 [x, y, z, reflectance] 형식으로 이루어져 있습니다.
    return points

# 예시
file_path = '/home/minseokim521/cloud_innovators/src/point_cloud_data/2011_09_26_drive_0009_sync/2011_09_26/2011_09_26_drive_0009_sync/velodyne_points/data/0000000000.bin'
points = load_velodyne_points(file_path)
print(points.shape)  # (N, 4), N은 포인트 수

# 프린트 결과 : (122320, 4)
# 각각 포인트클라우드의 수, 4개의 값(x, y, z, 반사강도)