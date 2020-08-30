from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
import time
from newyima import NewYiMa
import random


mt = NewYiMa()
def client_phone():
    caps = {
        "platformName": "Android",#平台
        "deviceName": "HWYAL-O",#手机devices名，通过adb获取
        "appPackage": "com.sankuai.meituan",#app包名
        "appActivity": "com.meituan.android.pt.homepage.activity.Welcome",#app activity入口
        "autoGrantPermissions":True,  # 设置自动授权权限
        "unicodeKeyboard":True,  # 输入中文时要加，要不然输入不了中文
        "resetKeyboard":True,  # 输入中文时要加，要不然输入不了中文 
            }
    driver = webdriver.Remote('http://localhost:4723/wd/hub',caps)
    return driver

def get_phone_size(driver):
    #获取当前手机尺寸与测试机屏幕尺寸比例
    x = driver.get_window_size()['width']/1080
    y = driver.get_window_size()['height']/2159
    return x,y

def handle_bounds(data):
    info = data.replace('[','').replace(']',',')
    info = info.split(',')
    x1 = info[0]
    x2 = info[2]
    y1 = info[1]
    y2 = info[3]
    x  = int((int(x1) + int(x2))/2)
    y  = int((int(y1) + int(y2))/2)
    return x,y

def get_trace(distance):
    trace = []
    current = 0
    mid = distance*3/4
    t = random.randint(2,3)/10
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a*t
        move = v0*t + 1/2*a*t*t
        current += move
        trace.append(round(move))
    return trace


def login(driver,wait,x,y):
    #登陆，采用的微信登陆
    #等待检查
    try:
        wait.until(EC.presence_of_element_located((By.XPATH,'//android.view.View[@content-desc="外卖"]')))
        time.sleep(3)
        TouchAction(driver).tap(x=int(960*x), y=int(2000*y)).perform()#点击登陆
        #等待检查
        wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_am_window')))
        #TouchAction(driver).tap(x=785*x, y=1820*y).perform()#同意协议
        wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_policy_agree'))).click()
        #等待检查
        #wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_mobile_next')))
        #time.sleep(3)
        #TouchAction(driver).tap(x=int(395*x), y=int(1875*y)).perform()#点击微信登陆
        #等待检查
        #wait.until(EC.presence_of_element_located((By.XPATH,'//android.view.View[@content-desc="外卖"]')))
        phone = mt.get_phone()
        wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_mobile_phone'))).send_keys(phone)
        time.sleep(3)
        wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_mobile_next'))).click()
        '''
        #判断是否出现滑块验证
        wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/yoda_dialog_container')))
        start = driver.find_element_by_id('com.sankuai.meituan:id/yoda_slider_block').get_attribute('bounds')
        end   = driver.find_element_by_id('com.sankuai.meituan:id/yoda_slider_window_lock').get_attribute('bounds')
        start_x = handle_bounds(start)
        end_x = handle_bounds(end)
        distance = end_x - start_x
        print(distance)
        trace = get_trace(distance)
        print(trace)
        slider = wait.until(EC.presence_of_element_located((By.ID, 'com.sankuai.meituan:id/yoda_slider_window_green_block')))
        print('1')
        ActionChains(driver).click_and_hold(slider).perform()
        print('1')
        for x in trace:
            ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        print('3')
        ActionChains(driver).release().perform()
        print('2')
        '''
        wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/num_i')))
        code = list(mt.get_code(phone))
        print(code)
        '''
        time.sleep(3)
        input_code_ele = driver.find_elements_by_android_uiautomator ('new UiSelector().resourceId("com.sankuai.meituan:id/num_a")')
        for i in range(4):
            input_code_ele[i].send_keys(code[i])
            time.sleep(1)
        '''
        for i in code:
            driver.press_keycode(int(i)+7)
            time.sleep(1)
        
        return
    except:
        TouchAction(driver).tap(x=int(540*x), y=int(1500*y)).perform()
        time.sleep(3)
        raise

def get_in_waimai(driver,wait,x,y):
    try:
        #进入外卖页
        wait.until(EC.presence_of_element_located((By.XPATH,'//android.view.View[@content-desc="外卖"]'))).click()
        #检查等待
        wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.TextView[@text="送药上门"]')))
    except:
        #滑动屏幕出发红包优惠页
        TouchAction(driver).tap(x=int(540*x), y=int(1500*y)).perform()
        time.sleep(3)
        raise
    #下拉至数据页
    time.sleep(2)
    #for i in range(3):
    while True:
        driver.swipe(int(500*x),int(2000*y),int(500*x),int(1200*y),1000)
        time.sleep(1)
        #检查是否到商家列表
        if check_waimai(driver):
            break
    
    return

def check_waimai(driver):
    #判断是否到达商家列表
    try:
        driver.find_element_by_id('com.sankuai.meituan:id/tab_hot')
        #wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/tab_hot')))
        return True
    except:
        return False

def relocation(driver,wait,x,y):
    #重新定位商家列表
    m = driver.find_element_by_id('com.sankuai.meituan:id/tab_hot').get_attribute('bounds')[5:9]
    if ']' in m:
        m = driver.find_element_by_id('com.sankuai.meituan:id/tab_hot').get_attribute('bounds')[5:8]
    driver.swipe(int(500*x),int(int(m)*y),int(500*x),int(350*y),1000)
    #TouchAction(driver).press(x=int(500*x),y=int(int(m)*y)).move_to(x=int(500*x),y=int(350*y)).release().perform()
    time.sleep(1)
    return

