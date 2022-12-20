import RPi.GPIO as GPIO
import threading
import time
import pigpio
import numpy as np
import cv2
import serial
import struct
import serial
import struct
import serial
import global_value
global_value._init()  #全局变量初始化，初始化字典
key = 0    #陀螺仪函数的全局变量
buff = {}  #陀螺仪函数的全局变量
wt_imu = serial.Serial("/dev/ttyAMA1", baudrate=115200) #设置陀螺仪串口
s = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.1) #设置机械臂串口
pm = serial.Serial("/dev/ttyAMA3", 9600, timeout=0.1) #设置屏幕串口
qrCodeDetector = cv2.QRCodeDetector() #设置扫码实例
pi = pigpio.pi()
E1A = 18
JGZ = 17
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
start_z = 0  #初始化z轴方向
y = {}
data = []  #存放扫码数据
ys = [] #存放扫码数据
#动作组
end = bytes.fromhex('ff ff ff')
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
    GPIO_in_list = (E1A, JGZ, JGY)
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
    elif direction == 'back' :
        GPIO.output(AIN1,0)
        GPIO.output(AIN2,1)
        GPIO.output(BIN1,0)
        GPIO.output(BIN2,1)
        GPIO.output(CIN1,1)
        GPIO.output(CIN2,0)
        GPIO.output(DIN1,1)
        GPIO.output(DIN2,0)
    elif direction == 'xuanzhuanzuo':
        GPIO.output(AIN1,1)
        GPIO.output(AIN2,0)
        GPIO.output(BIN1,0)
        GPIO.output(BIN2,1)
        GPIO.output(CIN1,1)
        GPIO.output(CIN2,0)
        GPIO.output(DIN1,0)
        GPIO.output(DIN2,1)
    elif direction == 'xuanzhuanyou':
        GPIO.output(AIN1,0)
        GPIO.output(AIN2,1)
        GPIO.output(BIN1,1)
        GPIO.output(BIN2,0)
        GPIO.output(CIN1,0)
        GPIO.output(CIN2,1)
        GPIO.output(DIN1,1)
        GPIO.output(DIN2,0)
    elif direction == 'zuo':
        GPIO.output(AIN1,1)
        GPIO.output(AIN2,0)
        GPIO.output(BIN1,0)
        GPIO.output(BIN2,1)
        GPIO.output(CIN1,0)
        GPIO.output(CIN2,1)
        GPIO.output(DIN1,1)
        GPIO.output(DIN2,0)
    elif direction == 'you':
        GPIO.output(AIN1,0)
        GPIO.output(AIN2,1)
        GPIO.output(BIN1,1)
        GPIO.output(BIN2,0)
        GPIO.output(CIN1,1)
        GPIO.output(CIN2,0)
        GPIO.output(DIN1,0)
        GPIO.output(DIN2,1)
    elif direction == 'stop':
        speed(PWMA,0)
        speed(PWMB,0)
        speed(PWMC,0)
        speed(PWMD,0)
    else:
        speed(PWMA,0)
        speed(PWMB,0)
        speed(PWMC,0)
        speed(PWMD,0)
################################################################
#快速
def forward_fast_speed():
    move('front')
    speed(PWMA,60)  #60
    speed(PWMB,59.5)#59.5
    speed(PWMC,80)  #80
    speed(PWMD,80)  #80
#慢速
def forward_slow_speed():
    move('front')
    speed(PWMA,22)  #33
    speed(PWMB,20)  #31
    speed(PWMC,40)  #35
    speed(PWMD,40)  #36
#中速前进
def forward_middle_speed():
    global start_z
    move('front')
    if get_jd(2) - start_z < -1: #向右偏
        speed(PWMA,33)  #33
        speed(PWMB,20)  #30
        speed(PWMC,45)  #50
        speed(PWMD,50)  #50
    elif get_jd(2) - start_z < -0.3: #向右偏
        speed(PWMA,33)  #33
        speed(PWMB,27)  #30
        speed(PWMC,48)  #50
        speed(PWMD,50)  #50
    elif get_jd(2) - start_z > 1: #向左偏
        speed(PWMA,20)  #33
        speed(PWMB,30)  #30
        speed(PWMC,50)  #50
        speed(PWMD,45)  #50
    elif get_jd(2) - start_z > 0.3: #向左偏
        speed(PWMA,30)  #33
        speed(PWMB,30)  #30
        speed(PWMC,50)  #50
        speed(PWMD,48)  #50
    else:
        speed(PWMA,33)  #33
        speed(PWMB,30)  #30
        speed(PWMC,50)  #50
        speed(PWMD,50)  #50
