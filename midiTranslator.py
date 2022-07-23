# UTF-8
import win32api
import win32con
import time
import threading
# import win32gui
# from pprint import pprint

from ctypes import *
import pygame
import os
import json
import pygame.midi
from pygame.locals import *

# 设置为True可以获取到MIDI键盘输入信息
DEBUG = False
# DEBUG = True

DEVICE_ID = None
# key为MIDI键盘key码（MIDI键盘输入信息中的"data2"）， value为在VK_CODE中存在的可模拟的键盘键位key
KEY_CONFIG = None
WHEEL_CONFIG = None
if os.path.exists('config.json'):
    with open('config.json', 'r', encoding='utf8') as f:
        config_f = json.loads(''.join([line for line in f.readlines() if not line.strip().startswith('//')]))
    KEY_CONFIG = {int(k): v for k, v in config_f.get('KEY_CONFIG', None).items()}
    WHEEL_CONFIG = {int(k): v for k, v in config_f.get('WHEEL_CONFIG', None).items()}
    DEBUG = config_f.get('DEBUG', True)
    DEVICE_ID = config_f.get('DEVICE_ID', None)

KEY_CONFIG = KEY_CONFIG or {
    32: 'd',
    33: 'f',
    34: 'j',
    35: 'k',
    36: 'd',
    37: 'f',
    38: 'j',
    39: 'k',
    48: 'spacebar',
    49: 'spacebar',
    50: 'spacebar',
    51: 'spacebar',
    52: 'spacebar',
    53: 'a',
    54: 'spacebar',
    55: 's',
    56: 'spacebar',
    57: 'd',
    58: 'spacebar',
    59: 'f',
    60: 'j',
    61: 'spacebar',
    62: 'k',
    63: 'spacebar',
    64: 'l',
    65: ';',
    66: 'spacebar',
    67: 'spacebar',
    68: 'spacebar',
    69: 'spacebar',
    70: 'spacebar',
    71: 'spacebar',
    72: 'enter'
}
WHEEL_CONFIG = WHEEL_CONFIG or {
    -1: ('right_arrow', 'left_arrow'),
    1: ('up_arrow', 'down_arrow'),
    5: ('up_arrow', 'down_arrow'),
    6: ('right_arrow', 'left_arrow'),
    7: ('F4', 'F3'),
    8: ('volume_up', 'volume_down'),
    9: ('spacebar', 'enter'),
}

"""
以上为MIDI键盘对应的模拟键位设置，以下为程序
"""

not_use_vk = {
    'F13': 124, 'F14': 125, 'F15': 126, 'F16': 127, 'F17': 128, 'F18': 129, 'F19': 130, 'F20': 131, 'F21': 132,
    'F22': 133, 'F23': 134, 'F24': 135, '\\': 220, 'clear': 12, 'clear_key': 254, 'crsel_key': 247, 'ctrl': 17,
    'decimal_key': 110, 'execute': 43, 'exsel_key': 248, 'help': 47, 'play_key': 250, 'print': 42, 'select': 41,
    'shift': 16, 'zoom_key': 251}

