import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import pyautogui
import mss
import threading
import time


class AutoFishingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动钓鱼助手 WLK版")

        # 运行状态变量
        self.running = False
        self.detection_enabled = False

        # 创建GUI组件
        self.create_widgets()

        # 初始化截图区域
        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

        # OpenCV参数
        self.prev_frame = None
        self.sensitivity = 500
        self.roi = (0, 0, 300, 300)  # x, y, w, h

    def create_widgets(self):
        # 控制面板
        control_frame = ttk.LabelFrame(self.root, text="控制")
        control_frame.pack(padx=10, pady=5, fill="x")

        self.start_btn = ttk.Button(control_frame, text="开始", command=self.start_program)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ttk.Button(control_frame, text="停止", command=self.stop_program, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        # 状态显示
        status_frame = ttk.LabelFrame(self.root, text="状态")
        status_frame.pack(padx=10, pady=5, fill="x")

        self.status_label = ttk.Label(status_frame, text="等待启动...")
        self.status_label.pack()

        # 配置区域
        config_frame = ttk.LabelFrame(self.root, text="配置")
        config_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(config_frame, text="检测灵敏度:").grid(row=0, column=0, padx=5, sticky="w")
        self.sensitivity_scale = ttk.Scale(config_frame, from_=100, to=2000, orient="horizontal")
        self.sensitivity_scale.set(500)
        self.sensitivity_scale.grid(row=0, column=1, padx=5, sticky="ew")

        ttk.Button(config_frame, text="设置检测区域", command=self.set_roi).grid(row=1, column=0, columnspan=2, pady=5)

    def set_roi(self):
        self.detection_enabled = False
        self.status_label.config(text="请用鼠标选择检测区域...")

        # 使用pyautogui获取屏幕区域
        try:
            region = pyautogui.locateOnScreen('float_day.png')  # 需要一个参考截图
            if region:
                self.roi = (region, region, region, region)
                self.monitor = {
                    "top": region,
                    "left": region,
                    "width": region,
                    "height": region
                }
                self.status_label.config(text=f"检测区域已设置：{self.roi}")
        except Exception as e:
            self.status_label.config(text="区域设置失败，请手动调整参数")

    def start_program(self):
        self.running = True
        self.detection_enabled = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_label.config(text="运行中...")

        # 启动检测线程
        threading.Thread(target=self.detection_loop, daemon=True).start()

    def stop_program(self):
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="已停止")

    def cast_fishing(self):
        # 模拟抛竿动作
        pyautogui.press('1')  # 假设1键是抛竿
        time.sleep(2)

    def detection_loop(self):
        with mss.mss() as sct:
            while self.running:
                if self.detection_enabled:
                    raw_img = np.array(sct.grab(self.monitor))
                    gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)

                    if self.prev_frame is not None:
                        # 计算帧间差异
                        frame_diff = cv2.absdiff(gray, self.prev_frame)
                        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
                        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                        # 检测显著变化
                        for cnt in contours:
                            if cv2.contourArea(cnt) > self.sensitivity:
                                self.trigger_action()
                                break

                    self.prev_frame = gray.copy()
                    time.sleep(0.1)
                else:
                    time.sleep(1)

    def trigger_action(self):
        # 触发收杆动作
        self.detection_enabled = False
        pyautogui.click(button='right')  # 右键收杆
        self.status_label.config(text="检测到鱼汛！已收竿")
        time.sleep(3)  # 等待下次抛竿
        self.cast_fishing()
        time.sleep(5)  # 等待浮标稳定
        self.detection_enabled = True


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoFishingApp(root)
    root.mainloop()