def get_comity_list(driver,wait):
    #获取商家列表
    #items = wait.until(EC.presence_of_all_elements_located((By.ID,'com.sankuai.meituan:id/parent')))
    items = driver.find_elements_by_android_uiautomator ('new UiSelector().resourceId("com.sankuai.meituan:id/parent")')
    return items

def get_comity_list_data(item):
    #获取列表页数据
    data = {}
    data['logo_ad'] = item.find_element_by_id('com.sankuai.meituan:id/img_poiList_adapter_poi_image_border').get_attribute('bounds')
    data['name'] = item.find_element_by_id('com.sankuai.meituan:id/textview_poi_name').get_attribute('text')
    data['point'] = item.find_element_by_id('com.sankuai.meituan:id/layout_poi_rating_sales').get_attribute('text')
    data['mouth_sale'] = item.find_element_by_id('com.sankuai.meituan:id/textview_month_sales_tip').get_attribute('text')
    data['distance_time'] = item.find_element_by_id('com.sankuai.meituan:id/layout_poi_distance_time').get_attribute('text')
    data['price_info'] = item.find_element_by_id('com.sankuai.meituan:id/layout_poi_price_info').get_attribute('text')
    data['tips_ad'] = item.find_element_by_id('com.sankuai.meituan:id/flowlayout_recommend_list_tags').get_attribute('bounds')
    data['activities_ad'] = item.find_element_by_id('com.sankuai.meituan:id/tag_activities_line').get_attribute('bounds')
    try:
        item.find_element_by_id('com.sankuai.meituan:id/imageview_type_icon')
        data['pp_t_or_f'] = 'yes'
    except:
        data['pp_t_or_f'] = 'no'
    return data

def get_in_comity_data(driver,wait):
    #进入商家页
    #ccc = comity_list_xpath+'[{}]'.format(str(num+1))
    #wait.until(EC.presence_of_element_located((By.XPATH,ccc))).click()
    wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/txt_comment_num')))#判断进入页面
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.TextView[@text="商家"]'))).click()
    wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/view_poi_phone')))#判断已跳转
    time.sleep(1)
    data = {}
    data['com_ad'] = driver.find_element_by_id('com.sankuai.meituan:id/txt_poi_address').get_attribute('text')
    #data['com_fw'] = driver.find_element_by_id('com.sankuai.meituan:id/txt_third_party_delivery_tip').get_attribute('text')
    #data['com_fw_time'] = driver.find_element_by_id('com.sankuai.meituan:id/txt_delivery_time').get_attribute('text')
    #data['com_pl'] = driver.find_element_by_id('com.sankuai.meituan:id/txt_comment_num').get_attribute('text')
    data['com_pl'] = wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/txt_comment_num'))).get_attribute('text')
    #com_info = driver.find_element_by_id('com.sankuai.meituan:id/shop_impression_layout')
    #data['com_info'] = com_info.find_element_by_id('com.sankuai.meituan:id/shop_impress_desc').get_attribute('text')
    #driver.find_element_by_id('com.sankuai.meituan:id/view_poi_phone').click()
    
    wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/view_poi_phone'))).click()
    data['com_phone'] = wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/dialog_item_text'))).get_attribute('text')
    #return data
    driver.back()
    #检查等等
    time.sleep(1)
    driver.back()
    #检查等等
    time.sleep(1)
    return data

def handle_comity_list(items,names):
    #处理商家列表数据
    names_ = []
    datas = []
    for item in items:
        try:
            #因当前页数据不全，获取数据出错，忽略此错误，下滑后再获取
            data = get_comity_list_data(item)
        except:
            data = {}
        if data and data['name'] not in names:
            item.click()
            try:
                #防止打烊店铺
                com_data = get_in_comity_data(driver,wait)
            except:
                driver.back()
                com_data = get_in_comity_data(driver,wait)
            #save(data)
            print({**data,**com_data})
            datas.append({**data,**com_data})
    for i in datas:
        names_.append(i['name'])#新的已经处理商家名称集
    com_relocation = datas[-1]['logo_ad'][4:8]#记录最新数据定位，滑动使用    
    if ']' in com_relocation:
        com_relocation = datas[-1]['logo_ad'][4:7]
    return int(com_relocation),names_


def com_relocation_reswip(driver,wait,x,y,com_logo_ad):
    driver.swipe(int(500*x),int(int(com_logo_ad)*y),int(500*x),int(485*y),1000)
    return
    

def save(data):
    pass
    
    


driver = client_phone()
wait = WebDriverWait(driver,10)
x,y = get_phone_size(driver)
time.sleep(5)
try:
    #防止出现红包优惠页等干扰
    login(driver,wait,x,y)
except:
    driver.back()
    login(driver,wait,x,y)


try:
    #防止出现红包优惠页等干扰
    get_in_waimai(driver,wait,x,y)
except:
    driver.back()
    get_in_waimai(driver,wait,x,y)

    
relocation(driver,wait,x,y)

items = get_comity_list(driver,wait)
names = []

com_relocation,names = handle_comity_list(items,names)

while True:
    com_relocation_reswip(driver,wait,x,y,com_relocation)
    #等待加载数据当前页载数
    time.sleep(1)
    items = get_comity_list(driver,wait)
    com_relocation,names = handle_comity_list(items,names)
        
        













