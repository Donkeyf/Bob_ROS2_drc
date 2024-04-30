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
        print(keypoints_prev)
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
    
    @staticmethod
    def _form_transf(R, t):
        """
        Makes a transformation matrix from the given rotation matrix and translation vector

        Parameters
        ----------
        R (ndarray): The rotation matrix
        t (list): The translation vector

        Returns
        -------
        T (ndarray): The transformation matrix
        """
        T = np.eye(4, dtype=np.float64)
        T[:3, :3] = R
        T[:3, 3] = t
        return T
    
    def decomp_essential_mat(self, E, q1, q2):
        """
        Decompose the Essential matrix

        Parameters
        ----------
        E (ndarray): Essential matrix
        q1 (ndarray): The good keypoints matches position in i-1'th image
        q2 (ndarray): The good keypoints matches position in i'th image

        Returns
        -------
        right_pair (list): Contains the rotation matrix and translation vector
        """
        def sum_z_cal_relative_scale(R, t):
            # Get the transformation matrix
            T = self._form_transf(R, t)
            # Make the projection matrix
            P = np.matmul(np.concatenate((self.K, np.zeros((3, 1))), axis=1), T)

            # Triangulate the 3D points
            hom_Q1 = cv2.triangulatePoints(self.P, P, q1.T, q2.T)
            # Also seen from cam 2
            hom_Q2 = np.matmul(T, hom_Q1)

            # Un-homogenize
            uhom_Q1 = hom_Q1[:3, :] / hom_Q1[3, :]
            uhom_Q2 = hom_Q2[:3, :] / hom_Q2[3, :]

            # Find the number of points there has positive z coordinate in both cameras
            sum_of_pos_z_Q1 = sum(uhom_Q1[2, :] > 0)
            sum_of_pos_z_Q2 = sum(uhom_Q2[2, :] > 0)

            # Form point pairs and calculate the relative scale
            relative_scale = np.mean(np.linalg.norm(uhom_Q1.T[:-1] - uhom_Q1.T[1:], axis=-1)/
                                     np.linalg.norm(uhom_Q2.T[:-1] - uhom_Q2.T[1:], axis=-1))
            return sum_of_pos_z_Q1 + sum_of_pos_z_Q2, relative_scale

        # Decompose the essential matrix
        R1, R2, t = cv2.decomposeEssentialMat(E)
        t = np.squeeze(t)

        # Make a list of the different possible pairs
        pairs = [[R1, t], [R1, -t], [R2, t], [R2, -t]]

        # Check which solution there is the right one
        z_sums = []
        relative_scales = []
        for R, t in pairs:
            z_sum, scale = sum_z_cal_relative_scale(R, t)
            z_sums.append(z_sum)
            relative_scales.append(scale)

        # Select the pair there has the most points with positive z coordinate
        right_pair_idx = np.argmax(z_sums)
        right_pair = pairs[right_pair_idx]
        relative_scale = relative_scales[right_pair_idx]
        R1, t = right_pair
        t = t * relative_scale

        return [R1, t]

    def get_state(self, k1, k2):
        E, _ = cv2.findEssentialMat(k2, k1, self.K, threshold=1, method = cv2.RANSAC)
        n, R, t, mask = cv2.recoverPose(E, k1, k2)
        t = np.squeeze(t)

        # R, t = self.decomp_essential_mat(E, k1, k2)

        transformation_matrix = self._form_transf(R, np.squeeze(t))
        return transformation_matrix

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