VK_CODE = {
    'backspace': 0x08, 'tab': 0x09, 'clear': 0x0C, 'enter': 0x0D, 'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
    'pause': 0x13, 'caps_lock': 0x14, 'esc': 0x1B, 'spacebar': 0x20, 'page_up': 0x21, 'page_down': 0x22,
    'end': 0x23, 'home': 0x24, 'left_arrow': 0x25, 'up_arrow': 0x26, 'right_arrow': 0x27, 'down_arrow': 0x28,
    'select': 0x29, 'print': 0x2A, 'execute': 0x2B, 'print_screen': 0x2C, 'ins': 0x2D, 'del': 0x2E, 'help': 0x2F,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
    'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F, 'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
    'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A, 'left_win': 0x5B, 'right_win': 0x5C,
    'applications': 0x5D, 'numpad_0': 0x60, 'numpad_1': 0x61, 'numpad_2': 0x62, 'numpad_3': 0x63,
    'numpad_4': 0x64, 'numpad_5': 0x65, 'numpad_6': 0x66, 'numpad_7': 0x67, 'numpad_8': 0x68, 'numpad_9': 0x69,
    'multiply_key': 0x6A, 'add_key': 0x6B,
    'separator_key': 0x6C,  # 小键盘enter
    'subtract_key': 0x6D, 'decimal_key': 0x6E, 'divide_key': 0x6F, 'F1': 0x70, 'F2': 0x71, 'F3': 0x72,
    'F4': 0x73, 'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78, 'F10': 0x79, 'F11': 0x7A,
    'F12': 0x7B, 'F13': 0x7C, 'F14': 0x7D, 'F15': 0x7E, 'F16': 0x7F, 'F17': 0x80, 'F18': 0x81, 'F19': 0x82,
    'F20': 0x83, 'F21': 0x84, 'F22': 0x85, 'F23': 0x86, 'F24': 0x87, 'num_lock': 0x90, 'scroll_lock': 0x91,
    'left_shift': 0xA0, 'right_shift': 0xA1, 'left_control': 0xA2, 'right_control': 0xA3, 'left_menu': 0xA4,
    'right_menu': 0xA5, 'browser_back': 0xA6, 'browser_forward': 0xA7, 'browser_refresh': 0xA8,
    'browser_stop': 0xA9, 'browser_search': 0xAA, 'browser_favorites': 0xAB, 'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD, 'volume_down': 0xAE, 'volume_up': 0xAF, 'next_track': 0xB0, 'previous_track': 0xB1,
    'stop_media': 0xB2, 'play/pause_media': 0xB3, 'start_mail': 0xB4, 'select_media': 0xB5,
    'start_application_1': 0xB6, 'start_application_2': 0xB7, 'attn_key': 0xF6, 'crsel_key': 0xF7,
    'exsel_key': 0xF8, 'play_key': 0xFA, 'zoom_key': 0xFB, 'clear_key': 0xFE, '=': 0xBB, ',': 0xBC, '-': 0xBD,
    '.': 0xBE, '/': 0xBF, '`': 0xC0, ';': 0xBA, '[': 0xDB, '\\': 0xDC, ']': 0xDD, "'": 0xDE, 'Unknown': 0
}
wangshang_yuanshi_make_code_set1 = {
    "esc": 0x01, "1": 0x02, "2": 0x03, "3": 0x04, "4": 0x05, "5": 0x06, "6": 0x07, "7": 0x08, "8": 0x09, "9": 0x0a,
    "0": 0x0b, "-": 0x0c, "=": 0x0d, "bksp": 0x0e, "tab": 0x0f, "q": 0x10, "w": 0x11, "e": 0x12, "r": 0x13, "t": 0x14,
    "y": 0x15, "u": 0x16, "i": 0x17, "o": 0x18, "p": 0x19, "[": 0x1a, "]": 0x1b, "enter": 0x1c, "l_ctrl": 0x1d,
    "a": 0x1e, "s": 0x1f, "d": 0x20, "f": 0x21, "g": 0x22, "h": 0x23, "j": 0x24, "k": 0x25, "l": 0x26, ";": 0x27,
    "'": 0x28, "`": 0x29, "l_shft": 0x2a, "z": 0x2c, "x": 0x2d, "c": 0x2e, "v": 0x2f, "b": 0x30, "n": 0x31,
    "m": 0x32, ",": 0x33, ".": 0x34, "/": 0x35, "r_shft": 0x36, "kp_*": 0x37, "l_alt": 0x38, "space": 0x39,
    "caps": 0x3a, "f1": 0x3b, "f2": 0x3c, "f3": 0x3d, "f4": 0x3e, "f5": 0x3f, "f6": 0x40, "f7": 0x41, "f8": 0x42,
    "f9": 0x43, "f10": 0x44, "num": 0x45, "scroll": 0x46, "kp_7": 0x47, "kp_8": 0x48, "kp_9": 0x49, "kp_-": 0x4a,
    "kp_4": 0x4b, "kp_5": 0x4c, "kp_6": 0x4d, "kp_+": 0x4e, "kp_1": 0x4f, "kp_2": 0x50, "kp_3": 0x51, "kp_0": 0x52,
    "kp_.": 0x53, "f11": 0x57, "f12": 0x58, "kp_en": 0xe01c, "r_ctrl": 0xe01d, "kp_/": 0xe035, "r_alt": 0xe038,
    "home": 0xe047, "up_arrow": 0xe048, "pg_up": 0xe049, "l_arrow": 0xe04b, "r_arrow": 0xe04d, "end": 0xe04f,
    "d_arrow": 0xe050, "pg_dn": 0xe051, "insert": 0xe052, "delete": 0xe053, "l_gui": 0xe05b, "r_gui": 0xe05c,
    "apps": 0xe05d}

