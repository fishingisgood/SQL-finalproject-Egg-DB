from Call_data_library import query_1_2
import tkinter as tk
from tkinter import ttk
from tkinter import font
import matplotlib.pyplot as plt

# 初始數據
date = ['20240420', '20240425', '20240427']
date_color = ['r', 'b', 'g']
color = 'white'
egg_serial = 'egg1'
direction = ['Reflectance_1', 'Reflectance_2', 'Reflectance_3', 'Reflectance_4', 'Reflectance_5']
direction_shape = ['', '.', '*', '^', 's']
wavelength = ['380.00', '780.00']



def update_values():
    global date, date_color, color, egg_serial, direction, direction_shape, wavelength

    date = date_entry.get().split(", ")
    date_color = date_color_entry.get().split(", ")
    color = color_entry.get()
    egg_serial = egg_serial_entry.get()
    direction = direction_entry.get().split(", ")
    direction_shape = direction_shape_entry.get().split(", ")
    wavelength = wavelength_entry.get().split(", ")
    
    tk.messagebox.showinfo("更新完成", "數據已更新")
    display_values()

def display_values():
    output = f"""
    日期列表: {date}
    日期顏色列表: {date_color}
    顏色變數: {color}
    蛋序列號: {egg_serial}
    方向列表: {direction}
    方向形狀列表: {direction_shape}
    波長列表: {wavelength}
    """
    tk.messagebox.showinfo("當前數據", output)

def plot_graph():
    plt.figure()

    # 遍歷日期列表
    for j in range(len(date)):
        # 遍歷方向列表
        for i in range(len(direction)):
            # 調用 query_1_2 函數並返回波長和反射值
            w, v = query_1_2(date[j], color, egg_serial, direction[i], wavelength)
            # 將波長轉換為浮點數
            w = [float(k) for k in w]
            # 將反射值轉換為浮點數
            v = [float(z) for z in v]
            # 如果是每個日期的第一條線，添加標籤
            if i == 0:  
                plt.plot(w, v, color=date_color[j], marker=direction_shape[i], label=f'{date[j]}')
            else:
                plt.plot(w, v, color=date_color[j], marker=direction_shape[i])

    # 設置 x 軸標籤
    plt.xlabel('wavelength')
    # 設置 y 軸標籤
    plt.ylabel('reflectance')
    # 設置圖表標題
    plt.title(egg_serial + ' wavelength to reflectance')

    # 顯示圖例
    plt.legend()

    # 顯示圖表
    plt.show()

# 建立主視窗
root = tk.Tk()
root.title("數據修改工具")

# 設置字體
custom_font = font.Font(family="標楷體", size=16, weight="bold")

# 日期 Frame
date_frame = tk.Frame(root)
date_frame.pack(pady=10)
tk.Label(date_frame, text="日期列表 (用逗號分隔):", font=custom_font).pack(side=tk.LEFT)
date_entry = tk.Entry(date_frame, width=50)
date_entry.pack(side=tk.LEFT)
date_entry.insert(0, ", ".join(date))

# 日期顏色 Frame
date_color_frame = tk.Frame(root)
date_color_frame.pack(pady=10)
tk.Label(date_color_frame, text="日期顏色列表 (用逗號分隔):", font=custom_font).pack(side=tk.LEFT)
date_color_entry = tk.Entry(date_color_frame, width=50)
date_color_entry.pack(side=tk.LEFT)
date_color_entry.insert(0, ", ".join(date_color))

# 顏色變數 Frame
color_frame = tk.Frame(root)
color_frame.pack(pady=10)
tk.Label(color_frame, text="顏色變數:", font=custom_font).pack(side=tk.LEFT)
color_entry = tk.Entry(color_frame, width=50)
color_entry.pack(side=tk.LEFT)
color_entry.insert(0, color)

# 蛋序列號 Frame
egg_serial_frame = tk.Frame(root)
egg_serial_frame.pack(pady=10)
tk.Label(egg_serial_frame, text="蛋序列號:", font=custom_font).pack(side=tk.LEFT)
egg_serial_entry = tk.Entry(egg_serial_frame, width=50)
egg_serial_entry.pack(side=tk.LEFT)
egg_serial_entry.insert(0, egg_serial)

# 方向列表 Frame
direction_frame = tk.Frame(root)
direction_frame.pack(pady=10)
tk.Label(direction_frame, text="方向列表 (用逗號分隔):", font=custom_font).pack(side=tk.LEFT)
direction_entry = tk.Entry(direction_frame, width=50)
direction_entry.pack(side=tk.LEFT)
direction_entry.insert(0, ", ".join(direction))

# 方向形狀列表 Frame
direction_shape_frame = tk.Frame(root)
direction_shape_frame.pack(pady=10)
tk.Label(direction_shape_frame, text="方向形狀列表 (用逗號分隔):", font=custom_font).pack(side=tk.LEFT)
direction_shape_entry = tk.Entry(direction_shape_frame, width=50)
direction_shape_entry.pack(side=tk.LEFT)
direction_shape_entry.insert(0, ", ".join(direction_shape))

# 波長列表 Frame
wavelength_frame = tk.Frame(root)
wavelength_frame.pack(pady=10)
tk.Label(wavelength_frame, text="波長列表 (用逗號分隔):", font=custom_font).pack(side=tk.LEFT)
wavelength_entry = tk.Entry(wavelength_frame, width=50)
wavelength_entry.pack(side=tk.LEFT)
wavelength_entry.insert(0, ", ".join(wavelength))

# 建立按鈕
update_button = tk.Button(root, text="修改數據", font=custom_font, command=update_values)
update_button.pack(pady=10)

display_button = tk.Button(root, text="顯示當前數據", font=custom_font, command=display_values)
display_button.pack(pady=10)

plot_button = tk.Button(root, text="顯示圖表", font=custom_font, command=plot_graph)
plot_button.pack(pady=10)

# 運行主迴圈
root.mainloop()
