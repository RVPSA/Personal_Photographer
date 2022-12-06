Here is the instruction for the usage of this project

We want :
 Arduino board
 One Servo Motor

Packages :
 Arduino - "firmata" package
 Python - OpenCV, PYfirmata, mediapipe

Instruction :

1. go to the arduino ide -> Tools -> Manage libraries -> Search firmata -> Install
2. Plug the arduino ide and select the port and remember port name.
3. Arduino ide, File -> Examples -> Firmata -> StandardFirmata
4. Upload the code.
5. After the uploading process, If you want you can close the arduino window but don't unplug Arduino board.

6. Go to the python script and change the port name according to the your's (2).
7. Connect the servo motor to the board, here you can use any digital pin, I choosed digital pin 10, 
	If you use something else please modify value of the variable named as 'pin' otherwise it causes for error.
8. Run the code.
9. Then you can see a picture of you, click and drag mouse near your face. you can draw a box around your face.
	(you can draw a box around any object which you want to track)
10. After that press enter button.
11. Now you can see program tracks your surrounded object.(suppose a face)
12. If program detects a smile on your face it automatically captures a image.
13. If you raise your left hand, program begins recording while tracking you.
14. When you raise your right hand, programm stops recording.