MAKE_CODE = {
    'esc': 1, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, '6': 7, '7': 8, '8': 9, '9': 10, '0': 11, '-': 12,
    '=': 13, 'backspace': 14, 'tab': 15, 'q': 16, 'w': 17, 'e': 18, 'r': 19, 't': 20, 'y': 21, 'u': 22,
    'i': 23, 'o': 24, 'p': 25, '[': 26, ']': 27, 'enter': 28, 'a': 30, 's': 31, 'd': 32, 'f': 33, 'g': 34,
    'h': 35, 'j': 36, 'k': 37, 'l': 38, ';': 39, "'": 40, '`': 41, 'z': 44, 'x': 45, 'c': 46, 'v': 47,
    'b': 48, 'n': 49, 'm': 50, ',': 51, '.': 52, '/': 53, 'spacebar': 57, 'F1': 59, 'F2': 60, 'F3': 61,
    'F4': 62, 'F5': 63, 'F6': 64, 'F7': 65, 'F8': 66, 'F9': 67, 'F10': 68, 'home': 57415, 'up_arrow': 57416,
    'end': 57423, 'F11': 87, 'F12': 88, 'numpad_0': 82, 'numpad_1': 79, 'numpad_2': 80, 'numpad_3': 81,
    'numpad_4': 75, 'numpad_5': 76, 'numpad_6': 77, 'numpad_7': 71, 'numpad_8': 72, 'numpad_9': 73,
    'left_arrow': 57419, 'left_control': 29, 'left_shift': 42, 'right_arrow': 57421, 'right_control': 57373,
    'scroll_lock': 70, 'caps_lock': 58, 'del': 57427, 'ins': 57426, 'left_menu': 56,
    'page_down': 57425, 'page_up': 57417, 'right_menu': 57400, 'down_arrow': 57424,
    'num_lock': 69, 'pause': 3776792033, 'right_shift': 54, 'print_screen': 3760906295, 'multiply_key': 55,
    'attn_key': 83, 'subtract_key': 74, 'divide_key': 57397, 'add_key': 78, 'alt': 56, 'separator_key': 57372,
    'applications': 57437, 'left_win': 57435, 'right_win': 57436,
    'start_application_1(calculator?)': 57387,  # TODO
    'start_application_2(my_computer?)': 57408,  # TODO
    # 以下为scan code set2
    'next_track': 57421, 'previous_track': 57365, 'volume_up': 57394, 'volume_down': 57377,
    'start_mail': 57416, 'select_media': 57424, 'play/pause_media': 57396, 'stop_media': 57403,
    'volume_mute': 57379, 'browser_back': 57400, 'browser_favorites': 57368, 'browser_forward': 57392,
    'browser_start_and_home': 57402, 'browser_refresh': 57376, 'browser_search': 57360, 'browser_stop': 57384,
    'Unknown': 0
}

