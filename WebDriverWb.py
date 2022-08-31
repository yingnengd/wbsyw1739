# -- coding: utf-8 --**
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import json,os
import random
# import psutil
import re,os,requests
from selenium.webdriver.common.action_chains import ActionChains

DRIVER_PATH = 'C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver.exe'
class DriverOptions(object):

    def __init__(self):
        """
        不打开浏览器运行
        """
        # 设置options参数
        self.options = webdriver.ChromeOptions()
        self.options = Options()
        self.options.add_argument("--no-sandbox")
        #self.options.add_argument('--user-agent=""')  # 设置请求头的User-Agent
        # self.options.add_argument('--remote-debugging-port=2222')
        # 可以启动一个监听端口始终为9222的chrome浏览器
        # self.options.add_experimental_option("debuggerAddress", "0.0.0.0:2222")
        # 可以让当前脚本连接到已打开的，监听端口为2222的chrome浏览器
        # self.options.add_argument('--window-size=1366x768')  # 设置浏览器分辨率（窗口大小）
        self.options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
        self.options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
        self.options.add_argument('--incognito')  # 隐身模式（无痕模式）
        #self.options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        #self.options.add_argument('--disable-javascript')  # 禁用javascript,如果觉得速度慢在加上这个
        self.options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        self.options.add_argument('--headless')  # 浏览器不提供可视化页面
        self.options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
        self.options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
        self.options.add_argument('--disable-gpu')  # 禁用GPU加速
        self.options.add_argument('–disable-software-rasterizer')
        self.options.add_argument('--disable-extensions')
        # 取消自动软件控制提示
        # self.options.add_argument("disable-infobars")
        # prefs = {
        #     'profile.default_content_setting_values': {'notifications': 2}
        # }
        # self.options.add_experimental_option("prefs", prefs)
        # global broswer

