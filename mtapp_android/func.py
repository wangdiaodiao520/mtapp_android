from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import time
import os
import xlrd
import requests
import json

from newyima import NewYiMa
from search_ad_url import search_ad_url




class OpenApp():
    '''
    美团app
    '''
    def __init__(self):
        self.caps = {
            "platformName": "Android",#平台
            "deviceName": "HWYAL-O",#手机devices名，通过adb获取
            "appPackage": "com.sankuai.meituan",#app包名
            "appActivity": "com.meituan.android.pt.homepage.activity.Welcome",#app activity入口
            "autoGrantPermissions":True,  # 设置自动授权权限
            "unicodeKeyboard":True,  # 输入中文时要加，要不然输入不了中文
            "resetKeyboard":True,  # 输入中文时要加，要不然输入不了中文 
            }

    def open(self,port='4723'):
        driver = webdriver.Remote('http://localhost:{}/wd/hub'.format(port),self.caps)
        return driver

    def get_size(self,driver):
        #获取当前手机尺寸与测试机屏幕尺寸比例
        x = driver.get_window_size()['width']/1080
        y = driver.get_window_size()['height']/2159
        return x,y


class HandleImg():
    pass



class MeiTuan():
    '''
    美团app操作
    '''
    def __init__(self,driver,x,y):
        self.wait = WebDriverWait(driver,5)
        self.x = x
        self.y = y
        self.hot_city = ['北京','上海','广州','深圳','成都','杭州','南京','苏州','重庆','天津','武汉','西安']

    def pass_html(self,driver):
        #过掉干扰界面
        time.sleep(10)
        TouchAction(driver).tap(x=int(540*self.x), y=int(950*self.y)).perform()
        time.sleep(3)
        driver.back()
        time.sleep(3)
        TouchAction(driver).tap(x=int(540*self.x), y=int(950*self.y)).perform()
        time.sleep(3)
        driver.back()
        return

    def login_for_phone(self,driver,mt_phone):
        #手机号登陆
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.view.View[@content-desc="外卖"]')))
        #点击登陆
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/button'))).click()
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_am_window')))
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_policy_agree'))).click()
        phone = mt_phone.get_phone()
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_mobile_phone'))).send_keys(phone)
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_mobile_next'))).click()
        #判断是否出现滑块验证
        time.sleep(10)
        try:
            driver.find_elements_by_android_uiautomator ('new UiSelector().resourceId("com.sankuai.meituan:id/yoda_dialog_container")')
            #wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/yoda_dialog_container')))
            hk = True
        except:
            hk = False
        print(hk)
        if hk:
            start = driver.find_element_by_id('com.sankuai.meituan:id/yoda_slider_block').get_attribute('bounds')
            end   = driver.find_element_by_id('com.sankuai.meituan:id/yoda_slider_window_lock').get_attribute('bounds')
            start_x,start_y = self.handle_bounds(start)
            end_x,end_y     = self.handle_bounds(end)
            trace = end_x - start_x
            print('1')
            TouchAction(driver).press(x=start_x, y=start_y)\
                                                 .move_to(x=start_x+1/10*trace,y=start_y)\
                                                 .move_to(x=start_x+3/10*trace,y=start_y)\
                                                 .move_to(x=start_x+7/10*trace,y=start_y)\
                                                 .move_to(x=start_x+trace,y=start_y)\
                                                 .release().perform()
            time.sleep(5)
                                                 
        #此处睡眠10s，给短信接收和页面跳转更多时间
        time.sleep(10)
        code = list(mt_phone.get_code(phone))
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/num_i')))
        for i in code:
            driver.press_keycode(int(i)+7)
            time.sleep(1)
        return

    def login_for_wx(self,driver):
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.view.View[@content-desc="外卖"]')))
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/button'))).click()
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_am_window')))
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/passport_policy_agree'))).click()
        TouchAction(driver).tap(x=int(395*self.x), y=int(1875*self.y)).perform()#点击微信登陆
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.view.View[@content-desc="外卖"]')))
        return

    def goto_waimai(self,driver):
        #进入外卖页
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.view.View[@content-desc="外卖"]'))).click()
        self.pass_html(driver)
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.TextView[@text="送药上门"]')))
        time.sleep(3)   
        return

    def swip_to_list(self,driver):
        while True:
            driver.swipe(int(500*self.x),int(2000*self.y),int(500*self.x),int(1200*self.y),1000)
            time.sleep(1)
            #检查是否到商家列表
            if self.check_waimai_page(driver):
                break    
        return

    def check_waimai_page(self,driver):
        #判断是否到达商家列表
        try:
            driver.find_element_by_id('com.sankuai.meituan:id/tab_hot')
            return True
        except:
            return False

    def relocation(self,driver):
        #重新定位商家列表
        location = driver.find_element_by_id('com.sankuai.meituan:id/tab_hot').get_attribute('bounds')[5:9]
        if ']' in location:
            location = driver.find_element_by_id('com.sankuai.meituan:id/tab_hot').get_attribute('bounds')[5:8]
        driver.swipe(int(500*self.x),int(int(location)*self.y),int(500*self.x),int(350*self.y),1000)
        time.sleep(1)
        return

    def get_comity_list(self,driver):
        #获取商家列表
        items = driver.find_elements_by_android_uiautomator ('new UiSelector().resourceId("com.sankuai.meituan:id/parent")')
        return items

    def get_comity_main_data(self,item):
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
            data['pp'] = 'yes'
        except:
            data['pp'] = 'no'
        return data

    def goto_comity(self,item):
        item.click()
        try:
            self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/txt_comment_num')))
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.TextView[@text="商家"]'))).click()
            self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/view_poi_phone')))
        except:
            self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/more_item'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.TextView[@text="商家详情"]'))).click()
            #第二种页面，还没想好如何定位，出现概率很低
        return
        
    def get_comity_info_data(self,driver):
        #获取商家数据
        data = {}
        data['com_ad'] = driver.find_element_by_id('com.sankuai.meituan:id/txt_poi_address').get_attribute('text')
        data['com_pl'] = driver.find_element_by_id('com.sankuai.meituan:id/txt_comment_num').get_attribute('text')
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/view_poi_phone'))).click()
        #phone_ele = driver.find_elements_by_android_uiautomator ('new UiSelector().resourceId("com.sankuai.meituan:id/dialog_item_text")')
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/dialog_item_text')))
        phone_ele = driver.find_elements_by_id('com.sankuai.meituan:id/dialog_item_text')
        phone = []
        for i in phone_ele:
            phone.append(i.get_attribute('text'))        
        data['com_phone'] = phone
        driver.back()
        driver.back()
        return data

    def handle_items(self,driver,items,names,num):
        #处理商家列表数据
        names_ = []
        datas  = []
        for item in items:
            #因当前页数据不全，获取数据出错，忽略此错误，下滑后再获取
            try:
                data = self.get_comity_main_data(item)
            except:
                data = {}
            if data and data['name'] not in names:
                self.goto_comity(item)
                #防止打烊店铺
                try:
                    com_data = self.get_comity_info_data(driver)
                except:
                    driver.back()
                    com_data = self.get_comity_info_data(driver)
                print({**data,**com_data})
                datas.append({**data,**com_data})
        for i in datas:
            names_.append(i['name'])#新的已经处理商家名称集
        ad = datas[-1]['logo_ad'][4:8]#记录最新数据定位，滑动使用
        if ']' in ad:
            ad = datas[-1]['logo_ad'][4:7]
        return int(ad),names_,num+len(datas)

    def reswip(self,driver,ad):
        #下拉刷新新的商家
        driver.swipe(int(500*self.x),int(int(ad)*self.y),int(500*self.x),int(485*self.y),1000)

    def click_ad(self,driver):
        #点击地址选择
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/actionbar_txt'))).click()

    def goto_top(self,driver):
        pass

    def change_city(self,driver,city):
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/wm_address_city_location_text'))).click()
        xpath_str = '//android.widget.TextView[@text="{}"]'.format(city)
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.EditText[@text="输入城市名进行搜索"]'))).send_keys(city)
        time.sleep(3)
        self.wait.until(EC.presence_of_element_located((By.XPATH,xpath_str))).click()

    def input_ad(self,driver,ad):
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/address_search_map_txt'))).click()
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/address_search_map_txt'))).send_keys(ad)
        time.sleep(1)
        #items = self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.support.v7.widget.RecyclerView[@resource-id="com.sankuai.meituan:id/list_map_location_info"]/android.widget.LinearLayout')))
        items = driver.find_elements_by_android_uiautomator ('new UiSelector().resourceId("com.sankuai.meituan:id/txt_map_adapter_name")')
        #考虑：用bounds下拉一页，取二十个，对比相似度，如果相似度打到**，不进行经纬度查询直接选用
        return items

    def handle_ad_items(self,items):
        ad_data = []
        for item in items:
            ad = item.get_attribute('text')
            ad_data.append(ad)
        return ad_data

    def handle_bounds(self,data):
        info = data.replace('[','').replace(']',',')
        info = info.split(',')
        x1 = info[0]
        x2 = info[2]
        y1 = info[1]
        y2 = info[3]
        x  = int((int(x1) + int(x2))/2)
        y  = int((int(y1) + int(y2))/2)
        return x,y



