# Needle-sensor-project
This is some codes and files of IV Cannulation Needle Sensor Project.

In order to initialize the robot, follow the following steps:
  1. Plug robot into power
  2. Plug robot into computer
  3. Launch the robot using the following code
username:~$roslaunch interbotix_xsarm_control xsarm_control.launch robot_model:=px100

  5. Now,you can control the robot directly from the command line by inputting angles directly, using code like this
rostopic pub -1 /px100/commands/joint_group interbotix_xs_msgs/JointGroupCommand "name: 'arm'                
cmd: [0,0,0,0]"
      Note: spacing in this command is a very important

  6. Or, you can control the robot using code. Start by navigating to the directory with the appropriate code. Then call the file you want to run, like this
username:~/my_python_code$ python3 test_code


Credits for Yuqi Xiong, Dr. Clark, Phoebe Esser Katz, Dr. Bajaj, Department of ME Univ. of Pittsburgh