class WebDriver(DriverOptions):
    
    def __init__(self):
        DriverOptions.__init__(self)

    def get_driver(self):
        driver = webdriver.Chrome(options=self.options)
        # driver = webdriver.Chrome(DRIVER_PATH, options=self.options)
        return driver

    def broswer_initial(self,url):
        driver = self.get_driver()
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get(url)
        return driver

    def log_csdn(self,driver):
        with open('cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        # 往broswer里添加cookies
        for cookie in listCookies:
            cookie_dict = {
                'domain': '.weibo.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            driver.add_cookie(cookie_dict)

    def roll_targets_duo(self,driver,ele,n):
        # 获取页面初始高度
        target = driver.find_elements(By.XPATH,ele)
        driver.execute_script("arguments[0].scrollIntoView(false);", target[n])

    # 页面滑动至于目标元素，例如：滑动页面到第一个点赞评论行
    def roll_target(self,driver):
        # 获取页面初始高度
        target = driver.find_elements(By.XPATH,'.//div[@class="card-act"]')[0]
        driver.execute_script("arguments[0].scrollIntoView(false);", target)#false底对其，true顶对齐


    # total_num = 500
    #滚动至目标底端
    def roll_bottom(self, driver, ele, LOS):
    #LOS标本量事NONE，则向下拉5次700像素。不为NONE，则下拉到底5次，后者用于动态图床
        # c = int(n/25)
        for j in range(5):
            if LOS is None:
                # 将滚动条调整至页面底部
                driver.execute_script('window.scrollBy(0,700)')
                time.sleep(10)
            else:
                # 方式1：通过文本内容精准定位元素
                driver.execute_script("arguments[0].scrollIntoView(false);", driver.find_element(By.XPATH, '//p[contains(text(), "下载我们的应用")]')) 
                # 方式2：通过文本内容模糊定位元素
                # driver.find_element(By.XPATH, '//div[text()="下载我们的应用"]')  

                # 将滚动条调整至页面底部
                # driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(10)
        # 获取页面初始高度
        js = "return action=document.body.scrollHeight"
        height = driver.execute_script(js)
        # 获取页面元素量
        result = driver.find_elements(By.XPATH,ele)
        count= len(result)
        print("经过5次滚动，页面高度是{}，共{}个目标在页面。".format(height,count))

    from ast import Return

    def open_tab(self, driver, url2):
        # ---------------------------启动浏览器---------------
        # self.broswer.execute_script("window.open({url2}, 'new tab')")
        driver.execute_script("window.open(arguments[0])", url2)
        time.sleep(5)
        handles = driver.window_handles          #获取当前浏览器的所有窗口句柄
        driver.switch_to.window(handles[1])     #切换到第二个打开的窗口
        # self.broswer.switch_to.window(handles[-2])     #切换到倒数第二个打开的窗口
        # self.broswer.switch_to.window(handles[0])      #切换到最开始打开的窗口
        time.sleep(5)
    # Selenium加–headless无界面下无法抓取图片或者其他文件的解决
    def enable_download_in_headless_chrome(self, driver, download_dir):
        #add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        driver.execute("send_command", params)

    def swb_txt(self, driver, text):
        input_w=driver.find_element(By.XPATH,'.//textarea[@class="Form_input_2gtXx"]')
        input_w.send_keys(text)
        time.sleep(1)

    # 按发送
    def send(self,driver,elesd):
        sends = driver.find_element(By.XPATH,elesd)
        driver.execute_script("arguments[0].click();", sends)
        time.sleep(4)# 等待发送成功字样消失

    # # 删除图片
    def del_file(self,filepath):
        for root,dirs,files in os.walk(filepath):
            for file in files:
                os.remove(root+"\\"+file)


    # --------------------搜微博热搜后追踪---------------------------
    def selenium_chrome_test(self): 
        time.sleep(1)
        driver = self.broswer_initial('https://s.weibo.com/top/summary?cate=realtimehot')
        time.sleep(6)
        self.log_csdn(driver)
        time.sleep(5)
        driver.refresh()
        time.sleep(3)
        eles = driver.find_elements(By.XPATH,'//tbody//tr')
        jf = open("hot.json",'r',encoding = 'utf-8')
        diclists = json.load(jf)
        ln0 = len(eles)
        r0 = random.randint(1,2)
        # t0 = [random.randint(1,ln0) for n in range(r0)]#随机生成n个50以内的数
        t0 = [random.randint(1,ln0) for n in range(1)]
        for i,ele in enumerate(eles):
            if i not in t0:continue
            item_datas = ele.find_elements(By.XPATH,'./td')
            title = item_datas[1].text
            title = item_datas[1].find_element(By.XPATH,'./a').get_attribute('text')
            print(title)
            href = item_datas[1].find_element(By.XPATH,'./a').get_attribute('href')
            print(href)
            data = {"标题":title,"链接":href}
            if not any(d.get("标题",None) == title for d in diclists):#不存在KEY用这个
                diclists.append(data)
            time.sleep(2)
        jf.close()
        try:
            jfile = open("hot.json",'w+',encoding = 'utf-8')
                #即添加参数 ensure_ascii=False，它默认的是Ture
            json.dump(diclists,jfile,ensure_ascii=False,indent=4)
            jfile.close()       
        except:
            print("hot没有保存成功")
        time.sleep(2)
        driver.quit()

    def retweet_comment(self,v):
        time.sleep(5)
        driver = self.broswer_initial(v)
        time.sleep(6)
        self.log_csdn(driver)
        time.sleep(5)
        driver.refresh()
        time.sleep(3)
    
        self.roll_target(driver)
        time.sleep(10)
        # 点赞
        like = driver.find_elements(By.XPATH,'.//button[@class="woo-like-main toolbar_btn"]')
        driver.execute_script("arguments[0].click();", like[0])
        time.sleep(10)
        # 点击评论
        comment = driver.find_elements(By.XPATH,'.//i[@class="woo-font woo-font--comment toolbar_icon"]')
        time.sleep(10)
        driver.execute_script("arguments[0].click();", comment[0])
        time.sleep(10)
        # 找更多评论位置
        time.sleep(10)
        if driver.find_element(By.XPATH, './/div[@class="card-more-a"]') is not None:
            # 点击更多评论
            time.sleep(10)
            driver.find_element(By.XPATH, './/div[@class="card-more-a"]//a').click()
            time.sleep(2)
            if driver.find_element(By.XPATH, '//div[@class="item1in woo-box-flex"]') is not None:
                time.sleep(5)
            #下滚并获取目标数量100个评论最底端
                self.roll_bottom(driver, '//div[@class="item1in woo-box-flex"]',None)
                time.sleep(5)
                # 归集评论
                listcomment = []
                item_datas = driver.find_elements(By.XPATH,'.//div[@class="con1 woo-box-item-flex"]')
                time.sleep(5)
                ln = len(item_datas)
                t = [random.randint(1,ln) for n in range(3)]#随机生成三个ln以内的数
                for i, v in enumerate(item_datas): 
                    if i not in t:continue
                    item_data =v.find_element(By.XPATH,'.//div[@class="text"]//span').get_attribute('innerHTML')
                    time.sleep(5)
                    datas = re.findall('[\u4e00-\u9fa5]+', item_data)
                    for data in datas:
                        if data is None:continue
                        print(data)
                        listcomment.append(data)
                c = open("txt/comment.txt", 'w+', encoding = "utf-8")
                for l in listcomment:
                    c.write(l+',')
                c.close()
                z = open("txt/comment.txt", 'r', encoding = "utf-8")
                d = z.read()
                # 滑动到发送处
                # target = self.broswer.find_element(By.XPATH,'.//input[@class="woo-checkbox-input"]')
                # self.broswer.execute_script("arguments[0].scrollIntoView(true);", target)
                #发文
                if d == "":
                    time.sleep(1)
                    driver.find_element(By.XPATH,'.//textarea[@class="Form_input_3JT2Q"]').send_keys("转发微博")
                    time.sleep(5)
                else:
                    time.sleep(1)
                    driver.find_element(By.XPATH,'.//textarea[@class="Form_input_3JT2Q"]').send_keys(d)
                time.sleep(3)
                # 点击同时转发
                self.send(driver,'.//input[@class="woo-checkbox-input"]')
                #点评论
                self.send(driver,'.//button[@class="disabled woo-button-main woo-button-flat woo-button-primary woo-button-m woo-button-round Composer_btn_2XFOD"]')
                print("转发评论成功")
                z.close()
            else:
                print("有更多评论，但评论被禁止显示了 ")
        else:
            print("无法点击评论，可能没有更多评论或禁止点击更多评论")
            # s = driver.find_elements(By.XPATH,'.//dic[@class="input"]')
            # time.sleep(3)
            # s[1].send_keys("转发微博")
            # time.sleep(1)
            # # 点击同时转发
            # ztsz = driver.find_element(By.NAME,("forward"))
            # time.sleep(2)
            # driver.execute_script("arguments[0].click();", ztsz)
            # zzf = driver.find_element(By.XPATH,'.//a[@class="s-btn-a"]')
            # driver.execute_script("arguments[0].click();", zzf)
            # print("转发成功")
        driver.quit()

    def pic_list(self):
        time.sleep(1)
        urls = []
        piclist = []
        u = open('url.txt', "r", encoding='utf-8')
        for l in u.readlines():
            urls.append(l)
        u.close()
        classurl = random.choice(urls)
        print(classurl)
        time.sleep(2)
        broswer = self.broswer_initial(classurl)
        self.enable_download_in_headless_chrome(broswer, "images")
        self.roll_bottom(broswer, './/article', 'L')
        ids = [i for i in broswer.find_elements(By.XPATH,'.//article//a[@class="Link_link__mTUkz spacing_noMargin__Q_PsJ"]')]
        ln = len(ids)
        r = random.randint(2, 6)
        t = [random.randint(1,ln) for n in range(r)]#随机生成n个ln以内的数
        for i, v in enumerate(ids): 
            if i in t:
                id = v.get_attribute('href').split('/')[5]
                print(id)
            else:continue
            picurl= 'https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg?cs=srgb&amp'%(id,id)
            try:
                r = requests.get(picurl)
                r.status_code
                p = open('images/%s.jpeg'%id, "wb")
                p.write(r.content)
                print('%s保存成功'%id)
                piclist.append(r"%s/images/%s.jpeg"%(os.path.abspath(os.path.dirname(__file__)),id))
                p.close()
            except:print("图片链接失败")
        uu = open('txt/piclist.txt', "w+", encoding='utf-8')
        for x in piclist:
            uu.write(x+',')
        uu.close()
        time.sleep(2)
        broswer.quit()

    def ji_tang(self):
        time.sleep(1)
        broswer = self.broswer_initial('https://weibo.com/login.php')
        time.sleep(6)
        self.log_csdn(broswer)
        time.sleep(5)
        broswer.refresh()
        time.sleep(3)
    #     fwb = self.broswer.find_element(By.XPATH,'.//button[@class="Pub_wrap_2V6Wk Nav_pub_QrDht"]')
    #     self.broswer.execute_script("arguments[0].click();", fwb)
        txt = []
        img_path_list = []
        time.sleep(2)
        jz = open("txt/jt.txt", 'r', encoding = "gbk", errors = "ignore")
        jt = open("txt/jts.txt", 'w+', encoding = "gbk", errors = "ignore")
        for t in jz.readlines():
            txt.append(t)
        text = random.choice(txt)
        jt.write(text)
        jt.close()
        jz.close()
        time.sleep(3)
        jts = open("txt/jts.txt", 'r', encoding='gbk', errors = 'ignore')
        tx = jts.readline().strip()
        piclist = open('txt/piclist.txt', "r", encoding='utf-8')
        for p in piclist.readline().strip().split(','):
            if p != "":
                img_path_list.append(p)
        time.sleep(2)
        count_img = len(img_path_list)
        # 上传内容
        if count_img==0:# 没有图片
            self.swb_txt(broswer,tx)
        elif count_img==1:# 单张图片
            self.swb_txt(broswer,tx)
            el = broswer.find_element(By.XPATH,'.//input[@class="FileUpload_file_27ilM"]')
            file = img_path_list[0]
            el.send_keys(file)
            time.sleep(30)
        else:# 多张图片
            self.swb_txt(broswer,tx)
            for i in range(len(img_path_list)):
                el = broswer.find_element(By.XPATH,'.//input[@class="FileUpload_file_27ilM"]')
                file = img_path_list[i]
                el.send_keys(file)
                time.sleep(30)
        # 按发布按钮
        time.sleep(30)
        self.send(broswer,'.//button[@class="woo-button-main woo-button-flat woo-button-primary woo-button-m woo-button-round Tool_btn_2Eane"]')
        time.sleep(3)
        piclist.close()
        jts.close()
        # 删除下载的所有图片
        for root,dirs,files in os.walk("%s\\wb\\images"%(os.path.abspath(os.path.dirname(__file__)))):
            for file in files:
                os.remove(root+"\\"+file)
        broswer.quit()
               
    def zhuan_fa(self):
        with open('hot.json', 'r', encoding='utf-8') as f2:
            info_res = json.load(f2)
        with open("hotRetweeted.json",'r',encoding = 'utf-8') as f3:
            hotReDics = json.load(f3)
        for info_re in info_res:
            for value in info_re.values():
                if ("https://" not in value):
                    continue
                if not any(d.get("链接",None) == value for d in hotReDics):#如有不相同的网址，value则执行
                    # self.open_tab(value)
                    self.retweet_comment(value)
                    time.sleep(random.uniform(1,6))


    def json_save(self):
        f2 = open('hot.json', 'r', encoding='utf-8') 
        info_res = json.load(f2)
        f3 = open("hotRetweeted.json",'r',encoding = 'utf-8')
        hotReDics = json.load(f3)
        for info_re in info_res:
            for value in info_re.values():
                if ("https://" not in value):
                    continue
                if not any(d.get("链接",None) == value for d in hotReDics):#如有不相同的网址，value则执行
                    a = info_re['标题']
                    b = info_re['链接']
                    hotRetweetdata = {"标题":a,"链接":b}
                    hotReDics.append(hotRetweetdata)
        try:
            with open("hotRetweeted.json",'w+',encoding = 'utf-8') as jfile:
                #即添加参数 ensure_ascii=False，它默认的是Ture
                json.dump(hotReDics,jfile,ensure_ascii=False,indent=4)       
        except:
            print("更新HOT失败")

    def restore_json(self):
        with open('hot0.json', "r", encoding='utf-8') as j:
            d =j.read()
        with open('hot.json', "w+", encoding='utf-8') as s:
            s.write(d)

        with open('hotRetweeted0.json', "r", encoding='utf-8') as o:
            f = o.read()
        with open('hotRetweeted.json', "w+", encoding='utf-8') as n:
            n.write(f)