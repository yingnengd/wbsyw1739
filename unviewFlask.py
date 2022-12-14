# -- coding: utf-8 --**

from WebDriverWb import WebDriver
from flask import Flask
import time
import random
import traceback2 as traceback
import os

from flask_apscheduler import APScheduler
      
# if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    
m = random.randint(1,3)
s = random.randint(1,20)
mm = random.randint(56,59)

class Config(object):  # 创建配置，用类
    JOBS = [  # 任务列表
        {  # 任务字典（细节）
            'id': 'index',
            'func': '__main__:index',
            # 'args': (1, 2),
            'trigger': 'cron',
            'timezone':"Asia/Shanghai",
            'day_of_week':'mon-sat',
            'hour':'5-23',
            'minute':'{}'.format(m),
            'second':'{}'.format(s)
            #'second':'5'
        },
        {  # 第二个任务字典
            'id': 'job1',
            'func': '__main__:job1',
            # 'args': (3, 4),#这是要输入函数的变量
            'trigger': 'cron',
            'timezone':"Asia/Shanghai",
            'day_of_week':'mon-sat', 
            'hour':'5-23',
            'minute':'{}'.format(mm)
            # 'day':'1'
            # 'second':'59'
        }
    ]

driver= WebDriver()#实例化（）不应在其他函数里，实例化后的实例driver应用在其他函数里

def job1():
    # path = r"%s/hotRetweeted.json"%(os.path.abspath(os.path.dirname(__file__)))
    # size = os.path.getsize(path)
    # if (size/1024 > 50):
    driver.restore_json()        

app = Flask(__name__)  # 实例化flask
app.config.from_object(Config())  # 为实例化的flask引入配置

@app.route('/')  # 首页路由
def index():  # 首页视图函数，就返回个hello
    # r0 = random.randint(2,4)
    # for i in range(r0):
    try:
        driver.selenium_chrome_test()
        time.sleep(random.uniform(1,3))
        driver.zhuan_fa()
        time.sleep(random.uniform(1,3))
    except Exception as e:
        print(e.args)
        print('======')
        print(traceback.format_exc())
    driver.json_save()
    time.sleep(random.uniform(1,3))
    driver.pic_list()
    time.sleep(random.uniform(1,3))
    driver.ji_tang()
    time.sleep(random.uniform(2,3))

if __name__ == '__main__':
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表
    app.run(host='0.0.0.0', port=8080)  # 启动flask