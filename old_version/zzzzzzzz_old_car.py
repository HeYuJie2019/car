import RPi.GPIO as GPIO
import time
import pigpio
import numpy as np
import cv2
from cv2 import COLOR_BGR2GRAY
import serial
from pyzbar.pyzbar import decode
s=serial.Serial("/dev/ttyAMA0", 9600, timeout=0.1) #设置串口
qrCodeDetector = cv2.QRCodeDetector() #设置扫码
# GPIO.setmode(GPIO.BCM)              #select model
pi = pigpio.pi()
# TRIG = 17   out
# ECHO = 27   in
JG = 17  #in
JGZ = 18
JGY = 27
PWMA = 13
AIN2 = 19
AIN1 = 26
BIN1 = 16
BIN2 = 20
PWMB = 21
PWMC = 12
CIN1 = 5
CIN2 = 6
DIN1 = 25
DIN2 = 24
PWMD = 23
# E1A = 5
# E2A = 6
Speed_A = 32
Speed_B = 31
Speed_C = 45
Speed_D = 45
num = 0
flag = 1
step = 1
y = {}
data = []
#动作组
data0 = bytes.fromhex('FF 09 00 00 00')
data1 = bytes.fromhex('FF 09 00 01 00')
data2 = bytes.fromhex('FF 09 00 02 00')
data3 = bytes.fromhex('FF 09 00 03 00')
data4 = bytes.fromhex('FF 09 00 04 00')
data5 = bytes.fromhex('FF 09 00 05 00')
data6 = bytes.fromhex('FF 09 00 06 00')
data7 = bytes.fromhex('FF 09 00 07 00')
data8 = bytes.fromhex('FF 09 00 08 00')
data9 = bytes.fromhex('FF 09 00 09 00')
data10 = bytes.fromhex('FF 09 00 0a 00')
data11 = bytes.fromhex('FF 09 00 0b 00')
data12 = bytes.fromhex('FF 09 00 0c 00')
data13 = bytes.fromhex('FF 09 00 0d 00')
data14 = bytes.fromhex('FF 09 00 0e 00')
data15 = bytes.fromhex('FF 09 00 0f 00')
################################################################
def pin_init():
    GPIO.setmode(GPIO.BCM)              #select model
    GPIO_out_list = (PWMA,AIN1,AIN2,BIN1,BIN2,PWMB,PWMC,CIN1,CIN2,DIN1,DIN2,PWMD) #select pin
    GPIO_in_list = (JG,JGZ,JGY)
    GPIO.setup(GPIO_in_list, GPIO.IN)
    GPIO.setup(GPIO_out_list, GPIO.OUT) #set pin's model
    pwm_init(PWMA, 9000, 40000)
    pwm_init(PWMB, 9000, 40000)
    pwm_init(PWMC, 9000, 40000)
    pwm_init(PWMD, 9000, 40000)
################################################################
def pwm_init(pin, frequency, totol):
    pi.set_PWM_frequency(pin, frequency)#设定pin号引脚产生的pwm波形的频率为frequency
    pi.set_PWM_range(pin, totol) #指定要把14号引脚上的一个pwm周期分成多少份，这里是分成2000份，这个数据的范围是25-40000
    return totol
################################################################
def speed(pin, n):
    totol = pwm_init(pin, 5000, 10000)
    num = 10000*n*0.01     #占空比 0~100
    pi.set_PWM_dutycycle(pin, num)
    return 0
