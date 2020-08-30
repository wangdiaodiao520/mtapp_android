from func import *



readfile = ReadFile()
citys    = readfile.get_citys()

ads      = ADS()

openapp  = OpenApp()
driver   = openapp.open('4723')
x,y      = openapp.get_size(driver)

mt       = MeiTuan(driver,x,y)

mt_phone = NewYiMa()


for city in citys:
    #当前城市采集点和经纬度：{地点：纬度，经度，···}
    address = readfile.get_file(city)
    city = city.replace('市.xlsx','')
    for i in address:
        ad = i['ad']
        jw = i['jw']
        print(city,ad,jw)
        mt.pass_html(driver)
        mt.login_for_wx(driver)
        mt.goto_waimai(driver)
        mt.click_ad(driver)
        mt.change_city(driver,city)
        ad_items = mt.input_ad(driver,ad)
        ad_data  = mt.handle_ad_items(ad_items)
        abs_ad = []
        for i in ad_data:
            print(i)
            i_jw = ads.get_ad_jw(city + '市' + i)
            abs_ = ads.handle_jw(jw,i_jw)
            print(abs_)
            abs_ad.append(abs_)
            time.sleep(1)
        abs_ad_min = min(abs_ad)
        index      = abs_ad.index(abs_ad_min)
        ad_items[index].click()
        mt.swip_to_list(driver)
        mt.relocation(driver)
        items = mt.get_comity_list(driver)
        print(items)
        num = 0
        names = []
        re_ad,names,num = mt.handle_items(driver,items,names,num)
        while num < 300:
            mt.reswip(driver,re_ad)
            items = mt.get_comity_list(driver)
            re_ad,names,num = mt.handle_items(driver,items,names,num)
        #回到顶部
            
        
            
            
        
            






















            
        
    
    
