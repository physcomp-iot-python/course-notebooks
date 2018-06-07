# Demo of Servo Motor Driving
# Author: Craig Versek, based on example and library by Tony DiCola
#
# We have a mini RC servo motor available for rotational actuation applications 
# (e.g., driving a pendulum, opening a door)
# According to Bill Earl (ref. https://learn.adafruit.com/adafruit-motor-selection-guide/rc-servos)
# """The most common and economical type of servo motor in the hobbyist world 
#   is the RC Servo. These were originally designed for hobbyist Radio 
#   Control systems. But these days they are widely used for all sorts of 
#   small-scale projects where moderately precise positioning is required.
#   Most RC servos provide position control over an approximately 180 degree 
#   range. They do not provide speed control or continuous rotation.""""
#
#  The signal for driving a servo to a particular angle (and holding it there)
#  is fairly simple.  According to Simon Monk 
#  (ref. https://learn.adafruit.com/adafruit-arduino-lesson-14-servo-motors/servo-motors)
# """ The position of the servo motor is set by the length of a pulse. 
#     The servo expects to receive a pulse roughly every 20 milliseconds 
#     [equivalent to a PWM frequency of 50Hz]. If that pulse is high for 1 
#     millisecond, then the servo angle will be zero, if it is 1.5 milliseconds, 
#     then it will be at its centre position and if it is 2 milliseconds 
#     it will be at 180 degrees. The end points of the servo can vary and many 
#     servos only turn through about 170 degrees."""
#
import time
import board
import pulseio

# setup the server PWM driver pin
# NOTE: the CPX pinout diagram is not accurate about which pins support PWM output
#       I have tested the following to be working: 
#          alligator pads: A1,A2,A3,A6
#          red LED: D13
# Other pins may not raise errors, but their use is questionable. For example, A8
# connects to the light sensor, so its probably not a good idea to drive it with PWM!
# When in doubt use A1 to drive external devices like servo motors.
servo = pulseio.PWMOut(board.A1, frequency=50)

#  The duration of the pulse being HIGH is known as the "duty cycle" often given
#  in a percentage of the pulse repeat period.  Here we will use milliseconds as
#  the measure of the duty cycle HIGH period and convert it to a fraction of the 
#  integer 2**16 = 65535, which is used by the pulseio library.
def compute_duty_cycle(pulse_ms, frequency=50):
    period_ms = 1.0 / frequency * 1000.0
    duty_cycle = int(pulse_ms / (period_ms / 65535.0))
    return duty_cycle
    
# Loop through three standard positions
while True:
    servo.duty_cycle = compute_duty_cycle(1.0)  #1ms go to 0 deg position
    time.sleep(1.0)
    servo.duty_cycle = compute_duty_cycle(1.5)  #1.5ms go to 90 deg position
    time.sleep(1.0)
    servo.duty_cycle = compute_duty_cycle(2.0)  #2.0ms go to 180 deg position
    time.sleep(1.0)