class ADS():
    def __init__(self):
        self.url = search_ad_url

    def get_ad_jw(self,ad):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
            }
        search_url = self.url.format(ad) 
        rep = requests.get(search_url,headers=headers)
        rep = rep.text[11:-1]
        rep = json.loads(rep)
        jw = rep['pois'][0]['location'].replace('.','')
        return jw

    def handle_jw(self,jw,get_jw):
        jw = jw.split(',')
        getjw = get_jw.split(',')
        j_c = int(jw[1]) - int(getjw[0])
        w_c = int(jw[0]) - int(getjw[1])
        if j_c < 0:
            j_c = -j_c
        if w_c < 0:
            w_c = -w_c
        return j_c + w_c



class ReadFile():
    def __init__(self):
        pass

    def get_citys(self):
        data = []
        path = os.getcwd()
        dirs = os.listdir(path)
        for i in dirs:
            if 'xlsx' in i:
                data.append(i)
        return data

    def get_file(self,path):
        data = []
        path = (os.getcwd() + '\\' + path).replace('~$','')
        f = xlrd.open_workbook(path)
        table = f.sheet_by_index(0)
        data_ad = table.col_values(0)
        data_wd = table.col_values(1)
        data_jd = table.col_values(2)
        for i in range(len(data_ad)):
            #data[data_ad[i]] = str(int(data_wd[i])) + ',' + str(int(data_jd[i]))
            data.append({'ad':data_ad[i],'jw':str(int(data_wd[i])) + ',' + str(int(data_jd[i]))})
        return data









#a = ADS()
#print(a.get_ad_jw('广州市龙烨军事体育培训中心'))


















    
