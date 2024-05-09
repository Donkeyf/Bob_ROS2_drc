import numpy as np
import cv2
import pickle   

class VisualOdometry():
    def __init__(self, calib_dir) -> None:
        self.detector = cv2.FastFeatureDetector.create(threshold = 25, nonmaxSuppression=True)
        self.kMinNumFeature = 1500

        self.lk_params = dict(winSize  = (21, 21), criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

        with open(calib_dir + "/camera_matrix.pkl", 'rb') as f:
            self.K = pickle.load(f)

        with open(calib_dir + "/projection_matrix.pkl", 'rb') as f:
            self.P = pickle.load(f)

        with open(calib_dir + "/distortion_coefficients.pkl", 'rb') as f:
            self.D = pickle.load(f)

    def optical_flow(self, prev_img, curr_img, prev_keys):
        #sparse Lucas-Kanade optical flow algorithm
        k2, status, err = cv2.calcOpticalFlowPyrLK(prev_img, curr_img, prev_keys, None, **self.lk_params)
        status = status.reshape(status.shape[0])

        #keep only features found in current and prev frames
        return prev_keys[status == 1], k2[status == 1]

    def get_pose(self, k1, k2):
        E, _ = cv2.findEssentialMat(k1, k2, self.K, threshold=1, method=cv2.RANSAC)
        n ,R, t, mask = cv2.recoverPose(E, k1, k2)
        t = np.squeeze(t)

        T = np.eye(4, dtype=np.float64)
        T[:3, :3] = R
        T[:3, 3] = t

        T_m = np.zeros((3,4), dtype=np.float64)
        T_m[:3, :3] = R
        T_m[:3, 3] = t

        mtx = np.matmul(self.K, T_m)

        return T, mtx


    def triangulate(self, mtx1, mtx2, prev_pts, cur_pts):
        points_3D = cv2.triangulatePoints(mtx1, mtx2, prev_pts[:2], cur_pts[:2])
        return points_3D
    
    def pnp(self, points_3D, cur_pts):
        retval, rvec, tvec = cv2.solvePnP(cur_pts, points_3D, self.K, self.D)
        t_vec = np.squeeze(t_vec)

        T = np.eye(4, dtype=np.float64)
        T[:3, :3] = rvec
        T[:3, 3] = tvec

        return T
    
    def process_first_frame(self, frame):
        keypoints_prev = self.detector.detect(frame)
        # keypoint detectors inherit the FeatureDetector interface
        return np.array([i.pt for i in keypoints_prev], dtype=np.float32)
    
    def process_frame(self, old_frame, new_frame, prev_keys):
        k1, k2 = self.optical_flow(old_frame, new_frame, prev_keys)
        T, mtx = self.get_pose(k1, k2)

        new_keys = self.detector.detect(new_frame)
        return np.array([i.pt for i in new_keys], dtype=np.float32), T, mtx