BREAK_CODE = {
    'esc': 128, '1': 128, '2': 129, '3': 128, '4': 129, '5': 130, '6': 131, '7': 128, '8': 129, '9': 130, '0': 131,
    '-': 132, '=': 133, 'backspace': 134, 'tab': 135, 'q': 128, 'w': 129, 'e': 130, 'r': 131, 't': 132, 'y': 133,
    'u': 134, 'i': 135, 'o': 136, 'p': 137, '[': 138, ']': 139, 'enter': 140, 'a': 142, 's': 143, 'd': 128, 'f': 129,
    'g': 130, 'h': 131, 'j': 132, 'k': 133, 'l': 134, ';': 135, "'": 136, '`': 137, 'z': 140, 'x': 141, 'c': 142,
    'v': 143, 'b': 144, 'n': 145, 'm': 146, ',': 147, '.': 148, '/': 149, 'spacebar': 153, 'F1': 155, 'F2': 156,
    'F3': 157, 'F4': 158, 'F5': 159, 'F6': 128, 'F7': 129, 'F8': 130, 'F9': 131, 'F10': 132, 'home': 57415,
    'up_arrow': 57416, 'end': 57423, 'F11': 151, 'F12': 152, 'numpad_0': 146, 'numpad_1': 143, 'numpad_2': 144,
    'numpad_3': 145, 'numpad_4': 139, 'numpad_5': 140, 'numpad_6': 141, 'numpad_7': 135, 'numpad_8': 136,
    'numpad_9': 137, 'left_arrow': 57419, 'left_control': 141, 'left_shift': 138, 'right_arrow': 57421,
    'right_control': 57373, 'scroll_lock': 134, 'caps_lock': 154, 'del': 57427, 'ins': 57426, 'left_menu': 152,
    'page_down': 57425, 'page_up': 57417, 'right_menu': 57400, 'down_arrow': 57424, 'num_lock': 133,
    'pause': 3776792033, 'right_shift': 150, 'print_screen': 3760906295, 'multiply_key': 151, 'attn_key': 147,
    'subtract_key': 138, 'divide_key': 57397, 'add_key': 142, 'alt': 152, 'separator_key': 57372, 'applications': 57437,
    'left_win': 57435, 'right_win': 57436, 'start_application_1(calculator?)': 57387,
    'start_application_2(my_computer?)': 57408, 'next_track': 57421, 'previous_track': 57365, 'volume_up': 57394,
    'volume_down': 57377, 'start_mail': 57416, 'select_media': 57424, 'play/pause_media': 57396, 'stop_media': 57403,
    'volume_mute': 57379, 'browser_back': 57400, 'browser_favorites': 57368, 'browser_forward': 57392,
    'browser_start_and_home': 57402, 'browser_refresh': 57376, 'browser_search': 57360, 'browser_stop': 57384,
    'Unknown': 0
}

Cache = {'keypress': {}, 'keyfastpress': {}}


class MyKeyPressThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.bool_stop = False
        self.check_key_press_interval = 0.05
        self.check_key_delay = 0.5

    def run(self):
        while not self.bool_stop:
            time_now = time.time()
            try:
                # print(Cache)
                for key_code, press_time in Cache['keypress'].items():
                    if press_time < (time_now - self.check_key_delay):
                        key_press(key_code)
            except (RuntimeError, KeyError):
                pass
            time.sleep(self.check_key_press_interval - 0.005)

    def stop(self):
        self.bool_stop = True


class MyKeyFastPressThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.bool_stop = False
        self.check_key_press_interval = 0.005
        self.check_key_delay = 0.001

    def run(self):
        while not self.bool_stop:
            time_now = time.time()
            try:
                # print(Cache)
                for key_code, press_time in Cache['keyfastpress'].items():
                    if press_time < (time_now - self.check_key_delay):
                        key_input(key_code)
            except (RuntimeError, KeyError):
                pass
            time.sleep(self.check_key_press_interval - 0.005)

    def stop(self):
        self.bool_stop = True


