from threading import Thread
import cv2
import ForgivingFRC as forgiving

""" from https://stackoverflow.com/questions/42017354/python-mjpeg-server """

class WebcamVideoStream:
	def __init__(self,src=0):
		self.stream=cv2.VideoCapture(src)
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH,forgiving.constant._CAMERA_FRAMESIZE[0])
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,forgiving.constant._CAMERA_FRAMESIZE[1])
		self.grabbed,self.frame=self.stream.read()
		self.stopped=False

	def start(self):
		Thread(target=self.update,args=()).start()
		return self

	def update(self):
		while True:
			if(self.stopped):
				self.stream.release()
				return
			self.grabbed,self.frame=self.stream.read()

	def read(self):
		return self.frame

	def stop(self):
		self.stopped=True
