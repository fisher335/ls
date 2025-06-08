import json
import os
import time
import threading
import keyboard
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox


class HekiliAutoBot:
    CONFIG_FILE = "hekili_config.json"

    def __init__(self, root):
        self.root = root
        self.root.title("Hekili 自动技能助手 v2.2")

        # 运行状态
        self.running = False
        self.hotkey_listener_active = True

        # 默认配置
        self.default_config = {
            'hekili_box': {
                'left': 1000,
                'top': 800,
                'width': 300,
                'height': 150
            },
            'toggle_key': 'f1',
            'threshold': 0.85,
            'skill_delay': 0.3
        }

        # 当前配置
        self.config = self.load_config()
        self.toggle_key = self.config['toggle_key']

        # 技能键位映射
        self.skill_keys = {
            '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
            '6': 'q', '7': 'e', '8': 'r', '9': 'f', '0': '0',
            '-': '-', '=': '=', '10': 'g', '11': 'F2',
            'F3': 'F3', 'F4': 'F4'
        }

        # 确保模板目录存在
        if not os.path.exists('templates'):
            os.makedirs('templates')

        # 加载模板
        self.templates = self.load_templates()

        # 创建GUI
        self.create_gui()

        # 启动热键监听
        self.start_hotkey_listener()

        # 设置窗口关闭时的处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_config(self):
        """安全加载配置文件"""
        config = self.default_config.copy()
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    user_config = json.load(f)
                    # 只更新存在的配置项
                    for key in config:
                        if key in user_config:
                            config[key] = user_config[key]
        except Exception as e:
            print(f"加载配置失败: {e}")
        return config

    def save_config(self):
        """安全保存当前配置"""
        config_to_save = {
            'hekili_box': {
                'left': self.left_var.get(),
                'top': self.top_var.get(),
                'width': self.width_var.get(),
                'height': self.height_var.get()
            },
            'toggle_key': self.toggle_key,
            'threshold': self.threshold_var.get(),
            'skill_delay': self.delay_var.get()
        }

        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config_to_save, f, indent=4)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def load_templates(self):
        """加载技能数字模板"""
        templates = {}
        for i in range(12):
            try:
                template_path = f'templates/{i}.png'
                if os.path.exists(template_path):
                    templates[str(i)] = cv2.imread(template_path, 0)
                    if templates[str(i)] is None:
                        print(f"警告: 无法加载模板文件 {template_path}")
                else:
                    print(f"警告: 模板文件 {template_path} 不存在")
            except Exception as e:
                print(f"加载模板 {i} 时出错: {e}")
        return templates

    def create_gui(self):
        """创建用户界面"""
        # 主窗口设置
        self.root.geometry("450x550")
        self.root.resizable(False, False)

        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        ttk.Label(main_frame, text="Hekili 自动技能助手",
                  font=('Arial', 14, 'bold')).pack(pady=10)

        # 状态显示
        self.status_var = tk.StringVar(value="状态: 等待启动")
        ttk.Label(main_frame, textvariable=self.status_var,
                  font=('Arial', 12)).pack(pady=5)

        # 配置管理按钮
        config_frame = ttk.Frame(main_frame)
        config_frame.pack(fill=tk.X, pady=5)

        ttk.Button(config_frame, text="保存配置",
                   command=self.on_save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_frame, text="重置配置",
                   command=self.on_reset_config).pack(side=tk.LEFT, padx=5)

        # 热键设置
        hotkey_frame = ttk.LabelFrame(main_frame, text="热键设置", padding="10")
        hotkey_frame.pack(fill=tk.X, pady=5)

        ttk.Label(hotkey_frame, text="启动/停止热键:").grid(row=0, column=0, sticky=tk.W)
        self.hotkey_var = tk.StringVar(value=self.toggle_key.upper())
        ttk.Entry(hotkey_frame, textvariable=self.hotkey_var,
                  width=5).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(hotkey_frame, text="更新",
                   command=self.on_update_hotkey).grid(row=0, column=2, padx=5)

        # 区域设置
        area_frame = ttk.LabelFrame(main_frame, text="Hekili提示区域设置", padding="10")
        area_frame.pack(fill=tk.X, pady=5)

        # 坐标设置
        ttk.Label(area_frame, text="左:").grid(row=0, column=0, sticky=tk.W)
        self.left_var = tk.IntVar(value=self.config['hekili_box']['left'])
        ttk.Entry(area_frame, textvariable=self.left_var,
                  width=6).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(area_frame, text="上:").grid(row=0, column=2, padx=(10, 0), sticky=tk.W)
        self.top_var = tk.IntVar(value=self.config['hekili_box']['top'])
        ttk.Entry(area_frame, textvariable=self.top_var,
                  width=6).grid(row=0, column=3, sticky=tk.W)

        ttk.Label(area_frame, text="宽:").grid(row=1, column=0, sticky=tk.W)
        self.width_var = tk.IntVar(value=self.config['hekili_box']['width'])
        ttk.Entry(area_frame, textvariable=self.width_var,
                  width=6).grid(row=1, column=1, sticky=tk.W)

        ttk.Label(area_frame, text="高:").grid(row=1, column=2, padx=(10, 0), sticky=tk.W)
        self.height_var = tk.IntVar(value=self.config['hekili_box']['height'])
        ttk.Entry(area_frame, textvariable=self.height_var,
                  width=6).grid(row=1, column=3, sticky=tk.W)

        # 区域操作按钮
        ttk.Button(area_frame, text="测试区域",
                   command=self.on_test_area).grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.W)
        ttk.Button(area_frame, text="自动定位",
                   command=self.on_auto_detect).grid(row=2, column=2, columnspan=2, pady=5, sticky=tk.E)

        # 高级设置
        adv_frame = ttk.LabelFrame(main_frame, text="高级设置", padding="10")
        adv_frame.pack(fill=tk.X, pady=5)

        # 匹配阈值
        ttk.Label(adv_frame, text="匹配阈值 (0.7-0.95):").grid(row=0, column=0, sticky=tk.W)
        self.threshold_var = tk.DoubleVar(value=self.config['threshold'])
        ttk.Scale(adv_frame, from_=0.7, to=0.95, variable=self.threshold_var,
                  length=150).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(adv_frame, textvariable=self.threshold_var).grid(row=0, column=2, sticky=tk.W)

        # 技能延迟
        ttk.Label(adv_frame, text="技能延迟 (秒):").grid(row=1, column=0, sticky=tk.W)
        self.delay_var = tk.DoubleVar(value=self.config['skill_delay'])
        ttk.Scale(adv_frame, from_=0.1, to=1.0, variable=self.delay_var,
                  length=150).grid(row=1, column=1, sticky=tk.W)
        ttk.Label(adv_frame, textvariable=self.delay_var).grid(row=1, column=2, sticky=tk.W)

        # 控制按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text=f"启动 ({self.toggle_key.upper()})",
                                    command=self.on_toggle_bot, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(btn_frame, text="退出",
                   command=self.on_close, width=15).pack(side=tk.LEFT, padx=5)

        # 版本信息
        ttk.Label(main_frame, text="v2.2 | 稳定版",
                  font=('Arial', 8)).pack(side=tk.BOTTOM, pady=5)

    def start_hotkey_listener(self):
        """启动热键监听线程"""

        def listen():
            while self.hotkey_listener_active:
                if keyboard.is_pressed(self.toggle_key):
                    self.root.after(0, self.on_toggle_bot)
                    time.sleep(0.5)  # 防抖
                time.sleep(0.1)

        threading.Thread(target=listen, daemon=True).start()

    def on_save_config(self):
        """保存配置按钮事件"""
        if self.save_config():
            messagebox.showinfo("成功", "配置已保存")

    def on_reset_config(self):
        """重置配置按钮事件"""
        if messagebox.askyesno("确认", "确定要重置所有配置为默认值吗？"):
            self.config = self.default_config.copy()
            self.left_var.set(self.config['hekili_box']['left'])
            self.top_var.set(self.config['hekili_box']['top'])
            self.width_var.set(self.config['hekili_box']['width'])
            self.height_var.set(self.config['hekili_box']['height'])
            self.threshold_var.set(self.config['threshold'])
            self.delay_var.set(self.config['skill_delay'])
            self.hotkey_var.set(self.config['toggle_key'].upper())
            self.toggle_key = self.config['toggle_key']
            self.start_btn.config(text=f"启动 ({self.toggle_key.upper()})")

    def on_update_hotkey(self):
        """更新热键按钮事件"""
        new_key = self.hotkey_var.get().lower()
        if new_key and new_key != self.toggle_key:
            self.toggle_key = new_key
            self.start_btn.config(text=f"启动 ({new_key.upper()})")

    def on_test_area(self):
        """测试区域按钮事件"""
        try:
            screenshot = ImageGrab.grab(bbox=(
                self.left_var.get(),
                self.top_var.get(),
                self.left_var.get() + self.width_var.get(),
                self.top_var.get() + self.height_var.get()
            ))

            test_window = tk.Toplevel(self.root)
            test_window.title("区域测试")

            img_tk = ImageTk.PhotoImage(screenshot)
            tk.Label(test_window, image=img_tk).pack()
            img_tk.image = img_tk  # 保持引用

            ttk.Button(test_window, text="关闭",
                       command=test_window.destroy).pack(pady=5)
        except Exception as e:
            messagebox.showerror("错误", f"无法截取区域: {e}")

    def on_auto_detect(self):
        """自动定位按钮事件"""
        messagebox.showinfo("提示", "请切换到游戏窗口，确保Hekili提示可见，5秒后开始检测...")
        time.sleep(5)

        try:
            screenshot = np.array(ImageGrab.grab())
            gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

            # 简单数字区域检测
            _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in sorted(contours, key=cv2.contourArea, reverse=True)[:5]:
                x, y, w, h = cv2.boundingRect(cnt)
                if 30 < w < 100 and 30 < h < 100:  # 假设数字区域大小
                    self.left_var.set(x)
                    self.top_var.set(y)
                    self.width_var.set(w)
                    self.height_var.set(h)
                    messagebox.showinfo("成功", f"检测到区域: {x},{y} {w}x{h}")
                    return

            messagebox.showwarning("警告", "未能自动检测到区域")
        except Exception as e:
            messagebox.showerror("错误", f"自动检测失败: {e}")

    def on_toggle_bot(self):
        """切换运行状态"""
        if self.running:
            self.stop_bot()
        else:
            self.start_bot()

    def start_bot(self):
        """启动脚本"""
        if not self.running:
            # if not any(self.templates.values()):
            #     messagebox.showerror("错误", "没有有效的技能模板")
            #     return

            self.running = True
            self.status_var.set(f"状态: 运行中 (按{self.toggle_key.upper()}停止)")
            self.start_btn.config(text=f"停止 ({self.toggle_key.upper()})")

            # 更新当前配置
            self.config.update({
                'hekili_box': {
                    'left': self.left_var.get(),
                    'top': self.top_var.get(),
                    'width': self.width_var.get(),
                    'height': self.height_var.get()
                },
                'threshold': self.threshold_var.get(),
                'skill_delay': self.delay_var.get(),
                'toggle_key': self.toggle_key
            })

            threading.Thread(target=self.run_bot, daemon=True).start()

    def stop_bot(self):
        """停止脚本"""
        if self.running:
            self.running = False
            self.status_var.set("状态: 已停止")
            self.start_btn.config(text=f"启动 ({self.toggle_key.upper()})")

    def run_bot(self):
        """主运行逻辑"""
        last_skill_time = 0

        while self.running:
            try:
                current_time = time.time()

                # 捕获Hekili区域
                screenshot = ImageGrab.grab(bbox=(
                    self.config['hekili_box']['left'],
                    self.config['hekili_box']['top'],
                    self.config['hekili_box']['left'] + self.config['hekili_box']['width'],
                    self.config['hekili_box']['top'] + self.config['hekili_box']['height']
                ))
                gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

                # 检测技能
                skill_num = None
                max_val = 0

                for num, template in self.templates.items():
                    if template is None:
                        continue

                    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
                    _, val, _, _ = cv2.minMaxLoc(res)

                    if val > self.config['threshold'] and val > max_val:
                        max_val = val
                        skill_num = num

                # 释放技能
                if skill_num and (current_time - last_skill_time) > self.config['skill_delay']:
                    pyautogui.press(self.skill_keys[skill_num])
                    last_skill_time = current_time
                    time.sleep(0.1)

                time.sleep(0.05)

            except Exception as e:
                print(f"运行错误: {e}")
                time.sleep(1)

    def on_close(self):
        """关闭窗口事件"""
        self.hotkey_listener_active = False
        self.stop_bot()
        self.save_config()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap('icon.ico')
    except:
        pass

    app = HekiliAutoBot(root)
    root.mainloop()