class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


po = POINT()


def get_mouse_point():
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)


def mouse_click(x=None, y=None):
    if x and y:
        mouse_move(x, y)
        time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def mouse_dclick(x=None, y=None):
    if x and y:
        mouse_move(x, y)
        time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def mouse_move(x, y):
    windll.user32.SetCursorPos(x, y)


def key_input_vk(key_name):
    key = VK_CODE[key_name]
    key_input(key)


def key_input(key_code):
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 2, 0)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 3, 0)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 1, 0)
    time.sleep(0.01)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 2, 0)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 3, 0)


def key_down(key_code):
    # win32api.keybd_event(VK_CODE[midi_key], MAKE_CODE.get(midi_key, 0), 1, 0)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 0, 0)
    # win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 1, 0)
    Cache['keypress'][key_code] = time.time()


def key_press(key_code):
    # win32api.keybd_event(VK_CODE[midi_key], MAKE_CODE.get(midi_key, 0), 1, 0)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 1, 0)


def key_up(key_code):
    # time.sleep(0.001)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 2, 0)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 3, 0)
    try:
        Cache['keypress'].pop(key_code)
    except KeyError:
        pass


def key_fast_down(key_code):
    # win32api.keybd_event(VK_CODE[midi_key], MAKE_CODE.get(midi_key, 0), 1, 0)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 0, 0)
    # win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 1, 0)
    Cache['keyfastpress'][key_code] = time.time()


def key_fast_up(key_code):
    # win32api.keybd_event(VK_CODE[key_name], BREAK_CODE[midi_key], 3, 0)
    # time.sleep(0.001)
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0) + 0b10000000, 3, 0)
    try:
        Cache['keyfastpress'].pop(key_code)
    except KeyError:
        pass


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()


def _print_device_info():
    res = []
    s = 'All [%d] MIDI devices. Default MIDI input ID is:    [%d]' % (pygame.midi.get_count(), pygame.midi.get_default_input_id())
    res.append(s)
    print(s)
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, _input, _output, opened) = r

        in_out = ""
        if _input:
            in_out = "(input)"
        if _output:
            in_out = "(output)"

        s = "%2i: interface :%s:, name :%s:, opened :%s:  %s" % (i, interf, name, opened, in_out)
        res.append(s)
        print(s)
    return res


def wheel_key_input(midi_wheel_cc, wheel_pos):
    wheel_pos_last = Cache.get(midi_wheel_cc, 64)
    key1, key2 = WHEEL_CONFIG[midi_wheel_cc]
    key1, key2 = VK_CODE[key1], VK_CODE[key2]
    flag = wheel_pos - wheel_pos_last
    if flag > 0 and 127 > wheel_pos > 64:
        key_input(key1)
    elif flag < 0 < wheel_pos < 64:
        key_input(key2)

    if wheel_pos == 0:
        key_fast_down(key2)
    elif wheel_pos == 127:
        key_fast_down(key1)
    else:
        if wheel_pos_last in (0, 127):
            key_fast_up(key1)
            key_fast_up(key2)

    Cache[midi_wheel_cc] = wheel_pos


