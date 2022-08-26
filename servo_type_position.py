from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM
import atexit

pwm = PWM(0x60)

pwm_frequency = 100  # servo 50 Hz but 100 MHz is needed for motors to work properly
pwm.setPWMFreq(pwm_frequency)

servo_mid_points_ms = 1.5
deflect_90_in_ms = 0.5

period_in_ms = 1000 / pwm_frequency
pulse_steps = 4096
steps_per_ms = pulse_steps / period_in_ms
steps_per_degree = (deflect_90_in_ms * steps_per_ms) / 90
servo_mid_points_steps = servo_mid_points_ms * steps_per_ms
