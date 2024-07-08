import time

INTEGRAL_MIN = 100
INTEGRAL_MAX = 0

def motor_speed(avg_speed, current_angle, ref_angle, current_integral, kp, ki):
    
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

def pid_motor_speed(avg_speed, current_angle, ref_angle, previous_time, previous_error, current_integral, kp, ki, kd):
    
    error = ref_angle - current_angle
    current_time = time.time()
    delta_time = current_time - previous_time
    delta_error = error - previous_error

    # ---------------------
    # PROPORTIONAL CONTROLLER
    # ---------------------
    proportional_output = kp * error

    # ---------------------
    # INTEGRAL CONTROLLER
    # ---------------------
    current_integral += error * delta_time
    current_integral = max(min(INTEGRAL_MAX, current_integral), INTEGRAL_MIN)

    integral_output = ki * current_integral

    # ---------------------
    # DERIVATIVE CONTROLLER
    # ---------------------
    current_derivative = delta_error/delta_time

    derivative_output = current_derivative * kd

    # ---------------------
    output = proportional_output + integral_output + derivative_output

    print(f"Proportional Output is: {proportional_output}\n\
          Rolling Integral is: {current_integral}\n\
          Integral Output is: {integral_output}")

    left_motor_speed = int(avg_speed - output)
    right_motor_speed = int(avg_speed + output)

    left_motor_speed = max(min(100, left_motor_speed), 0)
    right_motor_speed = max(min(100, right_motor_speed), 0)
    
    previous_time = current_time
    previous_error = error

    return (left_motor_speed, right_motor_speed, previous_time, previous_error, current_integral)