def input_main(device_id=None):
    pygame.init()
    SCREEN_SIZE = (640, 480)
    screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
    pygame.display.set_caption("midiTranslator v0.1", 'midiTranslator')

    if os.path.exists("./front.otf"):
        font = pygame.font.Font("./front.otf", 16)
    else:
        font = pygame.font.SysFont("Adobe Arabic", 16)
    font_height = font.get_linesize()
    event_text = []

    # 保证event_text里面只保留一个屏幕的文字
    # event_text = event_text[-SCREEN_SIZE[1] // font_height:]

    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    pygame.midi.init()

    event_text.extend(_print_device_info())
    screen.fill((41, 124, 248))

    # 寻找一个合适的起笔位置，最下面开始，留一行的空
    y = SCREEN_SIZE[1] - font_height
    for text in reversed(event_text):
        screen.blit(font.render(text, True, (139, 196, 94)), (0, y))
        y -= font_height
    pygame.display.update()

    if device_id is None and not DEVICE_ID:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id or DEVICE_ID

    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)

    if not DEBUG:
        pygame.display.set_mode((1, 1))

    going = True
    while going:
        events = event_get()
        for e in events:
            if e.type in [QUIT,
                          # KEYDOWN,
                          ]:
                going = False

            if e.type == VIDEORESIZE:
                screen = pygame.display.set_mode(e.size, RESIZABLE, 32)
                # pygame.display.set_caption("Window resized to " + str(e.size))

            if e.type in [pygame.midi.MIDIIN]:
                if DEBUG:
                    # print(e)
                    event_text.append('status[{:03d}]  KeyID[{:03d}]     power[{:03d}]'.format(e.status, e.data1, e.data2))
                    if len(event_text) > 20:
                        event_text.pop(0)
                    screen.fill((41, 124, 248))

                    # 寻找一个合适的起笔位置，最下面开始，留一行的空
                    y = SCREEN_SIZE[1] - font_height
                    for text in reversed(event_text):
                        screen.blit(font.render(text, True, (139, 196, 94)), (0, y))
                        y -= font_height
                    pygame.display.update()

                    # print('动作[{}] KeyID[{}] 力度[{}]'.format(e.status, e.data1, e.data2))
                key_status = e.status

                # 变动摇杆x状态
                if key_status is 224:
                    wheel_key_input(-1, e.data2)

                elif key_status is 176:
                    # 变动摇杆y状态
                    wheel = e.data1
                    if wheel in WHEEL_CONFIG:
                        wheel_key_input(wheel, e.data2)

                    # 变动推子K8状态
                    elif e.data1 == 12:
                        if e.data2 == 0:
                            key_input_vk('esc')
                        else:
                            for _key in ['d', 'f', 'j', 'k']:
                                m_code = MAKE_CODE[_key]
                                v_code = VK_CODE[_key]
                                win32api.keybd_event(v_code, m_code, 1, 0)
                                time.sleep(0.001)
                            for _key in ['d', 'f', 'j', 'k']:
                                v_code = VK_CODE[_key]
                                win32api.keybd_event(v_code, 0xF0, 3, 0)

                    # 变动推子K7状态
                    elif e.data1 == 11:
                        if 25 > e.data2 > 0:
                            key_input_vk('4')
                        elif 50 > e.data2 > 25:
                            key_input_vk('5')
                        elif 75 > e.data2 > 50:
                            key_input_vk('6')
                        elif 100 > e.data2 > 75:
                            key_input_vk('7')
                        elif 125 > e.data2 > 100:
                            key_input_vk('8')

                # 按下打击垫\键盘
                elif key_status is 153 or key_status is 144:
                    key_down(VK_CODE[KEY_CONFIG.get(e.data1, 'Unknown')])

                # 抬起打击垫\键盘
                elif key_status is 137 or key_status is 128 or (key_status is 144 and e.data2 is 1):
                    key_up(VK_CODE[KEY_CONFIG.get(e.data1, 'Unknown')])

        if i.poll():
            midi_events = i.read(1)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)

    del i
    pygame.midi.quit()


if __name__ == '__main__':
    # if (joy_x | joy_y | k1 | k2 | k3 | k8) is 127 or (joy_x & joy_y & k1 & k2 & k3 & k8) is 0:
    #     for key, st in {joy_x, joy_y, k1, k2, k3, k8}:
    th1 = MyKeyPressThread('keypress')
    th2 = MyKeyFastPressThread('keyfastpress')
    th1.start()
    th2.start()
    input_main()
    th1.stop()
    th2.stop()

    # for _ in range(3):
    #     time.sleep(1)
    #     # key_input_vk('+')
    #     key_input(0x5D)
