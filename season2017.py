from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread
import sys
import cv2
import ForgivingFRC as forgive
from networktables import NetworkTable
__author__="Soha King <soha@lohu.info>"

_GEAR_ONE_SIDE_AREA=[15000,50000]

vdev=cv2.VideoCapture(0)
vdev.set(cv2.CAP_PROP_FRAME_WIDTH,forgive.constant._CAMERA_FRAMESIZE[0])
vdev.set(cv2.CAP_PROP_FRAME_HEIGHT,forgive.constant._CAMERA_FRAMESIZE[1])

middle=int(forgive.constant._CAMERA_FRAMESIZE[0]/2)

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					# if(frame!=None):
					# 	pass
					r,buf=cv2.imencode(".jpg",frameFinal)
					self.wfile.write("--jpgboundary".encode())
					self.send_header('Content-type','image/jpeg')
					self.end_headers()
					self.wfile.write(bytearray(buf))
				except KeyboardInterrupt:
					break
			return
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def main():
	global frameFinal
	try:
		server=ThreadedHTTPServer(("0.0.0.0",9090),CamHandler)
		target=Thread(target=server.serve_forever,args=())

		NetworkTable.setIPAddress('10.54.53.2')
		NetworkTable.setClientMode()
		NetworkTable.initialize()
		nt=NetworkTable.getTable("Forgiving/Vision")

		isNotStarted=True

		while 2333366666:
			ret,image=vdev.read()
			blur=cv2.GaussianBlur(image,(9,9),0)
			frame=image
			result,mask=forgive.function.singleColorGlass(forgive.constant._HSV_RANGE_GREEN[0],forgive.constant._HSV_RANGE_GREEN[1],blur)

			cv2.line(frame,(middle,0),(middle,forgive.constant._CAMERA_FRAMESIZE[1]),(205,194,255),2) # output

			_,contours,_=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			centersX=[]
			centersY=[]
			for i in range(len(contours)):
				cnt=contours[i]
				area=cv2.contourArea(cnt)
				if(_GEAR_ONE_SIDE_AREA[0]<area<_GEAR_ONE_SIDE_AREA[1]):
					goal=forgive.function.polygon(cnt,0.02)
					cv2.drawContours(frame,[goal],0,(255,0,0),5) # output
					moments=cv2.moments(goal);
					centerX,centerY=forgive.function.getCenter(moments)
					cv2.circle(frame,(centerX,centerY),5,(255,0,255),-1) # output
					centersX.append(centerX)
					centersY.append(centerY)

			if((len(centersX)==2)and(len(centersY)==2)):
				finalX=int((centersX[0]+centersX[1])/2)
				finalY=int((centersY[0]+centersY[1])/2)
				cv2.circle(frame,(finalX,finalY),5,(255,255,255),-1) # output

				err=finalX-middle
				align=forgive.function.alignedToWhere(err,forgive.constant._PIXEL_TOLERANCE)
				if(align==-1):
					# print('left now, turn RIGHT')
					nt.putString("turn","right")
				elif(align==1):
					# print('right now, turn LEFT')
					nt.putString("turn","left")
				else:
					# print('center now, GREAT!')
					nt.putString("turn","great")				

			frameFinal=frame
			if(isNotStarted):
				target.start()
				isNotStarted=False

			# cv2.imshow("FRC 2017 Vision",result)
			# cv2.waitKey(1)

	except KeyboardInterrupt:
		vdev.release()
		sys.exit()
	# cv2.destroyAllWindows()

if(__name__=="__main__"):
	main()