from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def RunApp():
    desired_caps = {}
    desired_caps["app"] = "C:/Users/Harsh/Downloads/TH43dev/TH43dev/MTCppGUIDriver/vc12/x86/Release/MTCppGUIDriver.exe"
    desired_caps["platformName"] = "Windows"
    desired_caps["deviceName"] = "Windows"
    desired_caps["appWorkingDir"] = "C:/Users/Harsh/Downloads/TH43dev/TH43dev/MTCppGUIDriver/vc12/x86/Release"
    global driver
    driver= webdriver.Remote(
        command_executor='http://127.0.0.1:4723',
        desired_capabilities= desired_caps)

def Flashcase():
    time.sleep(0.5)
    driver.find_element_by_accessibility_id('1016').click()     #New
    driver.find_element_by_accessibility_id('1019').send_keys("Hello")      #Popup
    driver.find_element_by_name("OK").click()

def Thermocase():
    driver.find_element_by_accessibility_id("1012").click()     #New
    driver.find_element_by_accessibility_id('1019').send_keys("Hello")      #Popup
    driver.find_element_by_name("OK").click()

def RunGUI():
    driver.find_element_by_accessibility_id("1017").click()     #RUN GUI
    time.wait(2)

def Add_Components():
    comp_list="C1,C2,C3,H2O"
    for comp in comp_list.split(','):
        driver.find_element_by_accessibility_id('1355').send_keys(comp)     #Add Component
        driver.find_element_by_name('Add').click()

def Change_Family():
    Comp_Family_Name="<Edlib>:SIMSCI"
    #Comp_Family_Name="Ketones"
    CompF_List=driver.find_element_by_accessibility_id('1376')      #Component Family Acids, Ketones Etc
    for i in range(30):
        if CompF_List.text != Comp_Family_Name:
            try:
                driver.find_element_by_accessibility_id('1376').send_keys('%\ue015')
            except:
                print("List Not Found")
        else:
            break

def Save_Export():
    driver.find_element_by_name('Save').click()
    driver.find_element_by_name('OK').click()
    driver.find_element_by_name('Export...').click()
    driver.implicitly_wait(5)
    try:
        driver.find_element_by_class_name('Edit').find_element_by_accessibility_id('1001').send_keys(r'E:\Tests\Case4')
    except:
        driver.find_element_by_name('File name:').send_keys(r'E:\Tests\Case4')
    driver.find_element_by_name('Save').click()
    try:
        if driver.find_element_by_name('Confirm Save As'):
            driver.implicitly_wait(5)
            driver.find_element_by_name('Yes').click()
    except:
        pass

def Add_Petro():
    y = 65
    driver.find_element_by_name('Petro').click()
    time.sleep(0.5)
    comp_list = "P1,P2,P3,P4"
    for comp in comp_list.split(','):
        driver.find_element_by_accessibility_id('1604').send_keys(comp)     #Add Petro Component
        driver.find_element_by_name('Add').click()
    actions = ActionChains(driver)
    actions.reset_actions()
    ele = driver.find_element_by_accessibility_id('1609')       #Grid Finding
    actions.move_to_element_with_offset(ele, 135, y).click()
    for i in range(4):
        y += 18
        actions.send_keys('100\ue004')                          #Data Entry
        actions.send_keys('200\ue004')
        actions.send_keys('300\ue004')
        actions.send_keys('%\ue015').send_keys(Keys.ARROW_DOWN)
        actions.send_keys(Keys.TAB)
        actions.send_keys('%\ue015')
        actions.send_keys(Keys.TAB)
        actions.perform()
        actions.reset_actions()
        actions.move_to_element_with_offset(ele, 140, y).click()
    driver.find_element_by_accessibility_id('1605').click()

def Add_Cutset():
    driver.find_element_by_name('Cut Set').click()
    comp_list = "C1,C2,C3,C4,C5"
    y=65
    time.sleep(2)
    for comp in comp_list.split(','):
        driver.find_element_by_accessibility_id('1192').send_keys(comp)
        driver.find_element_by_name('Add').click()
    driver.find_element_by_accessibility_id('1198').click()         #No of Cuts
    driver.find_element_by_accessibility_id('1201').click()         #Temperature Increment
    driver.find_element_by_accessibility_id('1194').click()         #Individual Temperature
    actions = ActionChains(driver)
    actions.reset_actions()
    ele=driver.find_element_by_accessibility_id('1193')
    actions.move_to_element_with_offset(ele, 50, y).click()
    for i in range(1):
        y += 18
        actions.send_keys('100\ue004').send_keys('200\ue004').send_keys('300\ue004').send_keys('400\ue004')
        actions.perform()
        actions.reset_actions()
        actions.move_to_element_with_offset(ele, 50, y).click()
    driver.find_element_by_accessibility_id('1202').click()

def Select_List():
    C_Name="C5"
    D_list=driver.find_element_by_accessibility_id('1196')  #Cutset Rename or Delete from Drop down
    driver.find_element_by_accessibility_id('1196').send_keys('+'+Keys.PAGE_UP)
    for i in range(20):
        if D_list.text != C_Name:
            try:
                driver.find_element_by_accessibility_id('1196').send_keys('%\ue015')
            except:
                print("List Not Found")
        else:
            break
    actions = ActionChains(driver)
    actions.context_click(D_list).send_keys(Keys.DOWN).send_keys(Keys.RETURN).perform()
    driver.find_element_by_name('Yes').click()
    actions.reset_actions()

def Exit_App():
    driver.find_element_by_name('Exit').click()

RunApp()
Flashcase()
Thermocase()
RunGUI()
Change_Family()
Add_Components()
Add_Petro()
Add_Cutset()
Select_List()
Save_Export()
Exit_App()