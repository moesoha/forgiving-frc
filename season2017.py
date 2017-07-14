import cv2
import ForgivingFRC as forgive
__author__="Soha King <soha@lohu.info>"

_GEAR_ONE_SIDE_AREA=[15000,50000]

vdev=cv2.VideoCapture(0)
vdev.set(cv2.CAP_PROP_FRAME_WIDTH,forgive.constant._CAMERA_FRAMESIZE[0])
vdev.set(cv2.CAP_PROP_FRAME_HEIGHT,forgive.constant._CAMERA_FRAMESIZE[1])

middle=int(forgive.constant._CAMERA_FRAMESIZE[0]/2)

def main():
	while 2333366666:
		ret,image=vdev.read()
		blur=cv2.GaussianBlur(image,(9,9),0)
		result,mask=forgive.function.singleColorGlass(forgive.constant._HSV_RANGE_GREEN[0],forgive.constant._HSV_RANGE_GREEN[1],blur)

		cv2.line(result,(middle,0),(middle,forgive.constant._CAMERA_FRAMESIZE[1]),(205,194,255),2)

		_,contours,_=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		centersX=[]
		centersY=[]
		for i in range(len(contours)):
			cnt=contours[i]
			area=cv2.contourArea(cnt)
			if(_GEAR_ONE_SIDE_AREA[0]<area<_GEAR_ONE_SIDE_AREA[1]):
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

			err=finalX-middle
			align=forgive.function.alignedToWhere(err,forgive.constant._PIXEL_TOLERANCE)
			if(align==-1):
				print('left now, turn RIGHT')
			elif(align==1):
				print('right now, turn LEFT')
			else:
				print('center now, GREAT!')

		cv2.imshow("FRC 2017 Vision",result)
		cv2.waitKey(1)

	vdev.release()
	cv2.destroyAllWindows()

if(__name__=="__main__"):
	main()