################################################################
# def OpenReadSpeed(pin1,pin2):        #开始计数脉冲数
#     GPIO.setup(pin1, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #通过18号引脚读取左轮脉冲数据
#     GPIO.setup(pin2, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #通过35号引脚读取右轮脉冲数据
#     global counter                 #设置为全局变量
#     global counter1
#     counter = 0      #左轮脉冲初值
#     counter1 = 0     #右轮脉冲初值
#     def my_callback(channel):          #边缘检测回调函数，详情在参见链接中
#         global counter
#         if GPIO.event_detected(pin1):        #检测到一个脉冲则脉冲数加1
#             counter=counter+1
#     def my_callback1(channel1):            #这里的channel和channel1无须赋确定值，但笔者测试过，不能不写
#         global counter1
#         if GPIO.event_detected(pin2):
#             counter1=counter1+1
#     GPIO.add_event_detect(pin1,GPIO.RISING,callback=my_callback) #在引脚上添加上升临界值检测再回调
#     GPIO.add_event_detect(pin2,GPIO.RISING,callback=my_callback1)
################################################################
# def ReadSpeed(pin):
#     global counter1
#     global counter
#     if pin == E1A:
#         counter = 0
#         c1 = counter
#         time.sleep(0.04)
#         c2 = counter
#         return c2-c1
#     if pin == E2A:
#         counter1 = 0
#         c1 = counter1
#         time.sleep(0.04)
#         c2 = counter1
#         return c2-c1
# def ReadSpeedList(pin):
#     SpeedList = []
#     for i in range(5):
#         SpeedList.append(ReadSpeed(pin))
#     return SpeedList
# def crs(pin):
#     return np.average(ReadSpeedList(pin))*25    #返回一秒几个脉冲
################################################################
def move(direction):
    global Speed_A
    global Speed_B
    if direction == 'front':
        GPIO.output(AIN1,1)
        GPIO.output(AIN2,0)
        GPIO.output(BIN1,1)
        GPIO.output(BIN2,0)
        GPIO.output(CIN1,0)
        GPIO.output(CIN2,1)
        GPIO.output(DIN1,0)
        GPIO.output(DIN2,1)
        #a wheel
        # if crs(E1A) < A_F_speed - ErrorSpeed:
        #     Speed_A += 0.5
        #     speed(PWMA, Speed_A)
        # elif crs(E1A) > A_F_speed + ErrorSpeed:
        #     Speed_A -= 0.5
        #     speed(PWMA, Speed_A)
        # #b wheel
        # if crs(E2A) < B_F_speed - ErrorSpeed:
        #     Speed_B += 0.5
        #     speed(PWMB, Speed_B)
        # elif crs(E2A) > B_F_speed + ErrorSpeed:
        #     Speed_B -= 0.5
        #     speed(PWMB, Speed_B)
    if direction == 'back' :
        GPIO.output(AIN1,0)
        GPIO.output(AIN2,1)
        GPIO.output(BIN1,0)
        GPIO.output(BIN2,1)
        GPIO.output(CIN1,1)
        GPIO.output(CIN2,0)
        GPIO.output(DIN1,1)
        GPIO.output(DIN2,0)
    if direction == 'xie':
        GPIO.output(AIN1,0)
        GPIO.output(AIN2,1)
        GPIO.output(BIN1,1)
        GPIO.output(BIN2,0)
        GPIO.output(CIN1,1)
        GPIO.output(CIN2,0)
        GPIO.output(DIN1,0)
        GPIO.output(DIN2,1)
    if direction == 'stop':
        speed(PWMA,0)
        speed(PWMB,0)
        speed(PWMC,0)
        speed(PWMD,0)
    if direction == 'xuanzhuanzuo':
        GPIO.output(AIN1,1)
        GPIO.output(AIN2,0)
        GPIO.output(BIN1,0)
        GPIO.output(BIN2,1)
        GPIO.output(CIN1,1)
        GPIO.output(CIN2,0)
        GPIO.output(DIN1,0)
        GPIO.output(DIN2,1)
    if direction == 'xuanzhuanyou':
        GPIO.output(AIN1,0)
        GPIO.output(AIN2,1)
        GPIO.output(BIN1,1)
        GPIO.output(BIN2,0)
        GPIO.output(CIN1,0)
        GPIO.output(CIN2,1)
        GPIO.output(DIN1,1)
        GPIO.output(DIN2,0)
################################################################
def cal_dis(pin1, pin2):
    distance = 0
    GPIO.output(pin1, 1)
    time.sleep(0.00001)
    GPIO.output(pin1, 0)
    i = 0
    while GPIO.input(pin2) == 0:
        i += 1
        if i == 10000:    #防止超时卡死
            return 0
    t1 = time.time()
    while GPIO.input(pin2) == 1:
        i += 1
        if i == 20000:    #防止超时卡死
            return 0
    t2 = time.time()
    distance = (t2-t1)*34000/2
    return distance
def temp(pin1, pin2):
    ds = []
    for i in range(6):
        ds.append(round(cal_dis(pin1, pin2),1))
        time.sleep(0.01)
    # print(ds)
    return ds
