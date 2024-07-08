def motor_speed(avg_speed, current_angle, current_integral, ref_angle, kp, ki):
    
    error = ref_angle - current_angle

    new_integral = current_integral + ki * error
    output = kp * error + new_integral

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
    
    return (left_motor, right_motor, new_integral)

# def PID(Kp, Ki, setpoint, measurement):
#     global time, integral, time_prev, e_prev

#     # Value of offset - when the error is equal zero
#     offset = 320
    
#     # PID calculations
#     e = setpoint - measurement
        
#     P = Kp*e
#     integral = integral + Ki*e*(time - time_prev)

#     # calculate manipulated variable - MV 
#     MV = offset + P + integral
    
#     # update stored data for next iteration
#     e_prev = e
#     time_prev = time
#     return MV