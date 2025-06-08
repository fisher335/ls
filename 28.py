import pyautogui
import time
import keyboard
import cv2
import numpy as np
from PIL import ImageGrab

# 配置参数
pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True

# Hekili 提示框区域 (需要根据你的屏幕调整)
HEKILI_BOX = {
    'left': 913,
    'top': 591,
    'width': 300,
    'height': 150
}

# 技能键位映射 (根据你的游戏键位设置)
SKILL_KEYS = {
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '0': '0',
    '-': '-',
    '=': '=',
    'F1': 'F1',
    'F2': 'F2',
    'F3': 'F3',
    'F4': 'F4'
}

# 技能数字模板 (需要提前截取保存为图片)
TEMPLATES = {
    '1': cv2.imread('templates/1.png', 0),
    '2': cv2.imread('templates/2.png', 0),
    '3': cv2.imread('templates/3.png', 0),
    '4': cv2.imread('templates/4.png', 0),
    '5': cv2.imread('templates/5.png', 0),
    '6': cv2.imread('templates/6.png', 0),
    '7': cv2.imread('templates/7.png', 0),
    '8': cv2.imread('templates/8.png', 0),
    '9': cv2.imread('templates/9.png', 0),
    '0': cv2.imread('templates/0.png', 0)
}

# 匹配阈值 (0.8-0.95通常效果不错)
THRESHOLD = 0.9


def capture_hekili_prompt():
    """捕获Hekili提示框区域的截图并转换为OpenCV格式"""
    screenshot = ImageGrab.grab(bbox=(
        HEKILI_BOX['left'],
        HEKILI_BOX['top'],
        HEKILI_BOX['left'] + HEKILI_BOX['width'],
        HEKILI_BOX['top'] + HEKILI_BOX['height']
    ))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)


def detect_skill_number(image):
    """使用模板匹配检测技能编号"""
    max_val = 0
    best_match = None

    for skill_num, template in TEMPLATES.items():
        if template is None:
            continue

        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        _, val, _, _ = cv2.minMaxLoc(res)

        if val > THRESHOLD and val > max_val:
            max_val = val
            best_match = skill_num

    return best_match


def press_skill_key(key):
    """按下技能键"""
    if key in SKILL_KEYS:
        pyautogui.press(SKILL_KEYS[key])
        print(f"Pressed key: {SKILL_KEYS[key]}")
        return True
    return False


def main_loop():
    print("自动技能释放脚本已启动 (按F12停止)...")

    while True:
        if keyboard.is_pressed('F12'):
            print("检测到F12按键，停止脚本...")
            break

        # 1. 捕获Hekili提示区域
        hekili_image = capture_hekili_prompt()

        # 2. 检测当前推荐的技能
        skill_num = detect_skill_number(hekili_image)

        # 3. 如果检测到技能，则按下对应按键
        if skill_num:
            if press_skill_key(skill_num):
                time.sleep(0.3)  # 技能释放后短暂延迟

        time.sleep(0.05)  # 主循环延迟


if __name__ == "__main__":
    print("准备启动自动技能释放脚本...")
    print("请确保已准备好技能数字模板图片")
    time.sleep(3)  # 给用户3秒时间切换到游戏窗口

    try:
        main_loop()
    except pyautogui.FailSafeException:
        print("检测到故障安全触发，脚本已停止")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        print("脚本已停止")