#左移
def left_speed():
    move('zuo')
    if get_jd(2) - start_z < -1: #向右偏得更多
        speed(PWMA,50)  #30
        speed(PWMB,60)  #30
        speed(PWMC,50)  #30
        speed(PWMD,50)  #30
    elif get_jd(2) - start_z < -0.3: #向右偏
        speed(PWMA,50)  #30
        speed(PWMB,55)  #30
        speed(PWMC,50)  #30
        speed(PWMD,50)  #30
    elif get_jd(2) - start_z > 1: #向左偏得更多
        speed(PWMA,50)  #30
        speed(PWMB,50)  #30
        speed(PWMC,60)  #30
        speed(PWMD,50)  #30
    elif get_jd(2) - start_z > 0.3: #向左偏
        speed(PWMA,50)  #30
        speed(PWMB,50)  #30
        speed(PWMC,55)  #30
        speed(PWMD,50)  #30
    else:
        speed(PWMA,50)  #30
        speed(PWMB,50)  #30
        speed(PWMC,50)  #30
        speed(PWMD,50)  #30
#慢速右移
def right_slow_speed():
    move('you')
    if get_jd(2) - start_z < -1: #向右偏得更多
        speed(PWMA,25)  #30
        speed(PWMB,30)  #30
        speed(PWMC,35)  #30
        speed(PWMD,30)  #30
    elif get_jd(2) - start_z < -0.3: #向右偏
        speed(PWMA,28)  #30
        speed(PWMB,30)  #30
        speed(PWMC,32)  #30
        speed(PWMD,30)  #30
    elif get_jd(2) - start_z > 1: #向左偏得更多
        speed(PWMA,35)  #30
        speed(PWMB,30)  #30
        speed(PWMC,25)  #30
        speed(PWMD,30)  #30
    elif get_jd(2) - start_z > 0.3: #向左偏
        speed(PWMA,32)  #30
        speed(PWMB,30)  #30
        speed(PWMC,28)  #30
        speed(PWMD,30)  #30
    else:
        speed(PWMA,30)  #30
        speed(PWMB,30)  #30
        speed(PWMC,30)  #30
        speed(PWMD,30)  #30
#######################################################
#扫码
def get_qr_data(input_frame):
    global data
    global ys
    data = []
    ys = []
    try:
        data, bbox, straight_qrcode = qrCodeDetector.detectAndDecode(input_frame)
        if data[0] == '3':
            ys.append('b')
        elif data[0] == '2':
            ys.append('g')
        elif data[0] == '1':
            ys.append('r')
        if data[1] == '3':
            ys.append('b')
        elif data[1] == '2':
            ys.append('g')
        elif data[1] == '1':
            ys.append('r')
        if data[2] == '3':
            ys.append('b')
        elif data[2] == '2':
            ys.append('g')
        elif data[2] == '1':
            ys.append('r')
        if data[4] == '3':
            ys.append('b')
        elif data[4] == '2':
            ys.append('g')
        elif data[4] == '1':
            ys.append('r')
        if data[5] == '3':
            ys.append('b')
        elif data[5] == '2':
            ys.append('g')
        elif data[5] == '1':
            ys.append('r')
        if data[6] == '3':
            ys.append('b')
        elif data[6] == '2':
            ys.append('g')
        elif data[6] == '1':
            ys.append('r')
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
#陀螺仪程序
# 校验
def checkSum(list_data, check_data):
    return sum(list_data) & 0xff == check_data
# 16 进制转 ieee 浮点数
def hex_to_short(raw_data):
    return list(struct.unpack("hhhh", bytearray(raw_data)))
# 处理串口数据
def handleSerialData(raw_data):
    global buff
    global key
    angle_flag=False
    buff[key] = raw_data

    key += 1
    if buff[0] != 0x55:
        key = 0
        return
    if key < 11:  # 根据数据长度位的判断, 来获取对应长度数据
        return
    else:
        data_buff = list(buff.values())  # 获取字典所有 value
        if buff[1] == 0x51 :
            if checkSum(data_buff[0:10], data_buff[10]):
                global_value.set_value('jsd', [hex_to_short(data_buff[2:10])[i] / 32768.0 * 16 * 9.8 for i in range(0, 3)])
                # acceleration = [hex_to_short(data_buff[2:10])[i] / 32768.0 * 16 * 9.8 for i in range(0, 3)]

        elif buff[1] == 0x53:
            if checkSum(data_buff[0:10], data_buff[10]):
                global_value.set_value('jd', [hex_to_short(data_buff[2:10])[i] / 32768.0 * 180 for i in range(0, 3)])
                # angle_degree = [hex_to_short(data_buff[2:10])[i] / 32768.0 * 180 for i in range(0, 3)]
                angle_flag = True

        else:
            buff = {}
            key = 0

        buff = {}
        key = 0
def __tly__():
    while True:
        buff_count = wt_imu.inWaiting()
        buff_data = wt_imu.read(buff_count)
        for i in range(0, buff_count):
            handleSerialData(buff_data[i])
TLY = threading.Thread(target=__tly__)
#######################################################
def get_jd(axis,defValue=None):  #返回角度
    try :
        return global_value.get_value('jd')[axis]+180
    except TypeError:
        return defValue
