# IK testing
# Jul 21 2025
# PEK

# used to figure out what was wrong with the robot in 2nd meeting with Yuqi
# resolution : jack's final.py code on github is pretty different from what I had. I can use that moving forward
from interbotix_xs_modules.arm import InterbotixManipulatorXS

import math
import numpy as   np

import sys
import time

def main():
	################### Variables ##################################
	bot = InterbotixManipulatorXS("px100", "arm", "gripper")

	xPositions = {1:102.5, 2:138.5, 3:174.5, 4:210.5} # dictionary w X coordinates
	zFinal = 100 # mm . MIGHT NEED TO CHANGE
	#yFinal = 18 # mm. FOR LAB 6
	yPositions={'a': -126,'b': -90, 'c': -54, 'd': -18, 'e': 18, 'f': 54 , 'g': 90, 'h': 126 } #for final

	##### READ in
	#if len(sys.argv) > 1:
	pick_locationX = int(sys.argv[1])
	#pick_locationX = sys.argv[1]
	pick_locationY = sys.argv[2]

	place_locationX = int(sys.argv[3])
	place_locationY = sys.argv[4]

	#else:
	 # print("Please provide pick and place location numbers between 1 and 4.")

	#translate pick and place locations into coordinates
	xFinalPick = xPositions[pick_locationX] # mm
	yFinalPick = yPositions[pick_locationY]
	pickAngles = invKinematics(xFinalPick, yFinalPick, zFinal)
	
	xFinalPlace = xPositions[place_locationX] # mm
	yFinalPlace = yPositions[place_locationY]
	placeAngles = invKinematics(xFinalPlace,yFinalPlace,zFinal)

	time.sleep(1) # 100 s

# 	#### move robot to pick up location / pick up
# 	bot.arm.set_single_joint_position("waist", pickAngles[0]) #waist
# 	bot.arm.set_single_joint_position("shoulder", pickAngles[1]) #shoulder
# 	bot.gripper.open()
# 	bot.arm.set_single_joint_position("wrist_angle", pickAngles[3])
# 	bot.arm.set_single_joint_position("elbow", pickAngles[2])
# 	bot.gripper.close()

#   # move gripper straight up

# 	#### move robot to drop off location / drop off
# 	bot.arm.set_single_joint_position("waist", placeAngles[0]) #waist
# 	bot.arm.set_single_joint_position("shoulder", placeAngles[1]) #shoulder
# 	bot.gripper.open()
# 	bot.arm.set_single_joint_position("wrist_angle", placeAngles[3])
# 	bot.arm.set_single_joint_position("elbow", placeAngles[2])
# 	bot.gripper.close()

# 	#### go to sleep
# 	bot.arm.set_single_joint_position("waist", 0)
# 	bot.arm.set_single_joint_position("shoulder", -1.88)
# 	bot.arm.set_single_joint_position("elbow", 1.5)
# 	bot.arm.set_single_joint_position("wrist_angle", 0.8)



def invKinematics(xFinal, yFinal,zFinal):
	endEffector = math.radians(90) # must be vertical
	angleOffset = math.radians(90)
	wristAngleOffset = math.radians(45)

	elbowToWrist = 100 # mm
	shoulderToElbow = 100 # mm
	shoulderOffset = 35 # mm

	shoulderHyp = math.sqrt(shoulderToElbow**2 + shoulderOffset**2)

	elbowIK = math.acos(((xFinal**2)+(zFinal**2)-(elbowToWrist**2)-(shoulderHyp**2)) / (2*shoulderHyp*elbowToWrist))

	shoulderIKprime1 = math.atan(zFinal/xFinal)-math.atan((elbowToWrist*math.sin(elbowIK))/	(shoulderHyp+elbowToWrist*(math.cos(elbowIK) ) ) ) # w hypotenuse
	alpha = math.atan(shoulderOffset/shoulderToElbow) # accounting for offset
	shoulderIK1 = shoulderIKprime1 + alpha  #accounting for offset
	
	shoulderIKprime2 = math.atan(zFinal/xFinal)-math.atan((elbowToWrist*math.sin(-elbowIK))/(shoulderHyp+elbowToWrist*(math.cos(-elbowIK) ) ) ) # w hypotenuse
	shoulderIK2 = shoulderIKprime2 + alpha  #accounting for offset

	#### pick solution where shoulder angle is greatest
	if (shoulderIK1 >= shoulderIK2) :
		shoulderIK = -(shoulderIK1- np.pi/2.0)
	elif (shoulderIK2 > shoulderIK1):
		shoulderIK = -(shoulderIK2- angleOffset)
	else:
		shoulderIK = 0.0
		print("Error in calculating shoulder angle.")

  #### translate coordinate systems
	shoulder = shoulderIK # no offset
	elbow = elbowIK - angleOffset

	wrist = endEffector - elbow - shoulder - wristAngleOffset # bc total will always be vertical

	# waist angle can be treated separately
	prelim_waist = math.atan(xFinal/yFinal)
	if (prelim_waist < 0):
		waist = prelim_waist + angleOffset 
	elif (prelim_waist > 0):
		waist = -(angleOffset - prelim_waist)
	else:
		waist = 0

	# check angle ranges
	print("Waist angle: {}".format(waist))
	print("Shoulder angle: {}".format(shoulder))
	print("Elbow angle: {}".format(elbow))
	print("Wrist angle: {}".format(wrist))


	return [waist, shoulder, elbow, wrist]

if __name__=='__main__':
    	main()