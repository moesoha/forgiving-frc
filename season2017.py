import sys,os
import cv2
import time
import imutils
import ForgivingFRC as forgive
from networktables import NetworkTable
__author__="Soha King <soha@lohu.info>"

_GEAR_ONE_SIDE_AREA=[6000,50000]

os.system("v4l2-ctl -d /dev/video0 -c brightness=0,exposure_auto=1,exposure_absolute=4");
time.sleep(0.6)

vdev=forgive.WebcamVideoStream().start()
middle=int(forgive.constant._CAMERA_FRAMESIZE[0]/2)

def main():
	try:
		NetworkTable.setIPAddress('10.54.53.2')
		NetworkTable.setClientMode()
		NetworkTable.initialize()
		nt=NetworkTable.getTable("Forgiving/Vision")

		while 2333366666:
			image=vdev.read()
			blur=cv2.GaussianBlur(image,(9,9),0)
			result,mask=forgive.function.singleColorGlass(forgive.constant._HSV_RANGE_CYAN[0],forgive.constant._HSV_RANGE_CYAN[1],blur)

			_,contours,_=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			centersX=[]
			centersY=[]
			areas=[]
			print("contourNumber: "+str(len(contours)))
			ii=0
			for i in range(len(contours)):
				cnt=contours[i]
				area=cv2.contourArea(cnt)
				if((_GEAR_ONE_SIDE_AREA[0]-2000)<area<(_GEAR_ONE_SIDE_AREA[1]+2000)):
					areas.append(area)
				if(_GEAR_ONE_SIDE_AREA[0]<area<_GEAR_ONE_SIDE_AREA[1]):
					ii+=1
					goal=forgive.function.polygon(cnt,0.02)
					moments=cv2.moments(goal);
					centerX,centerY=forgive.function.getCenter(moments)
					centersX.append(centerX)
					centersY.append(centerY)
			print(" contourSelected: "+str(ii))

			if(len(areas)==2):
				nt.putNumber("area0",areas[0])
				nt.putNumber("area1",areas[1])

			if((len(centersX)==2)and(len(centersY)==2)):
				finalX=int((centersX[0]+centersX[1])/2)
				finalY=int((centersY[0]+centersY[1])/2)

				err=finalX-middle
				align=forgive.function.alignedToWhere(err,forgive.constant._PIXEL_TOLERANCE)
				angle=forgive.constant._DEGREES_PPX*err
				if(align==-1):
					print('left now, turn RIGHT for '+str(angle)+' deg')
					nt.putString("turn","right")
				elif(align==1):
					print('right now, turn LEFT for '+str(angle)+' deg')
					nt.putString("turn","left")
				else:
					print('center now, GREAT! '+str(angle)+' deg')
					nt.putString("turn","great")

			# cv2.imshow("FRC 2017 Vision",result)
			# cv2.waitKey(1)

	except KeyboardInterrupt:
		sys.exit()
	# cv2.destroyAllWindows()

if(__name__=="__main__"):
	main()