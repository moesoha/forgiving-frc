import cv2
import math

def singleColorGlass(low,high,img):
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	mask=cv2.inRange(hsv,low,high)
	bw=cv2.bitwise_and(img,img,mask=mask)
	return bw,mask

def getCenter(moment):
	x=int(moment['m10']/moment['m00'])
	y=int(moment['m01']/moment['m00'])
	return x,y

def polygon(c,epsil):
    hull=cv2.convexHull(c)
    epsilon=epsil*cv2.arcLength(hull,True)
    goal=cv2.approxPolyDP(hull,epsilon,True)
    return goal

def alignedToWhere(error,tolerance):
	""" -1 | 0 | 1 """
	if(math.fabs(error)>tolerance):
		if(error>0):
			return -1
		else:
			return 1
	else:
		return 0;
