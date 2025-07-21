# Phoebe Esser Katz
# June 30, 2025
# IV insertion part 1
# description: robot starts in home position. moves straight up and down to insert needle into jell-o stuff
    # this code attempts to use simultaneous robot commands
	# uses 4 parameter IK function

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
    yFinal = 1 # mm. need to measure (back and forth on board)
    zFinal = 40 # mm . need to measure (up and down)
    theta = 60 # degrees

    angles = invKinematics(xFinal, yFinal, zFinal,theta)
    sleep_joint_positions = [0,-1.88,1.5,0.8]

    time.sleep(2) # 10 s

	#### move robot to down pose
    bot.arm.set_joint_positions(sleep_joint_positions,0.005,0.05,0) # simultaneous motion
	
    bot.gripper.open()
    bot.arm.set_joint_positions(angles,0.05,4.0,0) # simultaneous motion

    bot.gripper.close()

  # move gripper straight up
    anglesRaised = invKinematics(xFinal, yFinal, zFinal + 30, theta)
    bot.arm.set_joint_positions(anglesRaised,0.1,4.0,0) # simultaneous motion

    time.sleep(2)
	#### go to sleep

    bot.arm.set_joint_positions(sleep_joint_positions,0.05,0.5,0) # simultaneous motion

def invKinematics(xFinal, yFinal,zFinal, theta):
	endEffector = math.radians(theta) # must be vertical
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
	if (shoulderIK1 >= shoulderIK2):
  		shoulderIK = -(shoulderIK1- np.pi/2.0)
	elif(shoulderIK2 > shoulderIK1):
  		shoulderIK = -(shoulderIK2 - angleOffset)
	else:
		shoulderIK = 0.0
		print("Error in calculating shoulder angle.")
    		
    	#### print angles
    	#print("Waist angle: {}".format(waist))
	print("Shoulder angle: {}".format(shoulderIK))
	print("Elbow angle: {}".format(elbowIK))
	#print("Wrist angle: {}".format(wrist))
	print("-----")

	#### translate coordinate systems
	#shoulder = -(shoulderIK - angleOffset)
	shoulder = shoulderIK # no offset
	elbow = elbowIK - angleOffset #- math.radians(10)
	
	wrist = endEffector - elbow - shoulder # bc total will always be vertical
	
	waist = angleOffset - math.atan(xFinal/yFinal) # waist angle can be treated separately
	
	print("Waist angle: {}".format(waist))
	print("Shoulder angle: {}".format(shoulder))
	print("Elbow angle: {}".format(elbow))
	print("Wrist angle: {}".format(wrist))
	print("-----")
	
	return [waist, shoulder, elbow, wrist]
    
if __name__=='__main__':
    main()

