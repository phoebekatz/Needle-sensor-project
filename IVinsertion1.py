# Phoebe Esser Katz
# June 11, 2025
# IV insertion part 1
# description: robot starts in home position. moves straight up and down to insert needle into jell-o stuff

# Modified from Robotics Final: Chess part 2

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

    time.sleep(10) # 10 s

	#### move robot to pick up location / pick up
    bot.arm.set_single_joint_position("waist", angles[0]) #waist
    bot.arm.set_single_joint_position("shoulder", angles[1]) #shoulder
    bot.gripper.open()
    bot.arm.set_single_joint_position("wrist_angle", angles[3])
    bot.arm.set_single_joint_position("elbow", angles[2])
    bot.gripper.close()

  # move gripper straight up

    anglesRaised = invKinematics(xFinal, yFinal, zFinal + 30)

	#### move robot to drop off location / drop off
    bot.arm.set_single_joint_position("waist", anglesRaised[0]) #waist
    bot.arm.set_single_joint_position("shoulder", anglesRaised[1]) #shoulder
    bot.gripper.open()
    bot.arm.set_single_joint_position("wrist_angle", anglesRaised[3])
    bot.arm.set_single_joint_position("elbow", anglesRaised[2])
    bot.gripper.close()

	#### go to sleep
    bot.arm.set_single_joint_position("waist", 0)
    bot.arm.set_single_joint_position("shoulder", -1.88)
    bot.arm.set_single_joint_position("elbow", 1.5)
    bot.arm.set_single_joint_position("wrist_angle", 0.8)

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