def dstc(pin1, pin2):
    list = temp(pin1, pin2)
    if np.average(list) < 50:          #排除错误数值
        check = 10.0
    elif 50 < np.average(list) < 100:
        check = 10.0
    elif 100 < np.average(list) < 150:
        check = 4.5
    elif 150 < np.average(list) < 200:
        check = 7.0
    elif 200 < np.average(list) < 250:
        check = 8.5
    else:
        check = 8.0
    standard = 0
    for i in range(len(list)):
        flag = 0          
        a = list[i]
        for j in range(i+1, len(list)):
            b = list[j]
            if abs(a -b) < check:  #判断差值
                flag += 1
        if flag > len(list)/2:
            standard = a
            break
    if standard == 0:
        return 0
    new_list = []
    for i in list:
        if abs(standard - i) < check:
            new_list.append(i)
    # print(new_list)
    distance = np.average(new_list)
    return distance
#*********************************
def judge(img):
    num = 0
    w, h = img.shape
    for i in range(w):
        for j in range(h):
            if img[i,j]==0:
                num += 1
                if num >= 200:
                    return True
    return False
def Judge(img):
    you = zuo = zhong = 0
    if judge(img[160:180,310:330]) == True:  #x
        zhong = 1
    if judge(img[160:180,260:280]) == True:  #nx_1
        zuo += 1
    if judge(img[160:180,360:380]) == True:  #px_1
        you += 1
    if judge(img[160:180,210:230]) == True:  #nx_2
        zuo += 1
    if judge(img[160:180,410:430]) == True:  #px_2    
        you += 1
    if judge(img[160:180,160:180]) == True:  #nx_3
        zuo += 1
    if judge(img[160:180,460:480]) == True:  #px_3
        you += 1
    if judge(img[160:180,110:130]) == True:  #nx_4
        zuo += 1
    if judge(img[160:180,510:530]) == True:  #px_4
        you += 1
    if judge(img[160:180,60:80]) == True:  #nx_5
        if judge(img[160:180,160:180]) == True:
            zuo += 2
        else:
            zuo += 4
    if judge(img[160:180,560:580]) == True:  #px_5
        if judge(img[160:180,460:480]) == True:
            you += 2
        else:
            you += 4
    if judge(img[160:180,10:30]) == True:  #nx_6
        if judge(img[160:180,110:130]) == True:
            zuo += 3
        elif judge(img[160:180,60:80]) == True:
            zuo += 5
        else:
            zuo += 10
    if judge(img[160:180,610:630]) == True:  #px_6
        if judge(img[160:180,510:530]) == True:
            you += 3
        elif judge(img[160:180,560:580]) == True:
            you += 5
        else:
            you += 10
    return you-zuo
def xunji2(frame):
    if -2 < Judge(frame) < 2:
        speed(PWMA,33)  #33
        speed(PWMB,31)  #31
        speed(PWMC,35)  #35
        speed(PWMD,36)  #36
    elif 2 <= Judge(frame) < 5:
        speed(PWMA,33)  #33
        speed(PWMB,34)  #31
        speed(PWMC,35)  #35
        speed(PWMD,36)  #36
    elif -5 < Judge(frame) <= -2:
        speed(PWMA,34)  #33
        speed(PWMB,31)  #31
        speed(PWMC,35)  #35
        speed(PWMD,36)  #36
    elif 5 <= Judge(frame) < 8:
        speed(PWMA,33)  #33
        speed(PWMB,39)  #31
        speed(PWMC,35)  #35
        speed(PWMD,36)  #36
    elif -8 < Judge(frame) <= -5:
        speed(PWMA,34)  #33
        speed(PWMB,31)  #31
        speed(PWMC,35)  #35
        speed(PWMD,36)  #36
    elif Judge(frame) >= 8:
        speed(PWMA,33)  #33
        speed(PWMB,42)  #31
        speed(PWMC,35)  #35
        speed(PWMD,36)  #36
    elif Judge(frame) <= -8:
        speed(PWMA,35)  #33
        speed(PWMB,31)  #31
        speed(PWMC,35)  #35
        speed(PWMD,36)  #36
def xunji1(frame):
    A = Speed_A  #33
    B = Speed_B  #31
    C = Speed_C  #35
    D = Speed_D  #36
    if Judge(frame) > 3:
        B = Speed_B + Judge(frame)*0.5
    elif Judge(frame) < -3:
        A = Speed_A - Judge(frame)*0.5
    elif Judge(frame) == 0:
        A = Speed_A
        B = Speed_B 
    print('A:',A,' B:',B)
    speed(PWMA,A)
    speed(PWMB,B)
    speed(PWMC,C)
    speed(PWMD,D)
