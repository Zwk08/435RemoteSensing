import numpy as np
import cv2
#import imutils
import time
import os
import smtplib
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def mask_image(img):
    mask = np.zeros((img.shape[0],img.shape[1]),dtype = "uint8")
    #for i in range(0,4):
        #bbox = cv2.selectROI(img,False)
        #print(bbox)
        #hit spacebar after creating box
        #after using the fucntion above to get points of our masked area we do the following 
    pts = np.array([[450, 719], [450, 180], [1279, 180], [1279, 719]], dtype=np.int32)
    cv2.fillConvexPoly(mask,pts,255)
    #can have 2 fillConvexPolys if we want to add extra areas 

    masked = cv2.bitwise_and(img, img, mask=mask)
    gray = cv2.resize(masked, (200, int(masked.shape[0] * 200 / masked.shape[1]))) #helps processing
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11,11),0)

    return masked, gray

#counter variable for analyis
counter =0
while True:
    counter = counter +1
    print("")
    print("----Times through loop since starting:",counter,"----")
    print("")
    #take a first and second image to compare
    #os.system("rpicam-still --nopreview -o test0.jpg --width 1280 --height 720 --vflip --hflip --timeout 100")
    os.system("rpicam-still -o test0.jpg --width 1280 --height 720 --vflip --hflip --rotation 270")
    # wait between images so motion can be detected
    time.sleep(.5)

    # take second image
    #os.system("rpicam-still --nopreview -o test1.jpg --width 1280 --height 720 --vflip --hflip --timeout 100")
    os.system("rpicam-still -o test1.jpg --width 1280 --height 720 --vflip --hflip --rotation 270")

    print ("Captured 1st & 2nd image for analysis...")

    #mask images
    test1 = cv2.imread("test0.jpg")
    test2 = cv2.imread("test1.jpg")
    masked1, gray1 = mask_image(test1)
    masked2, gray2 = mask_image(test2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Quitting...")
        break

    #compare the two images 
    pixel_thres= 50 #how much pixel has to actually change
    detector_total = np.uint64(0)
    detector = np.zeros((gray2.shape[0],gray2.shape[1]),dtype="uint8")
    #pixel by pixel comparison
    for i in range (0, gray2.shape[0]):
        for j in range (0,gray2.shape[1]):
            if abs(int(gray2[i,j])-int(gray1[i,j])) >pixel_thres:
                detector[i,j] = 255
    #sum the detector array
    detector_total = np.uint64(np.sum(detector))
    print("detector total=", detector_total)
    print("")


    #time.sleep(1)
    if detector_total >15000:
        print("SmartDoorbell has detected someone/something at the door")
        #define a unique name for the new video file
        timestr = time.strftime("doorbell-%Y%m%d-%H%M%S")
        
        save_path = f"/home/pi/{timestr}"
        os.makedirs(save_path, exist_ok=True)
        video_file = f"{save_path}/{timestr}.mp4"
        command2 = (
        f"rpicam-vid --nopreview -t 15000 "
        f"--width 1280 --height 720 "
        f"--vflip --hflip "
        f"--framerate 15 "
        f"--codec libav "
        f"-o {video_file}"
    )
        os.system(command2)

        """
        print("Finished recording... converting to mp4...")

        command3 = 'MP4Box -fps 30 -add' + timestr +'.h264 ' + timestr + '.mp4'
        os.system(command3)
        print("Finished converting file... available for viewing")
        """

        #write masked images to file
        cv2.imwrite("gray1.jpg",gray1)
        cv2.imwrite("gray2.jpg",gray2)
        cv2.imwrite("masked1.jpg",masked1)
        cv2.imwrite("masked2.jpg",masked2)

        #upload video file to the cloud


        #send email to users with images 
        smtpUser = 'Zacharykessler40@gmail.com'
        smtpPass = 'eesmxvgblkbddwro'
        toAdd = 'zwk0804@outlook.com'
        fromAdd = smtpUser

        f_time = datetime.now().strftime('%a %d %b @ %H:%M')
        subject = 'Smart Doorbell recording drom: ' +f_time
        msg= MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = fromAdd
        msg['To'] = toAdd
        msg.preamble = "image recorded at " + f_time

        body = MIMEText('Smart Doorbell video: ' + f_time)
        msg.attach(body)

        fp = open('test0.jpg', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp = open('test1.jpg', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp = open('gray1.jpg', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp = open('gray2.jpg', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp = open('masked1.jpg', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp = open('masked2.jpg', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        s =smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtpUser,smtpPass)
        s.sendmail(fromAdd, toAdd, msg.as_string())
        s.quit()

        print("Email Delivere!!")
        time.sleep(20)


    else:
        print("Nothing detected...yet!")



