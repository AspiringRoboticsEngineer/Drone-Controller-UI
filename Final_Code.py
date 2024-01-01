# Import Statements
from tkinter import *
from djitellopy import Tello
import cv2
import time
import threading
from PIL import ImageTk, Image

# Window
window = Tk()
window.geometry("1920x1080")
window.title("Tello Drone Controller")

# Background
bg = PhotoImage(file="Resources/Icons/User Interface Background.png")
label = Label(window, image=bg)
label.place(x=0, y=0)

# Tello Stream Reception
drone = Tello()
drone.connect()
drone.streamon()

# Takeoff & Land Buttons
BtnTakeoff_image = PhotoImage(file="Resources/Icons/Takeoff.png")
BtnTakeoff = Button(image=BtnTakeoff_image, bg="#0048E8", command=lambda: drone.takeoff())
BtnTakeoff.place(x=426.7, y=259.5)

BtnLand_image = PhotoImage(file="Resources/Icons/Land.png")
BtnLand = Button(image=BtnLand_image, bg="#0048E8", command=lambda: drone.land())
BtnLand.place(x=426.7, y=432.9)

# Translation Buttons
BtnForward_image = PhotoImage(file="Resources/Icons/Forward.png")
BtnForward = Button(image=BtnForward_image, bg="#0048E8", command=lambda: drone.move_forward(20))
BtnForward.place(x=121.1, y=261.6)

BtnBackward_image = PhotoImage(file="Resources/Icons/Backward.png")
BtnBackward = Button(image=BtnBackward_image, bg="#0048E8", command=lambda: drone.move_back(20))
BtnBackward.place(x=121.1, y=433)

BtnRight_image = PhotoImage(file="Resources/Icons/Right.png")
BtnRight = Button(image=BtnRight_image, bg="#0048E8", command=lambda: drone.move_right(20))
BtnRight.place(x=211.1, y=343)

BtnLeft_image = PhotoImage(file="Resources/Icons/Left.png")
BtnLeft = Button(image=BtnLeft_image, bg="#0048E8", command=lambda: drone.move_left(20))
BtnLeft.place(x=31.2, y=343)

# Rotation Buttons
BtnRotateRight_image = PhotoImage(file="Resources/Icons/Rotate_Right.png")
BtnRotateRight = Button(image=BtnRotateRight_image, bg="#0048E8", command=lambda: drone.rotate_clockwise(20))
BtnRotateRight.place(x=514.5, y=345.7)

BtnRotateLeft_image = PhotoImage(file="Resources/Icons/Rotate_Left.png")
BtnRotateLeft = Button(image=BtnRotateLeft_image, bg="#0048E8", command=lambda: drone.rotate_counter_clockwise(20))
BtnRotateLeft.place(x=338.7, y=347.5)

# Camera Button
def take_picture():
    frame = drone.get_frame_read().frame
    cv2.imwrite(f'Resources/Images/{time.time()}.jpg', frame)
    threading.Thread(target=stream_video).start()

BtnCamera_Image = PhotoImage(file="Resources/Icons/Camera.png")
BtnCamera = Button(image=BtnCamera_Image, bg="#0048E8", command=take_picture)
BtnCamera.place(x=604.6, y=51.5)

# Video Streaming
def stream_video():
    stream_label = Label(window)
    stream_label.place(x=800, y=0)
    while True:
        frame = drone.get_frame_read().frame
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (1120, 1080))
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image=image)
        stream_label.config(image=photo)
        cv2.waitKey(30)
        window.update()

# Start video streaming in a new thread
threading.Thread(target=stream_video).start()

# Start tkinter main loop
window.mainloop()
