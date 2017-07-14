import cv2
import ForgivingFRC as forgive

vdev=cv2.VideoCapture(0)
vdev.set(cv2.CAP_PROP_FRAME_WIDTH,forgive.constant._CAMERA_FRAMESIZE[0])
vdev.set(cv2.CAP_PROP_FRAME_HEIGHT,forgive.constant._CAMERA_FRAMESIZE[1])

while 666:
	ret,image=vdev.read()
	cv2.imshow("CAM",image)
	cv2.waitKey(1)

vdev.release()
cv2.destroyAllWindows()
