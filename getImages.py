import cv2
import pypylon.pylon as py 
import numpy as np 

def format_ip_config(cfg_str):
    result = []
    cfg = int(cfg_str)
    if cfg & 1:
        result.append("PersistentIP")
    if cfg & 2:
        result.append("DHCP")
    if cfg & 4:
        result.append("LLA")
    return ", ".join(result)

################################################################################

tl_factory = py.TlFactory.GetInstance()

for dev_info in tl_factory.EnumerateDevices():
    if dev_info.GetDeviceClass() == 'BaslerGigE':
        cam_info = dev_info
        print(
            "using %s @ %s (%s), IP config = %s" % (
                cam_info.GetModelName(),
                cam_info.GetIpAddress(),
                cam_info.GetMacAddress(),
                format_ip_config(cam_info.GetIpConfigCurrent())
                )
            )
        break
else:
    raise EnvironmentError("no GigE device found")

cam = py.InstantCamera(tl_factory.CreateFirstDevice())
cam.Open()

num = 0
cap = cv2.VideoCapture('http://192.168.108.68/1')

while cam.IsGrabbing():

    with cam.RetrieveResult(1000) as res:
            if res.GrabSucceeded():
                img = res.Array

    k = cv2.waitKey(5)

    if k == ord('q'): # wait for 'q' key exit
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('images/img' + str(num) + '.png', img)
        print("image saved!")
        num += 1

    cv2.imshow('Img',img)

# Release and destroy all windows before termination
cam.StopGrabbing()


cv2.destroyAllWindows()