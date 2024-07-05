#include <opencv2/opencv.hpp>
#include <raspicam_cv.h>
#include <string>
#include <iostream>
#include <thread>

using namespace std;
using namespace cv;
using namespace raspicam;

struct Frame{
    Mat frame;
    int process;
    float angle;
    bool is_obstacle;
    
}

void image_processing(Frame params){

}

int main(int argc, char** argv){
    Frame params[3];

    for(int i = 0; i < sizeof(params); i++){

        params[i].process = i;
        params[i].frame = frame.clone();
    }

    thread threads[3];
    for(int i = 0; i < sizeof(threads); i++){
        threads[i] = thread(image_processing, params);
    }

    for(int i = 0; i < sizeof(threads); i++){
        threads[i].join();
    }




    
}