import time
import pyautogui
import screen
import cv2
import numpy as np
import ark
import polygachas

clickX = 0
clickY = 0
count = 0

with open('beds.txt') as f:
    first_line = f.readline()
    parts = first_line.split()
    if(len(parts) >= 2):
        clickX = int(parts[0])
        clickY = int(parts[1])
    else:
        print("YO BEDS FILE IS FUCKED HAHAH")
        print("FIX IT")
        time.sleep(30)
        exit()


print("ARB Script")
print("you have 10 seconds to alt tab back into the game btw")
time.sleep(10)


sign_template = cv2.imread("templates/write_sign_template.png", cv2.IMREAD_COLOR)
signHsvLower = np.array([85,100,255])
signHsvUpper = np.array([105,120,255])
hsv = cv2.cvtColor(sign_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, signHsvLower, signHsvUpper)
masked_template = cv2.bitwise_and(sign_template, sign_template, mask= mask)
sign_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)


ark.setParams(2.4, 2.4, 20)

def canSeeSignText():
    roi = screen.getScreen()
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, signHsvLower, signHsvUpper)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_screen, sign_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 90000000):
        pyautogui.moveTo(960, 720)
        pyautogui.click()
        time.sleep(0.5)
        return True
    return False


def turnOn():
    roi = screen.getScreen()

    lower_blue = np.array([80,255,255])
    upper_blue = np.array([100,255,255])

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(roi, roi, mask= mask)
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    on_template = cv2.imread('templates/on.png', cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(on_template, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(on_template, on_template, mask= mask)
    on_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, on_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 3400000):
        pyautogui.press('e')
        canSeeSignText()


def openInventoryWithRetries(n):
    for i in range(n):
        if(ark.openInventory()):
            return True
        canSeeSignText()
    return False

def takeAllOverhead():
    while(ark.inventoryIsOpen() == False):
        ark.lookUp()
        openInventoryWithRetries(300)
    
    ark.takeAll()
    ark.closeInventory()
    ark.lookDown()

def takeGunpowder():
    turnOn()
    openInventoryWithRetries(100)
    ark.searchStructureStacks("gunpowder")
    pyautogui.moveTo(1296, 275)
    pyautogui.click()
    time.sleep(0.1)
    for i in range(10):
        pyautogui.press('a')
        time.sleep(0.5)
    
    ark.takeAll()
    ark.closeInventory()
    ark.lookUp()
    openInventoryWithRetries(100)
    ark.takeAll()
    ark.closeInventory()
    ark.step('left', 3.6)
    ark.lookDown()
    openInventoryWithRetries(100)
    ark.transferAll()
    ark.craft("advanced rifle", 10)
    ark.closeInventory()
    ark.lookUp()
    pyautogui.press('e')
    while(canSeeSignText()):
        ark.lookUp()
        pyautogui.press('e')
        time.sleep(3.0)
    ark.lookDown()
    ark.accessBed()

def addCharcoal():
    turnOn()
    openInventoryWithRetries(100)
    ark.searchStructureStacks("char")
    ark.takeAll()
    ark.closeInventory()
    takeAllOverhead()
    openInventoryWithRetries(100)
    ark.searchMyStacks("char")
    pyautogui.moveTo(167, 280, 0.1)
    pyautogui.click()
    for j in range(8): #transfer about 8 rows of charcoal
        for i in range(6):
            pyautogui.moveTo(167+(i*95), 280, 0.1)
            pyautogui.press('t')

    ark.closeInventory()
    ark.lookUp()
    pyautogui.press('e')
    while(canSeeSignText()):
        ark.lookUp()
        pyautogui.press('e')
        time.sleep(3.0)
    ark.lookDown()
    ark.accessBed()

def addStone():
    turnOn()
    openInventoryWithRetries(100)
    ark.searchStructureStacks("stone")
    ark.takeAll()
    ark.closeInventory()
    ark.lookUp()
    openInventoryWithRetries(100)
    ark.takeAll()
    ark.closeInventory()
    ark.lookDown()
    openInventoryWithRetries(100)
    ark.searchMyStacks("stone")
    pyautogui.moveTo(167, 280, 0.1)
    pyautogui.click()
    for j in range(4):
        for i in range(6):
            pyautogui.moveTo(167+(i*95), 280, 0.1)
            pyautogui.press('t')
        
    ark.closeInventory()
    ark.lookUp()
    pyautogui.press('e')
    while(canSeeSignText()):
        ark.lookUp()
        pyautogui.press('e')
        time.sleep(3.0)
    ark.lookDown()
    ark.accessBed()

def addFlint():
    turnOn()
    ark.step('left', 3.6)
    openInventoryWithRetries(100)
    ark.searchStructureStacks("flint")
    ark.takeAll()
    ark.closeInventory()
    takeAllOverhead()
    openInventoryWithRetries(100)
    ark.searchMyStacks("flint")
    pyautogui.moveTo(167, 280, 0.1)
    pyautogui.click()
    for j in range(6): #transfer flint
        for i in range(6):
            pyautogui.moveTo(167+(i*95), 280, 0.1)
            pyautogui.press('t')
        
    ark.searchStructureStacks("sparkpowder")
    pyautogui.moveTo(1296, 275)
    pyautogui.click()
    time.sleep(0.1)
    for i in range(10):
        pyautogui.press('a')
        time.sleep(0.5)
    ark.searchStructureStacks("gunpowder")
    pyautogui.moveTo(1296, 275)
    pyautogui.click()
    time.sleep(0.1)
    for i in range(10):
        pyautogui.press('a')
        time.sleep(0.5)

    ark.closeInventory()
    ark.lookUp()
    pyautogui.press('e')
    while(canSeeSignText()):
        ark.lookUp()
        pyautogui.press('e')
        time.sleep(3.0)
    ark.lookDown()
    ark.accessBed()

def addIngot():
    turnOn()
    openInventoryWithRetries(100)
    ark.searchStructureStacks("ingot")
    ark.takeAll()
    ark.closeInventory()
    takeAllOverhead()
    openInventoryWithRetries(100)
    ark.transferAll()
    ark.searchStructureStacks("advanced rifle")
    pyautogui.moveTo(1296, 275)
    pyautogui.click()
    time.sleep(0.1)
    for i in range(10):
        pyautogui.press('a')
        time.sleep(0.5)
    ark.closeInventory()
    ark.lookUp()
    pyautogui.press('e')
    while(canSeeSignText()):
        ark.lookUp()
        pyautogui.press('e')
        time.sleep(3.0)
    ark.lookDown()
    ark.accessBed()

count = 0
while(True):
    ark.bedSpawn("bf_gp1", clickX, clickY)
    takeGunpowder()

    ark.bedSpawn("bf_char1", clickX, clickY)
    addCharcoal()

    ark.bedSpawn("bf_stone5", clickX, clickY)
    addStone()

    ark.bedSpawn("bf_flint1", clickX, clickY)
    addFlint()

    polygachas.loadGacha("bf_gacha1")
    polygachas.loadGacha("bf_gacha2")
    
    ark.bedSpawn("bf_gp2", clickX, clickY)
    takeGunpowder()

    ark.bedSpawn("bf_char2", clickX, clickY)
    addCharcoal()

    ark.bedSpawn("bf_stone6", clickX, clickY)
    addStone()

    ark.bedSpawn("bf_flint2", clickX, clickY)
    addFlint()

    ark.bedSpawn("bf_gp1", clickX, clickY)
    takeGunpowder()

    ark.bedSpawn("bf_arb1", clickX, clickY)
    turnOn()
    openInventoryWithRetries(100)
    ark.searchStructureStacks("adv")
    ark.takeAll()
    ark.closeInventory()
    ark.lookUp()
    pyautogui.press('e')
    while(canSeeSignText()):
        ark.lookUp()
        pyautogui.press('e')
        time.sleep(3.0)
    ark.lookDown()
    ark.accessBed()

    ark.bedSpawn("bf_gpcraft2", clickX, clickY)
    openInventoryWithRetries(100)
    ark.craft("gunpowder", 20)
    ark.closeInventory()
    ark.accessBed()

    polygachas.loadGacha("bf_gacha3")
    polygachas.loadGacha("bf_gacha4")
    
    ark.bedSpawn("bf_gp2", clickX, clickY)
    takeGunpowder()
    
    ark.bedSpawn("bf_arb2", clickX, clickY)
    turnOn()
    openInventoryWithRetries(100)
    ark.searchStructureStacks("adv")
    ark.takeAll()
    ark.closeInventory()
    ark.lookUp()
    pyautogui.press('e')
    while(canSeeSignText()):
        ark.lookUp()
        pyautogui.press('e')
        time.sleep(3.0)
    ark.lookDown()
    ark.accessBed()
    
    ark.bedSpawn("bf_ingot1", clickX, clickY)
    addIngot()

    ark.bedSpawn("bf_ingot2", clickX, clickY)
    addIngot()

    ark.bedSpawn("bf_gpcraft1", clickX, clickY)
    openInventoryWithRetries(100)
    ark.craft("gunpowder", 20)
    ark.closeInventory()
    ark.accessBed()

    polygachas.whipCrystals("bf_gachacrystal1")
    polygachas.whipCrystals("bf_gachacrystal2")

    count += 1
    if(count >= 2):
        count = 0
        ark.bedSpawn("suicide bed", 705, 302)
        time.sleep(25)
