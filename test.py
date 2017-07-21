import cv2
import ForgivingFRC as forgive

GEAR_ONE_SIDE_AREA=[15000,50000]

vdev=cv2.VideoCapture(0)
vdev.set(cv2.CAP_PROP_FRAME_WIDTH,forgive.constant._CAMERA_FRAMESIZE[0])
vdev.set(cv2.CAP_PROP_FRAME_HEIGHT,forgive.constant._CAMERA_FRAMESIZE[1])

while 666:
	ret,image=vdev.read()
	imageRaw=image
	blur=cv2.GaussianBlur(image,(13,13),0)
	result,mask=forgive.function.singleColorGlass(forgive.constant._HSV_RANGE_GREEN[0],forgive.constant._HSV_RANGE_GREEN[1],blur)

	_,contours,_=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	centersX=[]
	centersY=[]
	for i in range(len(contours)):
		cnt=contours[i]
		area=cv2.contourArea(cnt)
		if(GEAR_ONE_SIDE_AREA[0]<area<GEAR_ONE_SIDE_AREA[1]):
			goal=forgive.function.polygon(cnt,0.02)
			cv2.drawContours(result,[goal],0,(255,0,0),5)
			moments=cv2.moments(goal);
			centerX,centerY=forgive.function.getCenter(moments)
			cv2.circle(result,(centerX,centerY),5,(255,0,255),-1)
			centersX.append(centerX)
			centersY.append(centerY)

	if((len(centersX)==2)and(len(centersY)==2)):
		finalX=int((centersX[0]+centersX[1])/2)
		finalY=int((centersY[0]+centersY[1])/2)
		cv2.circle(result,(finalX,finalY),5,(255,255,255),-1)

	cv2.imshow("FRC 2017 Vision",imageRaw)
	cv2.waitKey(1)

vdev.release()
cv2.destroyAllWindows()
