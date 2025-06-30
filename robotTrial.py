# Phoebe Esser Katz
# June 30, 2025
# IV insertion part 1
# description: robot starts in home position. moves straight up and down to insert needle into jell-o stuff
    # this code attempts to use simultaneous robot commands
# Modified from IVinsertion1.py

from interbotix_xs_modules.arm import InterbotixManipulatorXS

import math
import numpy as   np

import sys
import time

def main():
	################### Variables ##################################
    bot = InterbotixManipulatorXS("px100", "arm", "gripper")

    #xPositions = {1:102.5, 2:138.5, 3:174.5, 4:210.5} # dictionary w X coordinates
    xFinal = 100 # mm . need to measure (towards chess opponent)
    yFinal = 0 # mm. need to measure (back and forth on board)
    zFinal = 40 # mm . need to measure (up and down)

    angles = invKinematics(xFinal, yFinal, zFinal)

    time.sleep(2) # 10 s

	#### move robot to down pose
    bot.gripper.open()
    bot.arm.set_joint_positions(angles, vel=0.35, accel=4.0, mode=0) # simultaneous motion

    bot.gripper.close()

  # move gripper straight up
    anglesRaised = invKinematics(xFinal, yFinal, zFinal + 30)
    bot.arm.set_joint_positions(anglesRaised, vel=0.35, accel=4.0, mode=0) # simultaneous motion

	#### go to sleep
    sleep_joint_positions = [0,-1.88,1.5,0.8]
    bot.arm.set_joint_positions(sleep_joint_positions, vel=0.35, accel=4.0, mode=0) # simultaneous motion


if __name__=='__main__':
    main()

def invKinematics(xFinal, yFinal,zFinal):
    endEffector = math.radians(90) # must be vertical
    angleOffset = math.radians(90)

    elbowToWrist = 100 # mm
    shoulderToElbow = 100 # mm
    shoulderOffset = 35 # mm

    shoulderHyp = math.sqrt(shoulderToElbow**2 + shoulderOffset**2)

    elbowIK = math.acos(((xFinal**2)+(zFinal**2)-(elbowToWrist**2)-(shoulderHyp**2)) / (2*shoulderHyp*elbowToWrist))

    shoulderIKprime1 = math.atan(zFinal/xFinal)-math.atan((elbowToWrist*math.sin(elbowIK))/	(shoulderHyp+elbowToWrist*(math.cos(elbowIK) ) ) ) # w hypotenuse
    alpha = math.atan(shoulderOffset/shoulderToElbow) # accounting for offset
    shoulderIK1 = shoulderIKprime1 + alpha  #accounting for offset

    shoulderIKprime2 = math.atan(zFinal/xFinal)-math.atan((elbowToWrist*math.sin(-elbowIK))/	(shoulderHyp+elbowToWrist*(math.cos(-elbowIK) ) ) ) # w hypotenuse
    shoulderIK2 = shoulderIKprime2 + alpha  #accounting for offset

	#### pick solution where shoulder angle is greatest
    if shoulderIK1 >= shoulderIK2 :
        shoulderIK = -(shoulderIK1- np.pi/2.0)
    elif (shoulderIK2 > shoulderIK1):
        shoulderIK = -(shoulderIK2- angleOffset)
    else:
        shoulderIK = 0.0
        print("Error in calculating shoulder angle.")

  #### translate coordinate systems
    shoulder = -(shoulderIK - angleOffset)
    elbow = -(elbowIK + angleOffset)

    wrist = endEffector - elbow - shoulder # bc total will always be vertical

    waist = (np.pi/2) - math.atan(xFinal/yFinal) # waist angle can be treated separately

    print("Waist angle: {}".format(waist))
    print("Shoulder angle: {}".format(shoulder))
    print("Elbow angle: {}".format(elbow))
    print("Wrist angle: {}".format(wrist))


    return [waist, shoulder, elbow, wrist]