def shuxian():
    global num
    global flag
    if GPIO.input(JG) == 1 and flag == 1:
        num += 1
        flag = 0
    elif GPIO.input(JG) == 0:
        flag = 1
#快速
def xunji3():
    move('front')
    if GPIO.input(JGZ) == 1 and GPIO.input(JGY) == 1:
        speed(PWMA,60)  #60
        speed(PWMB,59.5)#59.5
        speed(PWMC,80)  #80
        speed(PWMD,80)  #80
    elif GPIO.input(JGZ) == 0 and GPIO.input(JGY) == 1:
        speed(PWMA,30)  #60
        speed(PWMB,59.5)#59.5
        speed(PWMC,80)  #80
        speed(PWMD,60)  #80
    elif GPIO.input(JGZ) == 1 and GPIO.input(JGY) == 0:
        speed(PWMA,60)  #60
        speed(PWMB,29.5)#59.5
        speed(PWMC,60)  #80
        speed(PWMD,80)  #80
    elif GPIO.input(JGZ) == 0 and GPIO.input(JGY) == 0:
        speed(PWMA,0)  #60
        speed(PWMB,0)  #59.5
        speed(PWMC,0)  #80
        speed(PWMD,0)  #80
#慢速
def xunji4():
    move('front')
    if GPIO.input(JGZ) == 1 and GPIO.input(JGY) == 1:
        speed(PWMA,22)  #33
        speed(PWMB,20)  #31
        speed(PWMC,40)  #35
        speed(PWMD,40)  #36
    elif GPIO.input(JGZ) == 0 and GPIO.input(JGY) == 1:
        speed(PWMA,10)  #33
        speed(PWMB,20)  #31
        speed(PWMC,40)  #35
        speed(PWMD,40)  #36
    elif GPIO.input(JGZ) == 1 and GPIO.input(JGY) == 0:
        speed(PWMA,22)  #33
        speed(PWMB,10)  #31
        speed(PWMC,40)  #35
        speed(PWMD,40)  #36
    elif GPIO.input(JGZ) == 0 and GPIO.input(JGY) == 0:
        speed(PWMA,0)  #33
        speed(PWMB,0)  #31
        speed(PWMC,0)  #35
        speed(PWMD,0)  #36
#中速
def xunji5():
    move('front')
    if GPIO.input(JGZ) == 1 and GPIO.input(JGY) == 1:
        speed(PWMA,33)  #33
        speed(PWMB,30)  #30
        speed(PWMC,50)  #50
        speed(PWMD,50)  #50
    elif GPIO.input(JGZ) == 0 and GPIO.input(JGY) == 1:
        speed(PWMA,15)  #33
        speed(PWMB,30)  #30
        speed(PWMC,50)  #50
        speed(PWMD,35)  #50
    elif GPIO.input(JGZ) == 1 and GPIO.input(JGY) == 0:
        speed(PWMA,33)  #33
        speed(PWMB,15)  #30
        speed(PWMC,35)  #50
        speed(PWMD,50)  #50
    elif GPIO.input(JGZ) == 0 and GPIO.input(JGY) == 0:
        speed(PWMA,0)  #33
        speed(PWMB,0)  #31
        speed(PWMC,0)  #35
        speed(PWMD,0)  #36
#######################################################
#扫码
def get_qr_data(input_frame):
    global data
    data = []
    try:
        ys, bbox, straight_qrcode = qrCodeDetector.detectAndDecode(input_frame)
        if ys[0] == '蓝':
            data.append('b')
        elif ys[0] == '绿':
            data.append('g')
        elif ys[0] == '红':
            data.append('r')
        if ys[2] == '蓝':
            data.append('b')
        elif ys[2] == '绿':
            data.append('g')
        elif ys[2] == '红':
            data.append('r')
    except:
        return data
#######################################################
#颜色识别
def color_recognize(img):
    b = np.average(img[:,:,0])
    g = np.average(img[:,:,1])
    r = np.average(img[:,:,2])
    if b > g and b > r:
        return 'b'
    elif g > b and g > r:
        return 'g'
    elif r > b and r > g:
        return 'r'
def yssb(img):
    global y
    y = {}
    x1 = img[110:180, 90:160]
    x2 = img[140:250, 260:370]
    x3 = img[220:340, 510:630]
    y['c'] = color_recognize(x1)
    y['b'] = color_recognize(x2)
    y['a'] = color_recognize(x3)
