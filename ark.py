import time
import pyautogui
import screen
import cv2
import numpy as np

inventory_template = cv2.imread("templates/inventory_template.png", cv2.IMREAD_COLOR)
invHsvLower = np.array([86,117,255])
invHsvUpper = np.array([106,137,255])
hsv = cv2.cvtColor(inventory_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, invHsvLower, invHsvUpper)
masked_template = cv2.bitwise_and(inventory_template, inventory_template, mask= mask)
inventory_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

img = cv2.imread("templates/bed_button_corner.png", cv2.IMREAD_GRAYSCALE)
bed_button_edge = cv2.Canny(img,100,200)

lookUpDelay = 3
lookDownDelay = 1.75

setFps = 25
firstRun = True


addedHsvLower = np.array([80,255,255]) 
addedHsvUpper = np.array([100,255,255])

added_template = cv2.imread("templates/added_template.png", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(added_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, addedHsvLower, addedHsvUpper)
masked_template = cv2.bitwise_and(added_template, added_template, mask= mask)
added_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)


removedHsvLower = np.array([20,255,255])
removedHsvUpper = np.array([40, 255, 255])

removed_template = cv2.imread("templates/removed_template.png", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(removed_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, removedHsvLower, removedHsvUpper)
masked_template = cv2.bitwise_and(removed_template, removed_template, mask= mask)
removed_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)


def limitFps():
    global setFps
    pyautogui.press("tab")
    time.sleep(0.2)
    pyautogui.typewrite("t.maxfps " + str(setFps), interval=0.02)
    pyautogui.press("enter")

def setGamma():
    pyautogui.press("tab")
    time.sleep(0.2)
    pyautogui.typewrite("gamma 5", interval=0.02)
    pyautogui.press("enter")


def setParams(up, down, fps):
    global lookUpDelay
    global lookDownDelay
    global setFps
    lookUpDelay = up
    lookDownDelay = down
    setFps = fps


def lookUp():
    global lookUpDelay
    pyautogui.keyDown('up')
    time.sleep(lookUpDelay)
    pyautogui.keyUp('up')

def lookDown():
    global lookDownDelay
    pyautogui.keyDown('down')
    time.sleep(lookDownDelay)
    pyautogui.keyUp('down')

def enterBedName(name):
    pyautogui.moveTo(336, 986, duration=0.1)
    pyautogui.click()
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.press('backspace')
    pyautogui.typewrite(name, interval=0.05)
    time.sleep(0.5)

def checkBedButtonEdge():
    img = screen.getGrayScreen()[950:1100,580:620]
    img = cv2.Canny(img, 100, 200)
    res = cv2.matchTemplate(img, bed_button_edge, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 2500000):
        return True
    return False


def canSeeAdded():
    roi = screen.getScreen()[0:1080,0:650]
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, addedHsvLower, addedHsvUpper)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_screen, added_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 6000000.0):
        return True
    return False


def canSeeRemoved():
    roi = screen.getScreen()[0:1080,0:750]
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, removedHsvLower, removedHsvUpper)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_screen, removed_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 14000000):
        return True
    return False

def detectWhiteFlash():
    roi = screen.getScreen()[700:900,0:1920]
    res1 = np.all([roi == 255])
    print(res1)
    return res1
    
def bedSpawn(bedName, x, y):
    global firstRun
    time.sleep(1.5)
    enterBedName(bedName)
    time.sleep(0.5)
    count = 0
    pyautogui.moveTo(x, y)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(1.0)
    """
    while(checkBedButtonEdge() == False):
        pyautogui.moveTo(x, y)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(2.0)
        count += 1
        if(count > 100):
            return False
    """
    pyautogui.moveTo(755, 983)
    time.sleep(0.25)
    pyautogui.click()
    count = 0
    while(detectWhiteFlash() == False):
        time.sleep(0.1)
        count += 1
        if(count > 100):
            break
    time.sleep(12)
    pyautogui.press('c')
    if(firstRun == True):
        firstRun = False
        limitFps()
        setGamma()
    return True


def inventoryIsOpen():# {{{
    roi = screen.getScreen()[90:150,100:300]
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, invHsvLower, invHsvUpper)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_screen, inventory_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 50000000.0):
        return True
    return False

    
def closeInventory():# {{{
    while(inventoryIsOpen() == True):
        pyautogui.moveTo(1816, 37)
        pyautogui.click()
        count = 0
        while(inventoryIsOpen()):
            count += 1
            if(count > 20):
                break
            time.sleep(0.1)
    time.sleep(1.0)

def craft(item, timesToPressA):
    searchStructureStacks(item)
    pyautogui.moveTo(1290, 280)
    pyautogui.click()
    for i in range(0, timesToPressA):
        pyautogui.press('a')
        time.sleep(0.25)

