import os
import pymysql
from os.path import join
import re
from os import walk

# 連接資料庫
def create_and_connect_database(conn, base_name):
    try:
        with conn.cursor() as cursor:
            # 創建資料庫
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {base_name}")
            print(f"資料庫 {base_name} 創建成功")

            # 連接到新創建的資料庫
            conn.select_db(base_name)
            print(f"已連接到資料庫 {base_name}")

            # 使用指定的資料庫
            cursor.execute(f"USE {base_name};")
            print(f"成功使用 {base_name} 資料庫")

    except pymysql.MySQLError as e:
        print(f"錯誤: {e}")


conn = pymysql.connect(host='127.0.0.1', user='root', password="abc123")
cursor = conn.cursor()

base_name = input("資料夾名稱: ")
file_name = "\\" + base_name
create_and_connect_database(conn, base_name)

# 檔案存在建立表格旗標 (0:表格不存在; 1:表格存在建立表格)
file_flag = 0
# 建立表格存在的列表
table_list = []

def count_files_in_directory(directory_path):
    # 檢查資料夾是否存在
    if not os.path.exists(directory_path):
        print(f"資料夾 {directory_path} 不存在。".encode('utf-8').decode('cp950'))
        return 0
    
    # 計算檔案數量
    file_count = sum(len(files) for _, _, files in os.walk(directory_path))
    return file_count

# 指定資料夾路徑 (引號內為大資料夾名稱)
directory_path = r"C:\test\SQL_final\pymysql1130618\pymysql\20240418buying_egg" + '\\' + base_name  

# 創建一個空列表來存儲文件的絕對路徑
file_list = []
# 遞迴列出所有檔案的絕對路徑
for root, dirs, files in os.walk(directory_path):
    for f in files:
        fullpath = os.path.join(root, f)
        file_list.append(fullpath)

# 定義提取數字的函數
def extract_number(file_path):
    # 使用正則表達式匹配並提取數字
    match = re.search(r'-(\d+)-1-1', file_path)
    return int(match.group(1)) if match else None

# 提取每個文件路徑中的數字，過濾掉 None 值
numbers = [extract_number(file_path) for file_path in file_list if extract_number(file_path) is not None]

# 找到最大的數字
if numbers:  
    max_number = 24
else:
    print("在文件路徑中未找到有效的數字。")

direction = 5

for k in range(1, max_number + 1):
    # 創建帶有多個反射列的表格
    title = []
    title.append(f"CREATE TABLE IF NOT EXISTS egg{k} (id INT AUTO_INCREMENT PRIMARY KEY,")
    title.append("Wavelength VARCHAR(20),")
    for d in range(1, direction + 1):
        title.append(f"Reflectance_{d} VARCHAR(20),")
    title[-1] = title[-1][:-1]  # 移除最後的逗號
    title.append(")")
    str_title = " ".join(title)
    cursor.execute(str_title)
    conn.commit()

    reflectance_data = [[] for _ in range(direction)]

    # 讀取每個方向的數據
    for j in range(1, direction + 1):
        # 需修改為檔案格式
        file_path = directory_path + file_name + "-" + str(k) + "-1-" + str(j) + ".sps"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
                file_flag = 1
                table_list.append(1)

                # 按行分割
                lines = file_content.splitlines()
                data = lines[26:]
                data = [item for s in data for item in s.split() if item]

                # 分離波長和反射值
                wavelength_list = data[::2]
                reflectance_list = data[1::2]

                reflectance_data[j - 1] = reflectance_list

        # 處理檔案未找到錯誤
        except FileNotFoundError:
            table_list.append(0)
            file_flag = 0
            print(f"檔案未找到: {file_path}")
        # 處理其他錯誤
        except Exception as e:
            print(f"讀取文件 {file_path} 時出錯: {e}")

    # 插入數據到資料庫
    if file_flag == 1:
        table_name = f"egg{str(k)}"
        columns = ["Wavelength"] + [f"Reflectance_{d}" for d in range(1, direction + 1)]
        str_insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

        # 收集所有數據
        data_sql_list = []
        for i in range(len(wavelength_list)):
            row = [wavelength_list[i]] + [reflectance_data[d][i] for d in range(direction)]
            data_sql_list.append(tuple(row))

        # 批量插入數據
        cursor.executemany(str_insert_sql, data_sql_list)
        conn.commit()
        print("數據插入成功。")

print('完成執行程式')

# 刪除不需要的表格
for i in range(0, len(table_list), direction):
    if table_list[i] == 0:
        drop = []
        drop.append('DROP TABLE egg' + str(int((i + direction) / direction)))
        str_drop = " ".join(drop)
        cursor.execute(str_drop)
        conn.commit()