#######################################################
#试写行走函数
def position(CurPosiX, CurPosiY, CurDir, TgtPosiX, TgtPosiY, TgtDir):
    global num, first, flag
    if TgtDir == 'y+':
        if CurPosiX == TgtPosiX:
            num = 0
            first = 1
            st = 1
            while 1:
                if TgtPosiY > CurPosiY:
                    if st == 1:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 2
                    if st == 2:
                        xunji5()
                        time.sleep(0.3)
                        st = 3
                    if st == 3:
                        shuxian()
                        xunji3()
                        if num == abs(TgtPosiY - CurPosiY) - 1:
                            st = 4
                    if st == 4:
                        shuxian()
                        xunji4()
                        if num == abs(TgtPosiY - CurPosiY):
                            move('stop')
                            break
                if TgtPosiY < CurPosiY:
                    if st == 1:
                        move('xuanzhuanyou')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 2
                    if st == 2:
                        xunji5()
                        time.sleep(0.3)
                        st = 3
                    if st == 3:
                        shuxian()
                        xunji3()
                        if num == abs(CurPosiY - TgtPosiY) - 1:
                            st = 4
                    if st == 4:
                        shuxian()
                        xunji4()
                        if num == abs(CurPosiY - TgtPosiY):
                            move('stop')
                            st = 5
                    if st == 5:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 6
                    if st == 6:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            break      
        elif CurPosiY == TgtPosiY:
            if TgtPosiX > CurPosiX:
                position(CurPosiX, CurPosiY, 'x+', TgtPosiX ,TgtPosiY, 'x+')
                first = 1
                while 1:
                    move('xuanzhuanzuo')
                    speed(PWMA,50)
                    speed(PWMB,50)
                    speed(PWMC,50)
                    speed(PWMD,50)
                    if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                        first = 0
                    if GPIO.input(JGZ) == 1 and first == 0:
                        move('stop')
                        first = 1
                        break
            elif TgtPosiX < CurPosiX:
                st = 1
                num = 0
                first = 1
                while 1:
                    if st == 1:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 2
                    if st == 2:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 3
                    if st == 3:
                        xunji5()
                        time.sleep(0.3)
                        st = 4
                    if st == 4:
                        shuxian()
                        xunji3()
                        if num == abs(CurPosiX - TgtPosiX) - 1:
                            st = 5
                    if st == 5:
                        shuxian()
                        xunji4()
                        if num == abs(CurPosiX - TgtPosiX):
                            move('stop')
                            st = 6
                    if st == 6:
                        move('xuanzhuanyou')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            num = 0
                            first = 1
                            break
        else:
            if TgtPosiY > CurPosiY:
                if TgtPosiX > CurPosiX:
                    position(CurPosiX, 0, 'x+', TgtPosiX, 0, 'x+')
                    position(0, CurPosiY, 'x+', 0, TgtPosiY, 'y+')
                elif TgtPosiX < CurPosiX:
                    position(0, CurPosiY, 'x+', 0, TgtPosiY, 'y+')
                    position(0, 0, 'x+', 0, CurPosiX-TgtPosiX, 'x+')
            elif TgtPosiY < CurPosiY:
                if TgtPosiX > CurPosiX:
                    position(0, 0, 'x+', 0, TgtPosiY-CurPosiY, 'x+')
                    position(CurPosiX, 0, 'x+', TgtPosiX, 0, 'y+')
                elif TgtPosiX < CurPosiX:
                    position(0, 0, 'x+', 0, TgtPosiY-CurPosiY, 'x-')
                    position(0, 0, 'x+', CurPosiX-TgtPosiX, 0, 'y-')
    elif TgtDir == 'y-':
        if CurPosiX == TgtPosiX:
            num = 0
            first = 1
            st = 1
            while 1:
                if TgtPosiY > CurPosiY:
                    if st == 1:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 2
                    if st == 2:
                        xunji5()
                        time.sleep(0.3)
                        st = 3
                    if st == 3:
                        shuxian()
                        xunji3()
                        if num == abs(TgtPosiY - CurPosiY) - 1:
                            st = 4
                    if st == 4:
                        shuxian()
                        xunji4()
                        if num == abs(TgtPosiY - CurPosiY):
                            move('stop')
                            st = 5
                    if st == 5:
                        move('xuanzhuanyou')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 6
                    if st == 6:
                        move('xuanzhuanyou')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            first = 1
                            break
                if TgtPosiY < CurPosiY:
                    if st == 1:
                        move('xuanzhuanyou')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 2
                    if st == 2:
                        xunji5()
                        time.sleep(0.3)
                        st = 3
                    if st == 3:
                        shuxian()
                        xunji3()
                        if num == abs(CurPosiY - TgtPosiY) - 1:
                            st = 4
                    if st == 4:
                        shuxian()
                        xunji4()
                        if num == abs(CurPosiY - TgtPosiY):
                            move('stop')
                            break      
        elif CurPosiY == TgtPosiY:
            if TgtPosiX > CurPosiX:
                position(CurPosiX, CurPosiY, 'x+', TgtPosiX ,CurPosiY, 'x+')
                first = 1
                while 1:
                    move('xuanzhuanyou')
                    speed(PWMA,50)
                    speed(PWMB,50)
                    speed(PWMC,50)
                    speed(PWMD,50)
                    if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                        first = 0
                    if GPIO.input(JGY) == 1 and first == 0:
                        move('stop')
                        first = 1
                        break
            elif TgtPosiX < CurPosiX:
                st = 1
                num = 0
                first = 1
                while 1:
                    if st == 1:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 2
                    if st == 2:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 3
                    if st == 3:
                        xunji5()
                        time.sleep(0.3)
                        st = 4
                    if st == 4:
                        shuxian()
                        xunji3()
                        if num == abs(CurPosiX - TgtPosiX) - 1:
                            st = 5
                    if st == 5:
                        shuxian()
                        xunji4()
                        if num == abs(CurPosiX - TgtPosiX):
                            move('stop')
                            st = 6
                    if st == 6:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            num = 0
                            first = 1
                            break
        else:
            if TgtPosiY > CurPosiY:
                if TgtPosiX > CurPosiX:
                    position(0, CurPosiY, 'x+', 0, TgtPosiY, 'x+')
                    position(CurPosiX, 0, 'x+', TgtPosiX, 0, 'y-')
                elif TgtPosiX < CurPosiX:
                    position(0, 0, 'x+', 0, TgtPosiY-CurPosiY, 'x-')
                    position(0, 0, 'x+', CurPosiX-TgtPosiX, 0, 'y+')
            elif TgtPosiY < CurPosiY:
                if TgtPosiX > CurPosiX:
                    position(0, CurPosiY, 'x+', 0, TgtPosiY, 'x+')
                    position(CurPosiX, 0, 'x+', TgtPosiX, 0, 'y-')
                elif TgtPosiX < CurPosiX:
                    position(0, 0, 'x+', 0, TgtPosiY-CurPosiY, 'x-')
                    position(0, 0, 'x+', CurPosiX-TgtPosiX, 0, 'y+')
    elif TgtDir == 'x+':
        if CurPosiY == TgtPosiY:
            num = 0
            first = 1
            st = 1
            while 1:
                if TgtPosiX > CurPosiX:
                    if st == 1:
                        xunji5()
                        time.sleep(0.3)
                        st = 2
                    if st == 2:
                        shuxian()
                        xunji3()
                        if num == abs(TgtPosiX - CurPosiX) - 1:
                            st = 3
                    if st == 3:
                        shuxian()
                        xunji4()
                        if num == abs(TgtPosiX - CurPosiX):
                            move('stop')
                            break
                elif TgtPosiX < CurPosiX:
                    if st == 1:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 2
                    if st == 2:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 3
                    if st == 3:
                        xunji5()
                        time.sleep(0.3)
                        st = 4
                    if st == 4:
                        shuxian()
                        xunji3()
                        if num == abs(CurPosiX - TgtPosiX) - 1:
                            st = 5
                    if st == 5:
                        shuxian()
                        xunji4()
                        if num == abs(CurPosiX - TgtPosiX):
                            move('stop')
                            st = 6
                    if st == 6:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 7
                    if st == 7:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            break
        elif CurPosiX == TgtPosiX:
            st = 1
            first = 1
            num = 0
            while 1:
                if TgtPosiY > CurPosiY:
                    if st == 1:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            num = 0
                            first = 1
                            st = 2
                    if st == 2:
                        xunji5()
                        time.sleep(0.3)
                        st = 3
                    if st == 3:
                        shuxian()
                        xunji3()
                        if num == abs(TgtPosiY - CurPosiY) - 1:
                            st = 4
                    if st == 4:
                        shuxian()
                        xunji4()
                        if num == abs(TgtPosiY - CurPosiY):
                            move('stop')
                            st = 5
                    if st == 5:
                        move('xuanzhuanyou')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            num = 0
                            first = 1
                            break
                elif TgtPosiY < CurPosiY:
                    if st == 1:
                        move('xuanzhuanyou')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            num = 0
                            first = 1
                            st = 2
                    if st == 2:
                        xunji5()
                        time.sleep(0.3)
                        st = 3
                    if st == 3:
                        shuxian()
                        xunji3()
                        if num == abs(CurPosiY - TgtPosiY) - 1:
                            st = 4
                    if st == 4:
                        shuxian()
                        xunji4()
                        if num == abs(CurPosiY - TgtPosiY):
                            move('stop')
                            st = 5
                    if st == 5:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            num = 0
                            first = 1
                            break
        else:
            if TgtPosiY > CurPosiY:
                if TgtPosiX > CurPosiX:
                    position(0, CurPosiY, 'x+', 0, TgtPosiY, 'x+')
                    position(CurPosiX, 0, 'x+', TgtPosiX, 0, 'x+')
                elif TgtPosiX < CurPosiX:
                    position(0, 0, 'x+', TgtPosiX-CurPosiX, 0, 'y+')
                    position(0, 0, 'x+', TgtPosiY-CurPosiY, 0, 'y-')
            elif TgtPosiY < CurPosiY:
                if TgtPosiX > CurPosiX:
                    position(0, 0, 'x+', 0, TgtPosiY-CurPosiY, 'x+')
                    position(CurPosiX, 0, 'x+', TgtPosiX, 0, 'x+')
                elif TgtPosiX < CurPosiX:
                    position(0, CurPosiY, 'x+', 0, TgtPosiY, 'x-')
                    position(0, 0, 'x+', CurPosiX-TgtPosiX, 0, 'x-')
    elif TgtDir == 'x-':
        if CurPosiY == TgtPosiY:
            st = 1
            first = 1
            num = 0
            while 1:
                if TgtPosiX < CurPosiX:
                    if st == 1:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            num = 0
                            first = 1
                            st = 2
                    if st == 2:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            num = 0
                            first = 1
                            st = 3
                    if st == 3:
                        xunji5()
                        time.sleep(0.3)
                        st = 4
                    if st == 4:
                        shuxian()
                        xunji3()
                        if num == abs(CurPosiX - TgtPosiX) - 1:
                            st = 5
                    if st == 5:
                        shuxian()
                        xunji4()
                        if num == abs(CurPosiX - TgtPosiX):
                            move('stop')
                            break
                if TgtPosiX > CurPosiX:
                    if st == 1:
                        xunji5()
                        time.sleep(0.3)
                        st = 2
                    if st == 2:
                        shuxian()
                        xunji3()
                        if num == abs(TgtPosiX - CurPosiX) - 1:
                            st = 3
                    if st == 3:
                        shuxian()
                        xunji4()
                        if num == abs(TgtPosiX - CurPosiX):
                            move('stop')
                            num = 0
                            st = 4
                    if st == 4:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 5
                    if st == 5:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            break
        elif CurPosiX == TgtPosiX:
            st = 1
            first = 1
            num = 0
            while 1:
                if TgtPosiY > CurPosiY:
                    if st == 1:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 2
                    if st == 2:
                        xunji5()
                        time.sleep(0.3)
                        st = 3
                    if st == 3:
                        shuxian()
                        xunji3()
                        if num == abs(TgtPosiY - CurPosiY) - 1:
                            st = 4
                    if st == 4:
                        shuxian()
                        xunji4()
                        if num == abs(TgtPosiY - CurPosiY):
                            move('stop')
                            num = 0
                            st = 5
                    if st == 5:
                        move('xuanzhuanzuo')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGZ) == 1 and first == 0:
                            move('stop')
                            first = 1
                            break
                elif TgtPosiY < CurPosiY:
                    if st == 1:
                        move('xuanzhuanyou')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            first = 1
                            st = 2
                    if st == 2:
                        xunji5()
                        time.sleep(0.3)
                        st = 3
                    if st == 3:
                        shuxian()
                        xunji3()
                        if num == abs(CurPosiY - TgtPosiY) - 1:
                            st = 4
                    if st == 4:
                        shuxian()
                        xunji4()
                        if num == abs(CurPosiY - TgtPosiY):
                            move('stop')
                            num = 0
                            st = 5
                    if st == 5:
                        move('xuanzhuanyou')
                        speed(PWMA,50)
                        speed(PWMB,50)
                        speed(PWMC,50)
                        speed(PWMD,50)
                        if GPIO.input(JGY) == 0 and GPIO.input(JGZ) == 0:
                            first = 0
                        if GPIO.input(JGY) == 1 and first == 0:
                            move('stop')
                            first = 1
                            break
        else:
            if TgtPosiY > CurPosiY:
                if TgtPosiX > CurPosiX:
                    position(CurPosiX, 0, 'x+', TgtPosiX, 0, 'y+')
                    position(CurPosiY, 0, 'X+', TgtPosiY, 0, 'y+')
                elif TgtPosiX < CurPosiX:
                    position(0, CurPosiY, 'x+', 0, TgtPosiY, 'y+')
                    position(0, 0, 'x+', 0, CurPosiX-TgtPosiX, 'y+')
            elif TgtPosiY < CurPosiY:
                if TgtPosiX > CurPosiX:
                    position(CurPosiX, 0, 'x+', TgtPosiX, 0, 'y-')
                    position(0, 0, 'x+', CurPosiY-TgtPosiY, 0, 'y-')
                elif TgtPosiX < CurPosiX:
                    position(0, CurPosiY, 'x+', 0, TgtPosiY, 'y-')
                    position(0, 0, 'x+', 0, TgtPosiX-CurPosiX, 'y-')
