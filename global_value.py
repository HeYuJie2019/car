def _init():
    global _global_dict
    acceleration = [0, 0, 0] #加速度
    angle_degree = [0, 0, 0] #欧拉角
    x_dis = 0
    y_dis = 0
    _global_dict = {'jsd':acceleration}
    _global_dict = {'jd':angle_degree}
    _global_dict = {'x_dis':x_dis}
    _global_dict = {'y_dis':y_dis}

def set_value(key,value):
    _global_dict[key] = value

def get_value(key,defValue=None):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
