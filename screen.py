import pyautogui
import time
import os
import Quartz
import objc
cnt = 0

# pid = 6845  # get/input a real pid from somewhere for the target app.
# point = Quartz.CGPoint()
# point.x = 1075 # get a target x from somewhere
# point.y = 745  # likewise, your target y from somewhere
# left_mouse_down_event = Quartz.CGEventCreateMouseEvent(objc.NULL, Quartz.kCGEventLeftMouseDown, point, Quartz.kCGMouseButtonLeft)
# left_mouse_up_event = Quartz.CGEventCreateMouseEvent(objc.NULL, Quartz.kCGEventLeftMouseUp, point, Quartz.kCGMouseButtonLeft)
#
# print ( Quartz.CGEventPostToPid(pid, left_mouse_down_event) )
# Quartz.CGEventPostToPid(pid, left_mouse_up_event)
#
# #pid = 2253 # get/input a real pid from somewhere for the target app.
# type_a_key_down_event = Quartz.CGEventCreateKeyboardEvent(objc.NULL, 0, True)
# type_a_key_up_event = Quartz.CGEventCreateKeyboardEvent(objc.NULL, 0, False)
#
# Quartz.CGEventPostToPid(pid, type_a_key_down_event)
# Quartz.CGEventPostToPid(pid, type_a_key_up_event)`

print (pyautogui.position())
#pyautogui.moveTo(100, 150)
#
# for i in range(1, 4):
#     print (1050 + i*25)
#     pyautogui.moveTo(1050 + i*25, 745)
#     pyautogui.click(1050 + i*25, 744)

# x, y = pyautogui.locateCenterOnScreen('remote.png')
# pyautogui.click(x, y)
#pyautogui.click(x, y)
while True:
    pyautogui.screenshot('myscreen.png')
    os.system('osascript ~/lnchr.scpt')
    cnt = cnt + 1
    print ("clciked " +  str(cnt))
    # for pos in pyautogui.locateAllOnScreen('remote.png'):
    #     print(pos)
    time.sleep(60 * 4)