def outDoor():
    first = 1
    while(1):
        move('front')
        speed(PWMA,40)
        speed(PWMB,0)
        speed(PWMC,46)
        speed(PWMD,0)
        if GPIO.input(JGZ) == 0 and first == 1:
            first = 0
        if GPIO.input(JGZ) == 1 and GPIO.input(JGY) == 1 and first == 0:
            move('stop')
            break
def inDoor():
    first = 1
    while 1:
        speed(PWMA,0)
        speed(PWMB,45)
        speed(PWMC,0)
        speed(PWMD,50)
        time.sleep(0.2)
        if GPIO.input(JG) == 0 and first == 1:
                first = 0
        if GPIO.input(JG) == 1 and first == 0:
            move('stop')
            break


##方案二
s=serial.Serial("/dev/ttyAMA0", 9600, timeout=0.1) #设置串口
qrCodeDetector = cv2.QRCodeDetector() #设置扫码
pin_init()
s.write(data0)
time.sleep(1)
s.write(data0)
time.sleep(1)
step = 1
outDoor()
position(0, 0, 'x+', 2, 1, 'x+')
#扫码动作组
s.write(data1)
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret,frame = cap.read()
    # cv2.imshow('frame', frame)
    get_qr_data(frame)
    if len(data) != 0:
        print('data:',data)
        #识别颜色动作组
        s.write(data2)
        cap.release()
        break
    if cv2.waitKey(1) == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
