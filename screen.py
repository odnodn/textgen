import pyautogui
import time
cnt = 0

while True:
    pyautogui.moveTo(100, 150)
    for i in range(1, 4):
        pyautogui.click(1050 + i*25, 773)

    pyautogui.click(500, 300)
    pyautogui.screenshot('myscreen.png')
    cnt = cnt + 1
    print ("clciked " +  str(cnt))
    time.sleep(60 * 7)