def searchMyStacks(thing):# {{{
    pyautogui.moveTo(144, 191)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.keyDown('ctrl')
    time.sleep(0.1)
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.typewrite(thing, interval=0.02)
    time.sleep(0.1)


def searchStructureStacks(thing):# {{{
    pyautogui.moveTo(1322, 191)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.keyDown('ctrl')
    time.sleep(0.1)
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.typewrite(thing, interval=0.02)
    time.sleep(0.1)
# }}}
def takeStacks(thing, count):# {{{
    searchStructureStacks(thing)
    pyautogui.moveTo(1287, 290)
    pyautogui.click()
    for i in range(count):
        pyautogui.press('t')
        time.sleep(1)
# }}}
def takeAll(thing = ""):
    if(thing != ""):
        time.sleep(0.1)
        pyautogui.moveTo(1285, 180)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        pyautogui.typewrite(thing, interval=0.01)
    pyautogui.moveTo(1424, 190)
    pyautogui.click()

def transferAll(thing = ""):# {{{
    if(thing != ""):
        pyautogui.moveTo(198, 191)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        pyautogui.typewrite(thing, interval=0.005)
        time.sleep(0.1)
    pyautogui.moveTo(351, 186)
    pyautogui.click()
    time.sleep(0.1)

def transferStacks(thing, count):# {{{
    pyautogui.moveTo(198, 191)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.typewrite(thing, interval=0.005)
    time.sleep(0.1)
    counter = 0
    pyautogui.moveTo(170, 280)
    pyautogui.click()
    time.sleep(0.2)
    while(counter < count):
        pyautogui.press('t')
        time.sleep(0.5)
        counter += 1

def openInventory():
    pyautogui.press('f')
    count = 0
    while(inventoryIsOpen() == False):
          count += 1
          if(count > 100):
              return False
          time.sleep(0.1)
          if(getBedScreenCoords() != None):
            pyautogui.press('esc')
            time.sleep(2.0)
    return True

def openMyInventory():
    pyautogui.press('i')
    count = 0
    while(inventoryIsOpen() == False):
          count += 1
          if(count > 100):
              return False
          time.sleep(0.1)
          if(getBedScreenCoords() != None):
            pyautogui.press('esc')
            time.sleep(2.0)
    return True

def tTransferTo(nRows):
    time.sleep(0.5)
    pyautogui.moveTo(167, 280, 0.1)
    pyautogui.click()
    for j in range(nRows): #transfer a few rows back to the gacha
        for i in range(6):
            pyautogui.moveTo(167+(i*95), 280, 0.1)
            pyautogui.press('t')

def tTransferFrom(nRows):
    pyautogui.moveTo(1288, 280, 0.1)
    pyautogui.click()
    for j in range(nRows):
        for i in range(6):
            pyautogui.moveTo(1288+(i*95), 280, 0.1)
            pyautogui.press('t')

def getBedScreenCoords():
    roi = screen.getScreen()

    lower_blue = np.array([90,200,200])
    upper_blue = np.array([100,255,255])


    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(roi, roi, mask= mask)
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    bed_template = cv2.imread('templates/bed_icon_template.png', cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(bed_template, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(bed_template, bed_template, mask= mask)
    bed_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)


    res = cv2.matchTemplate(gray_roi, bed_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 8000000):
        return (max_loc[0]+14, max_loc[1]+14)
    return None

def dropItems(thing):
    pyautogui.moveTo(198, 191)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.typewrite(thing, interval=0.02)
    time.sleep(0.5)
    pyautogui.moveTo(412, 190)
    pyautogui.click()


def accessBed():
    count = 0
    while(getBedScreenCoords() == None):
        lookDown()
        pyautogui.press('e')
        time.sleep(1.5)
        if(inventoryIsOpen()):
            closeInventory()
        count += 1
        if(count > 100):
            return False
    return True

def takeAllOverhead():
    lookUp()
    openInventory()
    takeAll()
    closeInventory()
    lookDown()

def depositOverhead():
    lookUp()
    pyautogui.press('e')
    lookDown()

def step(key, delay):
    pyautogui.keyDown(key)
    time.sleep(delay)
    pyautogui.keyUp(key)


def harvestCropStack(food):
    lookDown()
    step('s', 0.3)
    step('up', 0.8)

    for i in range(4):
        if(openInventory()):
            takeAll(food)
            transferAll()
            closeInventory()
        step('up', 0.1)

    pyautogui.press('c')
    step('down', 0.1)

    for i in range(4):
        if(openInventory()):
            takeAll()
            transferAll()
            closeInventory()
        step('up', 0.15)
    
    
            
    
