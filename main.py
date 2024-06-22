from Call_data_library import query_1_2
import matplotlib.pyplot as plt

# 查詢引索
# ======================================================================================================================
# 定義日期列表
date = ['20240420', '20240425', '20240427']  
# 定義日期顏色列表
date_color = ['r', 'b', 'g']  
# 定義顏色變數
color = 'white'  
# 定義蛋序列號
egg_serial = 'egg1'
# 定義方向列表
direction = ['Reflectance_1', 'Reflectance_2', 'Reflectance_3', 'Reflectance_4', 'Reflectance_5']  
# 定義方向形狀列表
direction_shape = ['', '.', '*', '^', 's']  
# 定義波長列表
wavelength = ['380.00', '780.00']  

# 遍歷日期列表
for j in range(len(date)):
    # 遍歷方向列表
    for i in range(len(direction)):
        # 調用 query_1_2 函數並返回波長和反射值
        [w, v] = query_1_2(date[j], color, egg_serial, direction[i], wavelength)
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








