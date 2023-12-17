from math import *
import pyaudio


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


def list_input_devices():
    p = pyaudio.PyAudio()
    devices = []
    c = 1
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0 and device_info['hostApi'] == 1:
            devices.append(f"{c} - {device_info['name']}")
            c += 1

    p.terminate()
    return devices
