from math import *

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))


def rgb_to_hex(rgb):
    return '#'+'%02x%02x%02x' % rgb


def f_pass():
    pass

def get_rot(x, y, x0, y0, angle):
    x -= x0
    y -= y0
    size = (x**2+y**2)**.5
    base_angle = atan(x/y) + pi/2*(x<0) + pi/2*(x>0) - pi*(y>0)
    return (round(x0+cos(base_angle+angle)*size), round(y0-sin(base_angle+angle)*size))