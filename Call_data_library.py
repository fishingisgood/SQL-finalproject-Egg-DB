import pymysql

def query_1_2(date, color, egg_serial, direction, wavelength):
    # 創建連接參數
    # ======================================================================================================================
    sqlhost = '127.0.0.1'  # SQL 主機地址
    sqlport = 3306  # SQL 連接埠
    sqluser = 'root'  # SQL 使用者名稱
    sqlpw = 'abc123'  # SQL 使用者密碼
    sqlname = date + color  # SQL 資料庫名稱，根據日期和顏色組合

    # 建立資料庫連接
    conn = pymysql.connect(
        host=sqlhost, port=sqlport,
        user=sqluser, password=sqlpw, database=sqlname
    )
    cursor = conn.cursor()  # 創建游標對象

    # 如果波長是 'all'
    if wavelength == 'all':
        # 查詢特定列的值和均值
        # ==========================================================================================
        select1 = "SELECT "                                     # 選擇
        select2 = direction                                     # 方向
        select3 = " FROM "                                      # 從
        select4 = egg_serial                                    # 蛋序列號
        final_select = select1 + select2 + select3 + select4    # 最終選擇語句

        cursor.execute(final_select)                            # 執行查詢
        results = cursor.fetchall()                             # 獲取所有結果

        float_values = []  # 浮點數值列表
        for row in results:
            float_value = float(row[0])  # 將結果轉換為浮點數
            float_values.append(float_value)  # 添加到列表中
        float_values = [float(row[0][0]) for row in float_values]  # 再次轉換為浮點數

        return float_values  # 返回浮點數值列表

    # 如果波長是單個浮點數
    elif isinstance(wavelength, float):
        # 查詢特定列的值和均值
        # ======================================================================================================================
        select1 = "SELECT "                                             # 選擇
        select2 = direction                                             # 方向
        select3 = " FROM "                                              # 從
        select4 = egg_serial                                            # 蛋序列號
        select5 = " WHERE Wavelength = %s"                              # 波長等於
        final_select = select1 + select2 + select3 + select4 + select5  # 最終選擇語句

        cursor.execute(final_select, wavelength)  # 執行查詢
        results = cursor.fetchall()  # 獲取所有結果

        results = float(results[0][0])  # 將結果轉換為浮點數

        return results  # 返回浮點數結果

    # 如果波長是多個值的列表
    elif isinstance(wavelength, list):
        select1 = "SELECT "                                     # 選擇
        select2 = direction                                     # 方向
        select3 = " FROM "                                      # 從
        select4 = egg_serial                                    # 蛋序列號
        select5 = " WHERE Wavelength BETWEEN %s"                # 波長介於
        select6 = " AND "                                       # 並且
        select7 = "%s"                                          # 另一個波長值
        final_select = select1 + select2 + select3 + select4 + select5 + select6 + select7  # 最終選擇語句

        select8 = "Wavelength"  # 波長列
        wavelength_select = select1 + select8 + select3 + select4 + select5 + select6 + select7  # 波長選擇語句
        cursor.execute(wavelength_select, wavelength)  # 執行波長查詢
        w_results = cursor.fetchall()  # 獲取波長結果
        w_results = [row[0] for row in w_results]  # 提取波長值

        cursor.execute(final_select, wavelength)  # 執行查詢
        results = cursor.fetchall()  # 獲取所有結果
        results = [row[0] for row in results]  # 提取結果值

        return [w_results, results]  # 返回波長值和結果值的列表

