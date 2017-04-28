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
}
BREAK_CODE = {}
for k, v in MAKE_CODE.items():
    BREAK_CODE[k] = int('0b1' + '0' * (7-len(bin(v)[3:])) +bin(v)[3:], 2)

print(BREAK_CODE)
