import win32api
import win32con
import time
# import win32gui
# from pprint import pprint

from ctypes import *
import pygame
import pygame.midi
from pygame.locals import *

MIDI_KEY_DOWN = 144
MIDI_KEY_UP = 128

VK_CODE = {
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'spacebar': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'numpad_0': 0x60,
    'numpad_1': 0x61,
    'numpad_2': 0x62,
    'numpad_3': 0x63,
    'numpad_4': 0x64,
    'numpad_5': 0x65,
    'numpad_6': 0x66,
    'numpad_7': 0x67,
    'numpad_8': 0x68,
    'numpad_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE
}

MAKE_CODE = {
    'a': 0x1C,
    'b': 0x32,
    'c': 0x21,
    'd': 0x23,
    'e': 0x24,
    'f': 0x2B,
    'g': 0x34,
    'h': 0x33,
    'i': 0x43,
    'j': 0x3B,
    'k': 0x42,
    'l': 0x4B,
    'm': 0x3A,
    'n': 0x31,
    'o': 0x44,
    'p': 0x4D,
    'q': 0x15,
    'r': 0x2D,
    's': 0x1B,
    't': 0x2C,
    'u': 0x3C,
    'v': 0x2A,
    'w': 0x1D,
    'x': 0x22,
    'y': 0x35,
    'z': 0x1A,
    ';': 0x27,
    'backspace': 0x66,
    'tab': 0x0D,
    'enter': 0x5A,
    'shift': 0x12,
    'ctrl': 0x14,
    'alt': 0x11,
    'esc': 0x76,
    'spacebar': 0x29,
    'left_arrow': 0x4B,
    'up_arrow': 0x48,
    'right_arrow': 0x4D,
    'down_arrow': 0x50,
    'volume_up': 144,  # TODO
    'volume_down': 145,  # TODO
    'F3': 0x3D,
    'F4': 0x3E,
}

BREAK_CODE = {'a': 268, 'b': 274, 'c': 257, 'd': 259, 'e': 260,
              'f': 267, 'g': 276, 'h': 275, 'i': 259, 'j': 283,
              'k': 258, 'l': 267, 'm': 282, 'n': 273, 'o': 260,
              'p': 269, 'q': 261, 'r': 269, 's': 267, 't': 268,
              'u': 284, 'v': 266, 'w': 269, 'x': 258, 'y': 277,
              'z': 266, ';': 263, 'backspace': 294, 'tab': 261,
              'enter': 282, 'shift': 258, 'ctrl': 260, 'alt': 257,
              'esc': 310, 'spacebar': 265, 'left_arrow': 267,
              'up_arrow': 264, 'right_arrow': 269,
              'down_arrow': 272, 'volume_up': 272,
              'volume_down': 273, 'F3': 285, 'F4': 286}


CONFIG = {
    32: 'a',
    33: 's',
    34: 'l',
    35: ';',
    36: 'd',
    37: 'f',
    38: 'j',
    39: 'k',
    48: 'spacebar',
    49: 'spacebar',
    50: 'spacebar',
    51: 'spacebar',
    52: 'spacebar',
    53: 'spacebar',
    54: 'spacebar',
    55: 'spacebar',
    56: 'spacebar',
    57: 'spacebar',
    58: 'spacebar',
    59: 'spacebar',
    60: 'spacebar',
    61: 'spacebar',
    62: 'spacebar',
    63: 'spacebar',
    64: 'spacebar',
    65: 'spacebar',
    66: 'spacebar',
    67: 'spacebar',
    68: 'spacebar',
    69: 'spacebar',
    70: 'spacebar',
    71: 'spacebar',
    72: 'enter'
}


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


def key_input(string=''):
    for c in string:
        win32api.keybd_event(VK_CODE[c], 0, 0, 0)
        win32api.keybd_event(VK_CODE[c], 0, 3, 0)
        time.sleep(0.001)


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()


def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, _input, _output, opened) = r

        in_out = ""
        if _input:
            in_out = "(input)"
        if _output:
            in_out = "(output)"

        print("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
              (i, interf, name, opened, in_out))


