import cv2
from pyzbar.pyzbar import decode
# Opening the camera
# cv2.namedWindow("preview")
# vc = cv2.VideoCapture(0)
#
# if vc.isOpened(): # try to get the first frame
#     rval, frame = vc.read()
# else:
#     rval = False
#
# while rval:
#     cv2.imshow("preview", frame)
#     rval, frame = vc.read()
#     key = cv2.waitKey(20)
#     if key == 27: # exit on ESC
#         break
#
# vc.release()
# cv2.destroyWindow("preview")

#read barcode
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    if not success:
        break
    for code in decode(img):
        code.data.decode('utf-8')
    cv2.imshow('image',img)
    cv2.waitKey(1)
cap.release()


# hello_psg.py

# import tkinter as tk
# from tkinter import ttk
#
# root = tk.Tk()
# root.title('Inventory Manager')
#
# items = [1,2,3]
# combo = ttk.Combobox(root)
# combo['values'] = items
# combo.pack()
#
# root.mainloop()