import os
import xlrd
from search_ad_url import url
import requests
import json
#
#

hot_city = ['北京','上海','广州','深圳','成都','杭州','南京','苏州','重庆','天津','武汉','西安']

def get_citys():
    data = []
    path = os.getcwd()
    dirs = os.listdir(path)
    for i in dirs:
        if 'xlsx' in i:
            data.append(i)
    return data

def get_file(path):
    data = {}
    path = (os.getcwd() + '\\' + path).replace('~$','')
    f = xlrd.open_workbook(path)
    table = f.sheet_by_index(0)
    data_ad = table.col_values(0)
    data_wd = table.col_values(1)
    data_jd = table.col_values(2)
    for i in range(len(data_ad)):
        data[data_ad[i]] = str(int(data_wd[i])) + ',' + str(int(data_jd[i]))
    return data
        

def click_ad(driver,wait):
    wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/actionbar_txt'))).click()

def change_city(driver,wait,city):
    wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/wm_address_city_location_text'))).click()
    if city in hot_city:
        wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.TextView[@text="{}"]'.format(city)))).click()
    else:
        wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.EditText[@text="输入城市名进行搜索"]'))).send_keys(city)
        wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.TextView[@text="{}"]'.format(city)))).click()

def search_ad(driver,wait,ad):
    wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/address_search_map_txt'))).click()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.ID,'com.sankuai.meituan:id/address_search_map_txt'))).send_keys(ad)
    time.sleep(1)
    driver.back()
    items = wait.until(EC.presence_of_element_located((By.XPATH,'//android.support.v7.widget.RecyclerView[@resource-id="com.sankuai.meituan:id/list_map_location_info"]/android.widget.LinearLayout')))
    return items

def handle_ad_items(items):
    ad_data = []
    for item in items:
        ad = item.find_element_by_id('com.sankuai.meituan:id/txt_map_adapter_name').get_attribute('text')
        ad_data.append(ad)
    return ad_data

def get_ad_jw(ad):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
    search_url = url.format(ad) 
    rep = requests.get(search_url,headers=headers)
    rep = rep.text[11:-1]
    rep = json.loads(rep)
    jw = rep['pois'][0]['location'].replace('.','')
    return jw

def handle_jw_and_getjw(jw,getjw):
    jw = jw.split(',')
    getjw = getjw.split(',')
    j_c = int(jw[0]) - int(getjw[0])
    w_c = int(jw[1]) - int(getjw[1])
    if j_c < 0:
        j_c = -j_c
    if w_c < 0:
        w_c = -w_c
    return j_c + w_c
























    