def get_jsd(axis,defValue=None):  #返回加速度
    try :
        return global_value.get_value('jsd')[axis]
    except TypeError:
        return defValue
#######################################################
#出门
def OutDoor():
    t1 = time.time()
    t2 = time.time()
    while t2-t1<4:
        move('front')
        t2 = time.time()
        speed(PWMA,50)  #33
        speed(PWMB,0)  #30
        speed(PWMC,50)  #50
        speed(PWMD,0)  #50
#######################################################
#旋转
def xuanzhuan(jiaodu):
    target_z = start_z + jiaodu
    if target_z > 360:
        target_z = target_z - 360
    speed_xunazhuan = 0
    while 1:
        if get_jd(2) <= target_z - 0.1:
            move('xuanzhuanzuo')
        elif get_jd(2) >= target_z + 0.1:
            move('xuanzhuanyou')
        elif target_z-0.1 < get_jd(2) < target_z+0.1:
            break
        speed(PWMA, speed_xunazhuan)
        speed(PWMB, speed_xunazhuan)
        speed(PWMC, speed_xunazhuan)
        speed(PWMD, speed_xunazhuan)
        if abs(target_z - get_jd(2)) > 45 :
            speed_xunazhuan = 95
        elif abs(target_z - get_jd(2)) > 35 :
            speed_xunazhuan = 75
        elif abs(target_z - get_jd(2)) > 25 :
            speed_xunazhuan = 55
        elif abs(target_z - get_jd(2)) > 15 :
            speed_xunazhuan = 35
        elif abs(target_z - get_jd(2)) > 10 :
            speed_xunazhuan = 25
        elif abs(target_z - get_jd(2)) > 5 :
            speed_xunazhuan = 20
        elif abs(target_z - get_jd(2)) > 3 :
            speed_xunazhuan = 15
    move('stop')
#######################################################
#显示数字
def display_num(index, num):
    mes = 'n'+str(index)+'.val='+str(num)   #n0.val=0
    pm.write(bytearray(mes.encode()))
    pm.write(end)
#######################################################
#延时行走
def move_time(t):
    t1 = time.time()
    t2 = time.time()
    while t2-t1 < t:
        t2 = time.time()
        forward_middle_speed()
    move('stop')
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#*******************************************************
TLY.start()
time.sleep(1)
start_z = None   
while start_z == None:  #初始化角度Z，否则会返回None
    start_z = get_jd(2)
second_z = start_z + 90
if second_z > 360:
    second_z = second_z -360
third_z = start_z + 180
if third_z > 360:
    third_z = third_z -360
pin_init()
s.write(data0)
#向左走移动一段距离
t1 = time.time()
t2 = time.time()
while t2-t1<0.5:
    t2 = time.time()
    left_speed()
s.write(data1)
move('stop')
#向前走扫码
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    move('front')
    get_qr_data(frame)
    if len(ys) != 0:
        break
    forward_middle_speed()
for i in range(3):
    display_num(i, int(data[i]))
for i in range(3,6):
    display_num(i, int(data[i+1]))
s.write(data2)
#向前走识别物料
move_time(4.5)
xuanzhuan(90)
start_z = second_z
move_time(8)
xuanzhuan(90)
start_z = third_z   
move_time(8)
cap.release()
cv2.destroyAllWindows()
time.sleep(1)
GPIO.cleanup()
#*******************************************************
# Q = 0.00001
# R = 0.1
# P_k_k1 = 1
# Kg = 0
# P_k1_k1 = 1
# x_k_k1 = 0
# ADC_OLD_Value = 0
# kalman_adc_old = 0
# def kalman(ADC_Value):
#     global kalman_adc_old
#     global P_k1_k1
#     Z_k = ADC_Value
#     if (abs(kalman_adc_old-ADC_Value)>=80):
#         x_k1_k1= ADC_Value*0.382 + kalman_adc_old*0.618
#     else:
#         x_k1_k1 = kalman_adc_old;
#     x_k_k1 = x_k1_k1
#     P_k_k1 = P_k1_k1 + Q
#     Kg = P_k_k1/(P_k_k1 + R)
#     kalman_adc = x_k_k1 + Kg * (Z_k - kalman_adc_old)
#     P_k1_k1 = (1 - Kg)*P_k_k1
#     P_k_k1 = P_k1_k1
#     ADC_OLD_Value = ADC_Value
#     kalman_adc_old = kalman_adc
#     return kalman_adc

# #开启陀螺仪的进程
# TLY.start()
# time.sleep(1)
# start_z = None
# while start_z == None:  #初始化角度Z，否则会返回None
#     start_z = get_jd(2)

# x = 0
# y = 0
# v_x = 0
# v0_y = 0
# time.sleep(2)
# t1 = time.time()
# t2 = time.time()
# while 1:
#     ay = kalman(get_jsd(1))
#     v = v0_y + ay*1
#     v0_y = v
#     print('ay: ', ay, '  v: ', v)
    