time.sleep(3)
cap = cv2.VideoCapture(0)
while cap.isOpened():
    _, frame2 = cap.read()
    # cv2.imshow('frame2',frame2)
    yssb(frame2)
    if len(y) != 0:
        # cv2.destroyAllWindows()
        cap.release()
        s.write(data0)
        break
print('color:',y)
position(0, 0, 'x+', 2, -1, 'x+')
##############################################抓物料
if y['a'] == data[0]:
    s.write(data3)
    time.sleep(5)
    s.write(data6)
    time.sleep(6)
elif y['b'] == data[0]:
    s.write(data4)
    time.sleep(5)
    s.write(data6)
    time.sleep(6)
elif y['c'] == data[0]:
    s.write(data5)
    time.sleep(5)
    s.write(data6)
    time.sleep(6)
if y['a'] == data[1]:
    s.write(data3)
    time.sleep(5)
    s.write(data7)
    time.sleep(6)
elif y['b'] == data[1]:
    s.write(data4)
    time.sleep(5)
    s.write(data7)
    time.sleep(6)
elif y['c'] == data[1]:
    s.write(data5)
    time.sleep(5)
    s.write(data7)
    time.sleep(6)
###################################################
position(0, 0, 'x+', 2, 5, 'x-')
position(0, 0, 'x+', 6, 5, 'y+')
inDoor()
s.close() #关闭串口
GPIO.cleanup()