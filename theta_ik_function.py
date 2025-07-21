# Phoebe Esser Katz and Jack Berkowitz
# April 21, 2025
# Robotics Final: Chess part 2
# using inverse kinematics

# the IK function has 4 inputs here, the new one being final angle of the wrist (theta)

from interbotix_xs_modules.arm import InterbotixManipulatorXS

import math
import numpy as   np

import sys
import time

def main():
	################### Variables ##################################
	bot = InterbotixManipulatorXS("px100", "arm", "gripper")
	xPositions = {1:102.5, 2:138.5, 3:174.5, 4:210.5} # dictionary w X coordinates
	zFinal = 40 # mm . 
	yPositions = {'a': 126,'b': 90, 'c': 54, 'd': 18, 'e': 18, 'f': 54 , 'g': 90, 'h':126}
	theta = 135 # degrees
	
	##### READ in
	#if len(sys.argv) > 1:
	pick_locationX = int(sys.argv[1])
	pick_locationY = sys.argv[2]
	
	place_locationX = int(sys.argv[3])
	place_locationY = sys.argv[4]

	#else:
	 # print("Please provide pick and place location numbers between 1 and 4.")

	#translate pick and place locations into coordinates
	xFinalPick = xPositions[pick_locationX] # mm
	yFinalPick = yPositions[pick_locationY]
	pickAngles = invKinematics(xFinalPick, yFinalPick, zFinal,theta)
	
	xFinalPlace = xPositions[place_locationX] # mm
	yFinalPlace = yPositions[place_locationY]
	placeAngles = invKinematics(xFinalPlace,yFinalPlace,zFinal,theta)

	if (pick_locationY == 'e') or (pick_locationY == 'f') or (pick_locationY == 'g') or (pick_locationY == 'h'):
		waistPick = -1*pickAngles[0]
	else:
		waistPick = pickAngles[0]
		
	if (place_locationY == 'e') or (place_locationY == 'f') or (place_locationY == 'g') or (place_locationY == 'h'):
		waistPlace = -1*placeAngles[0]
	else:
		waistPlace = placeAngles[0]
	
	print("Real Pick Waist angle: {}".format(waistPick))
	print("Real Place Waist angle: {}".format(waistPlace))
	
	time.sleep(2) # pause for 5 s	
	
	#Move Robot to Home
	bot.arm.go_to_home_pose()

	#Move Robot to pick up location / pick up
	bot.gripper.open()
	if pick_locationX == 3 or pick_locationX == 4:
		bot.arm.set_single_joint_position("waist", waistPick)
		bot.arm.set_single_joint_position("wrist_angle", pickAngles[3])
		bot.arm.set_single_joint_position("elbow", pickAngles[2])
		bot.arm.set_single_joint_position("shoulder", pickAngles[1])
		bot.gripper.close()
	else:
		bot.arm.set_single_joint_position("waist", waistPick)
		bot.arm.set_single_joint_position("shoulder", pickAngles[1])
		bot.arm.set_single_joint_position("wrist_angle", pickAngles[3])
		bot.arm.set_single_joint_position("elbow", pickAngles[2])
		bot.gripper.close()
		
	if pick_locationX == 3 or pick_locationX == 4:
  		bot.arm.set_single_joint_position("shoulder", 0.45)
	else:
  		bot.arm.set_single_joint_position("shoulder", -0.15)	
		
	#Move Robot to Home
	bot.arm.go_to_home_pose()
	
	#Move Robot to drop off location / drop off 
	if place_locationX == 3 or place_locationX == 4:
		bot.arm.set_single_joint_position("waist", waistPlace)
		bot.arm.set_single_joint_position("wrist_angle", placeAngles[3])
		bot.arm.set_single_joint_position("elbow", placeAngles[2])
		bot.arm.set_single_joint_position("shoulder", placeAngles[1])
		bot.gripper.open()
	else:
		bot.arm.set_single_joint_position("waist", waistPlace)
		bot.arm.set_single_joint_position("shoulder", placeAngles[1])
		bot.arm.set_single_joint_position("wrist_angle", placeAngles[3])
		bot.arm.set_single_joint_position("elbow", placeAngles[2])
		bot.gripper.open()
  	
	if place_locationX == 3 or place_locationX == 4:
  		bot.arm.set_single_joint_position("shoulder", 0.45)
	else:
  		bot.arm.set_single_joint_position("shoulder", -0.15)	
		
	#Move Robot to Home
	bot.arm.go_to_home_pose() 	

	#### go to sleep
	bot.arm.go_to_sleep_pose()
	
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