def input_main(device_id=None):
    pygame.init()
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)

    pygame.display.set_mode((1, 1))

    going = True
    # pos_x, pos_y = get_mouse_point()
    # xg, yg = 0, 0
    joy_x, joy_y = 64, 64
    k1, k2, k3, k8 = 0, 0, 0, 0
    while going:
        events = event_get()
        for e in events:
            if e.type in [QUIT]:
                going = False
            # if e.type in [KEYDOWN]:
            #     going = False
            if e.type in [pygame.midi.MIDIIN]:
                # print(e)
                key_status = e.status

                # pos_x, pos_y = get_mouse_point()
                #
                # if key_status is 224:  # 变动鼠标x加速度状态
                #     if e.data2 < 30:
                #         xg = -10
                #     elif e.data2 > 99:
                #         xg = 10
                #     else:
                #         xg = 0
                #
                # elif key_status is 176:  # 变动鼠标y加速度状态
                #     if e.data2 < 30:
                #         yg = 10
                #     elif e.data2 > 99:
                #         yg = -10
                #     else:
                #         yg = 0

                if key_status is 224:  # 变动摇杆x状态
                    flag = e.data2 - joy_x
                    if flag > 0 and e.data2 > 64:
                        m_code = MAKE_CODE['right_arrow']
                        time.sleep(0.01)
                        v_code = VK_CODE['right_arrow']
                        win32api.keybd_event(v_code, m_code, 1, 0)
                        time.sleep(0.01)
                        win32api.keybd_event(v_code, BREAK_CODE['right_arrow'], 3, 0)
                    elif flag < 0 and e.data2 < 64:
                        m_code = MAKE_CODE['left_arrow']
                        time.sleep(0.01)
                        v_code = VK_CODE['left_arrow']
                        win32api.keybd_event(v_code, m_code, 1, 0)
                        time.sleep(0.01)
                        win32api.keybd_event(v_code, BREAK_CODE['right_arrow'], 3, 0)
                    joy_x = e.data2

                elif key_status is 176:
                    if e.data1 == 1:  # 变动摇杆y状态
                        flag = e.data2 - joy_y
                        if flag > 0 and e.data2 > 64:
                            m_code = MAKE_CODE['up_arrow']
                            v_code = VK_CODE['up_arrow']
                            win32api.keybd_event(v_code, m_code, 1, 0)
                            time.sleep(0.01)
                            win32api.keybd_event(v_code, 0xC8, 3, 0)
                        elif flag < 0 and e.data2 < 64:
                            m_code = MAKE_CODE['down_arrow']
                            v_code = VK_CODE['down_arrow']
                            win32api.keybd_event(v_code, m_code, 1, 0)
                            time.sleep(0.01)
                            win32api.keybd_event(v_code, 0xD0, 3, 0)
                        joy_y = e.data2
                    elif e.data1 == 5:  # 变动推子K1状态
                        flag = e.data2 - k1
                        if flag > 0 and e.data2 > 64:
                            m_code = MAKE_CODE['volume_up']
                            v_code = VK_CODE['volume_up']
                            win32api.keybd_event(v_code, m_code, 1, 0)
                            win32api.keybd_event(v_code, 0xF0, 3, 0)
                        elif flag < 0 and e.data2 < 64:
                            m_code = MAKE_CODE['volume_down']
                            v_code = VK_CODE['volume_down']
                            win32api.keybd_event(v_code, m_code, 1, 0)
                            win32api.keybd_event(v_code, 0xF0, 3, 0)
                        k1 = e.data2
                    elif e.data1 == 6:  # 变动推子K2状态
                        flag = e.data2 - k2
                        if flag > 0 and e.data2 > 64:
                            m_code = MAKE_CODE['right_arrow']
                            v_code = VK_CODE['right_arrow']
                            win32api.keybd_event(v_code, m_code, 1, 0)
                            time.sleep(0.01)
                            win32api.keybd_event(v_code, 0xF0, 3, 0)
                        elif flag < 0 and e.data2 < 64:
                            m_code = MAKE_CODE['left_arrow']
                            v_code = VK_CODE['left_arrow']
                            win32api.keybd_event(v_code, m_code, 1, 0)
                            time.sleep(0.01)
                            win32api.keybd_event(v_code, 0xF0, 3, 0)
                        k2 = e.data2
                    elif e.data1 == 7:  # 变动推子K3状态
                        flag = e.data2 - k3
                        if flag > 0 and e.data2 > 64:
                            m_code = MAKE_CODE['F4']
                            v_code = VK_CODE['F4']
                            win32api.keybd_event(v_code, m_code, 1, 0)
                            time.sleep(0.01)
                            win32api.keybd_event(v_code, 0xF0, 3, 0)
                        elif flag < 0 and e.data2 < 64:
                            m_code = MAKE_CODE['F3']
                            v_code = VK_CODE['F3']
                            win32api.keybd_event(v_code, m_code, 1, 0)
                            time.sleep(0.01)
                            win32api.keybd_event(v_code, 0xF0, 3, 0)
                        k3 = e.data2
                    elif e.data1 == 12:  # 变动推子K8状态
                        if e.data2 == 0:
                            m_code = MAKE_CODE['esc']
                            v_code = VK_CODE['esc']
                            win32api.keybd_event(v_code, m_code, 1, 0)
                            time.sleep(0.01)
                            win32api.keybd_event(v_code, 0xF0, 3, 0)
                        else:
                            for _key in ['d', 'f', 'j', 'k']:
                                m_code = MAKE_CODE[_key]
                                v_code = VK_CODE[_key]
                                win32api.keybd_event(v_code, m_code, 1, 0)
                                time.sleep(0.001)
                                win32api.keybd_event(v_code, 0xF0, 3, 0)

                if key_status is 153:  # 按下打击垫
                    midi_key = CONFIG[e.data1]
                    # win32api.keybd_event(CONFIG[midi_key], 0, 0, 0)
                    # win32api.keybd_event(VK_CODE[midi_key], 0, 0, 0)
                    win32api.keybd_event(VK_CODE[midi_key], MAKE_CODE[midi_key], 1, 0)

                elif key_status is 137:  # 抬起打击垫
                    midi_key = CONFIG[e.data1]
                    # win32api.keybd_event(CONFIG[midi_key], 0, 0, 0)
                    win32api.keybd_event(VK_CODE[midi_key], MAKE_CODE[midi_key], 3, 0)

                elif key_status is 144:  # 按下键盘
                    midi_key = CONFIG[e.data1]
                    # win32api.keybd_event(CONFIG[midi_key], 0, 0, 0)
                    win32api.keybd_event(VK_CODE[midi_key], MAKE_CODE[midi_key], 1, 0)

                elif key_status is 128:  # 抬起键盘
                    midi_key = CONFIG[e.data1]
                    # win32api.keybd_event(CONFIG[midi_key], 0, 0, 0)
                    win32api.keybd_event(VK_CODE[midi_key], MAKE_CODE[midi_key], 3, 0)

                    # windll.user32.SetCursorPos(pos_x + xg, pos_y + yg)

        if i.poll():
            midi_events = i.read(1)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)

    del i
    pygame.midi.quit()


if __name__ == '__main__':
    input_main()
