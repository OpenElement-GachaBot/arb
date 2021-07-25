import ark
import time
import pyautogui

bedX = 506
bedY = 465

with open('beds.txt') as f:
    first_line = f.readline()
    parts = first_line.split()
    if(len(parts) >= 2):
        bedX = int(parts[0])
        bedY = int(parts[1])
    else:
        print("YO BEDS FILE IS FUCKED HAHAH")
        print("FIX IT")
        time.sleep(30)
        exit()

ark.setParams(2.3, 2.3, 20)


print("10 seconds to alt tab back in")
time.sleep(10)

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


def openInventoryWithRetries(n):
    for i in range(n):
        if(ark.openInventory()):
            return True
    return False

def takeAllOverhead():
    while(ark.inventoryIsOpen() == False):
        ark.lookUp()
        openInventoryWithRetries(3)
    
    ark.takeAll()
    ark.closeInventory()
    ark.lookDown()

def loadStone(bedName):
    ark.bedSpawn(bedName, bedX, bedY)
    turnOn()
    takeAllOverhead()

    if(openInventoryWithRetries(6) == False):
        ark.depositOverhead()
        ark.accessBed()
        return

    ark.transferAll()
    ark.craft("blueprint flint", 40)
    ark.closeInventory()

    ark.depositOverhead()

    ark.accessBed()

def flintRoutine():
    if(openInventoryWithRetries(6) == False):
        ark.accessBed()
        return

    ark.craft("blueprint flint", 40)
    ark.takeAll("flint")
    ark.closeInventory()
    ark.depositOverhead()
    ark.accessBed()


count = 0
while(True):
    loadStone("bf_stone1")
    loadStone("bf_stone3")
    loadStone("bf_stone2")
    loadStone("bf_stone4")

    ark.bedSpawn("bf_flint1", bedX, bedY)
    turnOn()
    flintRoutine()
    ark.bedSpawn("bf_flint2", bedX, bedY)
    turnOn()
    flintRoutine()
    time.sleep(30)

    count += 1
    if(count > 2):
        count = 0
        ark.bedSpawn("suicide bed", bedX, bedY)
        time.sleep(40)
