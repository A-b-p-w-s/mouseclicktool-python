import tkinter as tk
import pyautogui
import threading
import keyboard
import random
from tkinter import messagebox

# 全局变量，用于控制连点
clicking = False
click_interval = 1  # 默认连点间隔时间，单位为秒
offset_x = 5  # 水平方向偏移范围
offset_y = 5  # 垂直方向偏移范围
offset_button = False  # 是否添加随机时间延迟
random_delay = False  # 是否添加随机时间延迟
random_delay_range = 2  # 随机时间延迟范围，单位为秒

def start_clicking():
    global clicking, click_interval, random_delay, random_delay_range,offset_x,offset_y,offset_button
    clicking = True
    # 获取文本框中的连点间隔时间
    try:
        interval = float(interval_entry.get())
        if interval <= 0:
            raise ValueError
        click_interval = interval
        random_delay = random_delay_var.get()
        # 获取随机时间延迟范围
        if random_delay_var.get():
            random_delay_range = float(random_delay_entry.get())
            if random_delay_range <= 0:
                raise ValueError
        offset_button = offset_button_var.get()
        # 获取随机偏移量
        if offset_button_var.get():
            offset_x = int(offset_button_entry.get())
            offset_y = int(offset_button_entry.get())
            if offset_x <= 0 or offset_y <= 0:
                raise ValueError
    except ValueError:
        messagebox.showerror("输入错误", "请输入一个大于0的数字")
        return
    # 使用线程避免阻塞GUI
    threading.Thread(target=auto_click).start()

def stop_clicking():
    global clicking
    clicking = False

def auto_click():
    # 获取当前鼠标位置
    x, y = pyautogui.position()
    while clicking:
        # 生成随机偏移量
        dx = random.randint(-offset_x, offset_x)
        dy = random.randint(-offset_y, offset_y)
        if offset_button:
            # 移动鼠标到偏移后的位置
            pyautogui.moveTo(x + dx, y + dy, duration=0.25)
        # 模拟鼠标点击
        pyautogui.click()
        # 如果启用随机时间延迟，则添加随机延迟
        if random_delay:
            pyautogui.sleep(random.uniform(0, random_delay_range))
        # 按照用户设置的间隔时间进行点击
        pyautogui.sleep(click_interval)

def on_key_event(event):
    if event.name == 'esc':
        stop_clicking()
    elif event.name == 'f10' and event.event_type == 'down':
        start_clicking()

# 注册键盘事件
keyboard.hook(on_key_event)

# 创建主窗口
root = tk.Tk()
root.title("鼠标连点器")
root.geometry("300x200")

# 创建一个Frame容器
click_delay_frame = tk.Frame(root)
click_delay_frame.pack(pady=5)
# 创建标签
interval_label = tk.Label(click_delay_frame, text="连点间隔时间（秒）：")
interval_label.pack(side=tk.LEFT,pady=5)
# 创建文本框
interval_entry = tk.Entry(click_delay_frame, width=20)
interval_entry.pack(side=tk.LEFT,pady=5)
interval_entry.insert(0, "1")  # 默认值

# 创建一个Frame容器
random_delay_frame = tk.Frame(root)
random_delay_frame.pack(pady=5)
# 创建复选框
random_delay_var = tk.BooleanVar()
random_delay_checkbox = tk.Checkbutton(random_delay_frame, text="添加随机时间延迟（秒）:", variable=random_delay_var)
random_delay_checkbox.pack(side=tk.LEFT, padx=5)
# 创建随机时间延迟范围文本框
random_delay_entry = tk.Entry(random_delay_frame, width=10)
random_delay_entry.pack(side=tk.LEFT, padx=5)
random_delay_entry.insert(0, "2")  # 默认值
random_delay_var.set(True)  # 默认勾选


# 创建一个Frame容器
offset_button_frame = tk.Frame(root)
offset_button_frame.pack(pady=5)
# 创建复选框
offset_button_var = tk.BooleanVar()
offset_button_checkbox = tk.Checkbutton(offset_button_frame, text="添加鼠标随机偏移量（像素点）:", variable=offset_button_var)
offset_button_checkbox.pack(side=tk.LEFT, padx=5)
# 创建偏移文本框
offset_button_entry = tk.Entry(offset_button_frame, width=10)
offset_button_entry.pack(side=tk.LEFT, padx=5)
offset_button_entry.insert(0, "5")  # 默认值
offset_button_var.set(True)  # 默认勾选


# 创建一个Frame容器
end_button_frame = tk.Frame(root)
end_button_frame.pack(pady=5)
# 创建开始按钮
start_button = tk.Button(end_button_frame, text="开始连点 (Alt+F10)", command=start_clicking)
start_button.pack(side=tk.LEFT,padx=20,pady=10)

# 创建结束按钮
stop_button = tk.Button(end_button_frame, text="结束连点 (Esc)", command=stop_clicking)
stop_button.pack(side=tk.LEFT,padx=20,pady=10)

# 进入主事件循环
root.mainloop()