# 3D point cloud를 시각화하는 코드

import open3d as o3d
import numpy as np

# 포인트 클라우드 로드
points = np.fromfile("/home/minseokim521/cloud_innovators/src/point_cloud_data/2011_09_26_drive_0009_sync/2011_09_26/2011_09_26_drive_0009_sync/velodyne_points/data/0000000000.bin", dtype=np.float32).reshape(-1, 4)

# Open3D로 포인트 클라우드 변환
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points[:, :3])

# 포인트 클라우드 시각화
o3d.visualization.draw_geometries([pcd])
