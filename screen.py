import pyautogui
import time
cnt = 0

while True:
    pyautogui.moveTo(100, 150)

    for i in range(1, 4):
        pyautogui.click(1050 + i*25, 773)

    # x, y = pyautogui.locateCenterOnScreen('remote.png')
    # pyautogui.click(x, y)
    #pyautogui.click(x, y)
    pyautogui.screenshot('myscreen.png')
    cnt = cnt + 1
    print ("clciked " +  str(cnt))
    # for pos in pyautogui.locateAllOnScreen('remote.png'):
    #     print(pos)
    time.sleep(60 * 7)