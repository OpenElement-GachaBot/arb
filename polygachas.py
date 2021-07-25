import time
import pyautogui
import screen
import cv2
import numpy as np
import ark

clickX = 707
clickY = 303
count = 0


crystal_template = cv2.imread("templates/gacha_crystal.png", cv2.IMREAD_GRAYSCALE)
gen2suit_template = cv2.imread("templates/gen2suit.png", cv2.IMREAD_GRAYSCALE)
deposit_all_template = cv2.imread("templates/deposit_all.png", cv2.IMREAD_COLOR)
added_template = cv2.imread("templates/added_template.png", cv2.IMREAD_GRAYSCALE)

lower_cyan = np.array([90,255,255])
upper_cyan = np.array([110,255,255])

hsv = cv2.cvtColor(deposit_all_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
masked_template = cv2.bitwise_and(deposit_all_template, deposit_all_template, mask= mask)
deposit_all_gray_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)




def openInventoryBlocking():
    while(ark.openInventory() == False):
        continue


def checkWeGotRowOfCrystals():
    roi = screen.getScreen()[323:423,111:213]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crystal_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 5500000):
        return True
    return False

def checkWeGotCrystals():
    roi = screen.getScreen()[230:330,120:210]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crystal_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 5500000):
        return True
    return False

def canDeposit():
    roi = screen.getScreen()    
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, lower_cyan, upper_cyan)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_screen, deposit_all_gray_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 14000000):
        return True
    return False

def loadGacha(bed):
    ark.bedSpawn(bed, clickX, clickY)
    ark.step("w", 0.5)
    ark.step("down", 0.3)
    openInventoryBlocking()
    pyautogui.moveTo(1288, 278)
    pyautogui.click()
    for i in range(2):
        pyautogui.press('o')
        time.sleep(0.5)
        
    ark.closeInventory()
    ark.step('s', 0.3)
    ark.accessBed()

def pickupWithFSpam():
    pyautogui.press('c')
    ark.lookDown()
    ark.step('s', 1.5)
    for i in range(6):
        pyautogui.press('f')
        time.sleep(0.2)
        ark.step('w', 0.1)
    ark.step('w', 1.0)

    pyautogui.press('f')
        
    

def whipCrystals(bedName):
    ark.bedSpawn(bedName, clickX, clickY)

    pickupWithFSpam()

    ark.openMyInventory()

    
    ark.searchMyStacks("gacha")
    pyautogui.moveTo(167, 280, 0.1)
    pyautogui.click()
    time.sleep(1.0)

    count = 0
    while(checkWeGotRowOfCrystals()):
        for i in range(6):
            pyautogui.moveTo(167+(i*95), 280, 0.1)
            pyautogui.click()
            pyautogui.press('e')

        time.sleep(0.8)
        count += 6

    pyautogui.moveTo(165, 280)
    pyautogui.click()
    while(checkWeGotCrystals()):
        pyautogui.press('e')
        time.sleep(0.2)
        count += 1
        if(count > 300):
            break
    ark.closeInventory()

    pyautogui.press('c')
    ark.step('up', 0.9)

    while(canDeposit() == False):
        ark.step('a', 0.4)
        ark.step('w', 0.4)
        ark.step('d', 0.2)
        time.sleep(0.2)
        
    for i in range(8):
        pyautogui.press('e')
        time.sleep(0.2)
        while(ark.getBedScreenCoords() != None):
            pyautogui.press('esc')
            time.sleep(2.0)

    ark.step('up', 1.0)
    for i in range(6):
        pyautogui.press('e')
        time.sleep(0.2)
        while(ark.getBedScreenCoords() != None):
            pyautogui.press('esc')
            time.sleep(2.0)

    ark.openMyInventory()
    ark.dropItems("")
    ark.closeInventory()
    
    ark.lookDown()
    ark.lookDown()
    ark.step('s', 0.4)
    while(ark.accessBed() == False):
        ark.step('s', 0.2)
        time.sleep(2.0)


def run():
    count = 0
    while(True):
        loadGacha("bf_gacha1")
        loadGacha("bf_gacha2")
        loadGacha("bf_gacha3")
        loadGacha("bf_gacha4")
        whipCrystals("bf_gachacrystal1")
        whipCrystals("bf_gachacrystal2")
        time.sleep(500)
        count += 1
        if(count >= 2):
            ark.bedSpawn("suicide bed", clickX, clickY)
            time.sleep(30)
            count = 0
    
    
if __name__ == "__main__":
    time.sleep(10)
    run()
    
