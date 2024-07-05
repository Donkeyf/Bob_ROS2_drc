def motor_speed(avg_speed, current_angle, ref_angle, kp):

    # if current_angle < 1.57:
        
    #     ref_angle = 0

    # elif current_angle > 1.57:

    #     ref_angle = 3.14
    
    error = ref_angle - current_angle
    output = kp * error

    left_motor = int(avg_speed - output)
    right_motor = int(avg_speed + output)

    if left_motor > 100:
        left_motor = 100
    elif left_motor < 0:
        left_motor = 0

    if right_motor > 100:
        right_motor = 100
    elif right_motor < 0:
        right_motor = 0
    
    return (left_motor, right_motor)

# if __name__ == '__main__':

#     import cv2 as cv
#     capture = cv.VideoCapture(0)
#     capture.set(3, 128)
#     capture.set(4, 96)
    
#     while True:

#         retval, frame = capture.read() 

#         if not retval:
#             break
        
#         motor_speed(50, )

#         cv.imshow('frame', frame_blur)
#         key = cv.waitKey(1)

#         if key == ord('f'):
#             break

#         elif key == ord('p'):
#             cv.waitKey(-1)
