import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cv2
import numpy as np
import pyautogui
import mss
import threading
import time
import json
import os


class EnhancedFishingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("魔兽世界WLK智能钓鱼 v3.0")

        # 初始化参数
        self.config = {
            "roi": {"left": 0, "top": 0, "width": 300, "height": 300},
            "threshold": 30,
            "sensitivity": 400,
            "cast_key": "1",
            "delay": 3.5,
            "templates": {
                "day": "float_day.png",
                "night": "float_night.png"
            }
        }
        self.load_config()

        # 状态控制
        self.running = False
        self.debug_mode = False
        self.current_template = "day"

        # 初始化GUI
        self.create_interface()

        # 初始化图像处理
        self.sct = mss.mss()
        self.prev_frame = None
        self.debug_window = None

        # 绑定事件
        self.root.protocol("WM_DELETE_WINDOW", self.safe_shutdown)

    def create_interface(self):
        """创建图形用户界面"""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板")
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.btn_start = ttk.Button(control_frame, text="开始钓鱼", command=self.start_cycle)
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_stop = ttk.Button(control_frame, text="停止", command=self.stop_cycle, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        # 参数配置
        config_frame = ttk.LabelFrame(main_frame, text="智能配置")
        config_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(config_frame, text="抛竿按键:").grid(row=0, column=0, sticky="w")
        self.entry_cast_key = ttk.Entry(config_frame, width=5)
        self.entry_cast_key.insert(0, self.config["cast_key"])
        self.entry_cast_key.grid(row=0, column=1)

        ttk.Label(config_frame, text="灵敏度 (100-2000):").grid(row=1, column=0, sticky="w")
        self.scale_sens = ttk.Scale(config_frame, from_=100, to=2000, value=self.config["sensitivity"])
        self.scale_sens.grid(row=1, column=1, sticky="ew")

        ttk.Label(config_frame, text="响应延迟 (秒):").grid(row=2, column=0, sticky="w")
        self.entry_delay = ttk.Entry(config_frame, width=5)
        self.entry_delay.insert(0, str(self.config["delay"]))
        self.entry_delay.grid(row=2, column=1)

        # 高级功能
        advance_frame = ttk.LabelFrame(main_frame, text="高级功能")
        advance_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Button(advance_frame, text="手动设置区域", command=self.manual_roi).pack(side=tk.LEFT, padx=2)
        ttk.Button(advance_frame, text="智能校准", command=self.smart_calibrate).pack(side=tk.LEFT, padx=2)
        ttk.Checkbutton(advance_frame, text="调试模式", command=self.toggle_debug).pack(side=tk.LEFT, padx=2)

        # 状态显示
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, sticky="ew")
        self.update_status("就绪")

    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(f"状态: {message}")
        self.root.update()

    def start_cycle(self):
        """启动钓鱼循环"""
        self.running = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.update_config()

        threading.Thread(target=self.fishing_processor, daemon=True).start()

    def stop_cycle(self):
        """停止钓鱼循环"""
        self.running = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.update_status("已停止")

    def fishing_processor(self):
        """钓鱼主循环"""
        while self.running:
            try:
                self.cast_fishing()
                if self.wait_for_bite():
                    self.reel_fish()
                time.sleep(1)
            except Exception as e:
                self.update_status(f"错误: {str(e)}")
                break

    def cast_fishing(self):
        """执行抛竿动作"""
        pyautogui.press(self.config["cast_key"])
        self.update_status("抛竿中...")
        time.sleep(2 + self.config["delay"])

    def wait_for_bite(self):
        """等待鱼汛的核心检测逻辑"""
        self.update_status("检测鱼汛中...")
        start_time = time.time()

        with self.sct as sct:
            while self.running and (time.time() - start_time < 60):
                frame = np.array(sct.grab(self.config["roi"]))

                # 环境自适应
                brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
                self.current_template = "night" if brightness < 50 else "day"

                # 双模式检测
                if self.detect_movement(frame) or self.detect_template(frame):
                    return True

                if self.debug_mode:
                    self.show_debug_frame(frame)

                time.sleep(0.1)
        return False

    def detect_movement(self, frame):
        """基于运动的检测方法"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_frame is None:
            self.prev_frame = gray
            return False

        diff = cv2.absdiff(gray, self.prev_frame)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) > self.config["sensitivity"]:
                self.prev_frame = None
                return True
        self.prev_frame = gray
        return False

    def detect_template(self, frame):
        """基于模板匹配的检测方法"""
        try:
            template = cv2.imread(self.config["templates"][self.current_template], cv2.IMREAD_GRAYSCALE)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)

            if max_val > 0.8:
                return True
        except Exception as e:
            self.update_status(f"模板错误: {str(e)}")
        return False

    def reel_fish(self):
        """执行收竿动作"""
        self.update_status("检测到鱼汛！收竿中...")
        pyautogui.rightClick()
        time.sleep(1.5)

    def manual_roi(self):
        """手动设置检测区域"""
        self.update_status("手动模式：输入坐标(x,y,width,height)")
        try:
            roi_str = simpledialog.askstring("设置区域", "请输入坐标:")
            if roi_str:
                x, y, w, h = map(int, roi_str.split(','))
                self.config["roi"].update({"left": x, "top": y, "width": w, "height": h})
                self.save_config()
        except Exception as e:
            messagebox.showerror("错误", f"无效输入: {str(e)}")

    def smart_calibrate(self):
        """智能校准检测区域"""
        self.update_status("智能校准中...")
        try:
            # 优先使用模板匹配
            template = cv2.imread(self.config["templates"][self.current_template], cv2.IMREAD_GRAYSCALE)
            screenshot = pyautogui.screenshot()
            gray_screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

            res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            if max_val > 0.7:
                x, y = max_loc
                w, h = template.shape[::-1]
                self.config["roi"].update({
                    "left": x - 20,
                    "top": y - 20,
                    "width": w + 40,
                    "height": h + 40
                })
                self.save_config()
                self.update_status(f"校准成功：{self.config['roi']}")
                return

            # 备用边缘检测方案
            edges = cv2.Canny(gray_screen, 50, 150)
            circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20,
                                       param1=50, param2=30, minRadius=10, maxRadius=50)

            if circles is not None:
                x, y, r = np.round(circles).astype("int")
                self.config["roi"].update({
                    "left": x - r * 2,
                    "top": y - r * 2,
                    "width": r * 4,
                    "height": r * 4
                })
                self.save_config()
                self.update_status("边缘校准成功")
            else:
                messagebox.showwarning("警告", "校准失败，请尝试手动设置")

        except Exception as e:
            messagebox.showerror("错误", f"校准失败: {str(e)}")

    def toggle_debug(self):
        """切换调试模式"""
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.update_status("调试模式已启用")
        else:
            cv2.destroyAllWindows()

    def show_debug_frame(self, frame):
        """显示调试窗口"""
        debug_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        debug_img = cv2.resize(debug_img, (400, 400))

        if self.debug_window is None:
            cv2.namedWindow("Debug Preview")

        cv2.imshow("Debug Preview", debug_img)
        cv2.waitKey(1)

    def update_config(self):
        """更新配置参数"""
        self.config.update({
            "cast_key": self.entry_cast_key.get(),
            "sensitivity": self.scale_sens.get(),
            "delay": float(self.entry_delay.get())
        })
        self.save_config()

    def save_config(self):
        """保存配置到文件"""
        with open('fishing_config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def load_config(self):
        """从文件加载配置"""
        if os.path.exists('fishing_config.json'):
            with open('fishing_config.json', 'r') as f:
                self.config.update(json.load(f))

    def safe_shutdown(self):
        """安全关闭程序"""
        self.stop_cycle()
        self.save_config()
        cv2.destroyAllWindows()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedFishingApp(root)
    root.mainloop()
