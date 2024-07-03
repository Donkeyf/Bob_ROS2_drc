#include <opencv2/opencv.hpp>
#include <raspicam_cv.h>
#include <string>
#include <iostream>

using namespace std;
using namespace cv;
using namespace raspicam;

void cam_setup(int argc, char **arg, RaspiCam_Cv &cam){
    cam.set( CAP_PROP_FRAME_WIDTH,("-w", argc, argv, 400));
	cam.set( CAP_PROP_FRAME_HEIGHT, ("-h", argc, argv, 240));
	cam.set( CAP_PROP_BRIGHTNESS, ("-br", argc, argv, 50));
	cam.set( CAP_PROP_CONTRAST, ("-co", argc, argv, 50));
	cam.set( CAP_PROP_SATURATION, ("-sa", argv, argc, 50));
	cam.set( CAP_PROP_GAIN, ("-g", argc, argv, 50));
	cam.set( CAP_PROP_FPS, ("-fps", argc, argv,0));


}

Mat roi(Mat &frame, Point2f &source, Point2f &destination){
    line(frame, source[0], source[1], Scalar(0, 0, 255), 1);
    line(frame, source[1], source[3], Scalar(0, 0, 255), 1);
    line(frame, source[3], source[2], Scalar(0, 0, 255), 1);
    line(frame, source[2], source[0], Scalar(0, 0, 255), 1);

    Mat matrix = getPerspectiveTransform(source, destination);  
    Mat perspective;

    warpPerspective(frame, perspective, matrix, Size(320, 240));

    return perspective;
}

void threshold(Mat &perspective, Mat &threshold, Mat &grey, Mat &edge, Mat &final, Mat &final_dup0, Mat &sfinal_dup1){
    cvtColor(perspective, grey, COLOR_RGB2GRAY);
    inRange(grey, 180, 255, threshold);
    inRange(grey, 160, 255, grey);
    Canny(grey, edge, 150, 400, 3, false);
    add(threshold, edge, final);
	cvtColor(final, final, COLOR_GRAY2RGB);
	cvtColor(final, final_dup0, COLOR_RGB2GRAY); // for histogram only 
	cvtColor(final, final_dup1, COLOR_RGB2GRAY); // for histogram only

}

void histogram(Mat &frame, Mat &final_dup0, Mat &final_dup1, vector<int> &hist_lane, vector<int> &hist_end){

    hist_lane.resize(400);
    hist_lane.clear();

    for(size_t i{0}; i < frame.size().width; ++i){
		
		Mat rn_lane = final_dup0(Rect(i,140,1,100));
		divide(255, rn_lane, rn_lane);
		hist_lane.push_back((int)(sum(rn_lane)[0]));
		}

    hist_lane.resize(400);
	hist_lane.clear();

	for(size_t i{0}; i < frame.size().width; ++i){
		
		Mat rn_end = final_dup1(Rect(i,0,1,240));
		divide(255, rn_end, rn_end);
		hist_end.push_back((int)(sum(rn_end)[0]));
		
		}
    
}

int[] line_detection(vector<int> &hist_lane, vector<int> &hist_end, Mat &final){
    vector<int>:: iterator left_ptr;
    left_ptr = max_element(hist_lane.begin(), hist_lane.begin() + 200);
    int left_lane = distance(hist_lane.begin(), left_ptr);

    vector<int>:: iterator right_ptr;
    right_ptr = max_element(hist_lane.begin() + 240, hist_lane.end());
    int right_lane = distance(hist_lane.begin(), right_ptr);


    line(final, Point2f(left_lane, 0), Point2f(left_lane, 240), Scalar(0,255,0),3);
    line(final, Point2f(right_lane, 0), Point2f(right_lane, 240), Scalar(0,255,0),3);

    return [left_lane, right_lane];
}

void center(int[] lanes){
    int line_center = (lanes[1] - lanes[0])/2 + lanes[0];
    int frame_center = 216;

    diff = line_center - frame_center;
    cout << "Diff: " << diff << endl;

}

int main(int argc, char **argv){
    // Raspicam_Cv cam;
    // cam_setup(argc, argv, cam);

    Mat frame, threshold, grey, edge, final, final_dup0, final_dup1;

    // cam.grab();
    // cam.retrieve(frame);
    // cvtColor(frame, frame, COLOR_BGR2RGB);

    VideoCapture cap(0);

    while(cap.isOpened()){
        cap >> frame;

        waitKey(1);

        Point2f source[] ={Point2f(80,160), Point2f(300,160), Point2f(40,210), Point2f(340,210)};
        Point2f destination[] ={Point2f(130,0), Point2f(310,0), Point2f(130,240), Point2f(310,240)};


        Mat perspective = roi(frame, source, destination);

        threshold(frame, perspective, grey, edge, final, final_dup0, final_dup1);
        histogram(final, final_dup0, final_dup1, hist_lane, hist_end);

        vector<int> hist_lane;
        vector<int> hist_end;

        int lanes[] = line_detection(hist_lane, hist_end, final);
        center(lanes);

    }

    
}