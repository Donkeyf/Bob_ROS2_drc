import numpy as np
import cv2
import pickle         
from matplotlib import pyplot as plt
from lib.visualization import plotting

class VisualOdometry():
    def __init__(self, calib_dir):
        self.detector = cv2.FastFeatureDetector.create(threshold = 25, nonmaxSuppression=True)
        self.kMinNumFeature = 1500

        with open(calib_dir + "/camera_matrix.pkl", 'rb') as f:
            self.K = pickle.load(f)

        with open(calib_dir + "/projection_matrix.pkl", 'rb') as f:
            self.P = pickle.load(f)
        

        self.lk_params = dict(winSize  = (21, 21), 
             	criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

    def process_first_frame(self, frame):
        keypoints_prev = self.detector.detect(frame)
        # keypoint detectors inherit the FeatureDetector interface
        return np.array([i.pt for i in keypoints_prev], dtype=np.float32)
    
    def process_frame(self, old_frame, new_frame, prev_keys):
        k1, k2 = self.optical_flow(old_frame, new_frame, prev_keys)
        T = self.get_state(k1, k2)

        new_keys = self.detector.detect(new_frame)
        return np.array([i.pt for i in new_keys], dtype=np.float32), T

    def optical_flow(self, prev_img, curr_img, prev_keys):
        #sparse Lucas-Kanade optical flow algorithm
        k2, status, err = cv2.calcOpticalFlowPyrLK(prev_img, curr_img, prev_keys, None, **self.lk_params)
        status = status.reshape(status.shape[0])

        #keep only features found in current and prev frames
        k1 = prev_keys[status == 1]
        k2 = k2[status == 1]
        return k1, k2
    
    def get_state(self, k1, k2):
        E, _ = cv2.findEssentialMat(k2, k1, self.K, threshold=1, method = cv2.RANSAC)
        n, R, t, mask = cv2.recoverPose(E, k1, k2)
        t = np.squeeze(t)

        T = np.eye(4, dtype=np.float64)
        T[:3, :3] = R
        T[:3, 3] = t
        return T

def main():
    data_dir = "camera_params"
    vo = VisualOdometry(data_dir)

    estimated_path = []
    start_pose =  np.ones((3, 4))
    start_translation = np.zeros((3,1))
    start_rotation = np.identity(3)
    start_pose = np.concatenate((start_rotation, start_translation), axis = 1)

    cam = cv2.VideoCapture(0)

    cam.set(3, 1280)
    cam.set(4, 720)

    old_frame = None
    new_frame = None

    curr_pose = start_pose

    prev_keys = 0

    traj = np.zeros((600,600,3), dtype=np.uint8)

    i = 0
    while(cam.isOpened()):

        if(i == 0):
            ret, new_frame = cam.read()
            prev_keys = vo.process_first_frame(new_frame)
            old_frame = new_frame
            i += 1
            continue

        ret, new_frame = cam.read()
        prev_keys, transf = vo.process_frame(old_frame, new_frame, prev_keys)
        old_frame = new_frame

        curr_pose = np.matmul(curr_pose, np.linalg.inv(transf))
        estimated_path.append((curr_pose[0, 3], curr_pose[2, 3]))
         
        if (i == 100):
            break

        i += 1

    cv2.destroyAllWindows() 
        
    plotting.visualize_paths(estimated_path, estimated_path, "Visual Odometry", file_out="blah.html")


if __name__ == "__main__":
    main()
