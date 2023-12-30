import os
from unittest import result

import pandas as pd
from calculate import average_caculate, sample_chose, data_average_caculate
from calculate_ratio_light import process_images_and_calculate_ratios
# from calculate_ratio import process_images_and_calculate_ratios
# from calculate_ratio_seg import process_images_and_calculate_ratios

if __name__ == "__main__":
    # 指定要处理的图片目录
    # directory_path = "/home/sxwang/SOTAtest/test"
    # #directory_path_or = "/home/sxwang/SOTAtest/231215MightyOutput/20231215_172140641"
    # test_time_start = 1721
    # test_time_end = 1746
    # directory_path_or = "/home/sxwang/SOTAtest/sample"
    # test_time_start = 1450
    # test_time_end = 1451

    directory_path_or = "/home/sxwang/SOTAtest/231229MightyOutput/20231229_150659/20231229_152308991"

    test_time_start = 1523
    test_time_end = 1600
    test_time_start_1 = 1600
    test_time_end_1 = 1617
    directory_path = directory_path_or + "/raw_images"
    r = 15   # 按需更改
    n = 5   # 按需更改
    A = 100000 * test_time_start
    B = 100000 * test_time_end
    A11 = 100000 * test_time_start_1
    B11 = 100000 * test_time_end_1
    result_folder_path = os.path.join(directory_path_or, "result")
    if not os.path.exists(result_folder_path):
        os.makedirs(result_folder_path)
    # 调用函数处理图片并计算比例
    df = process_images_and_calculate_ratios(directory_path)
    df_all, df_dict, b1 = data_average_caculate(df, directory_path_or, A, B, A11, B11, r)
    sample_chose(df_all, df_dict, directory_path, directory_path_or, b1, n)

    print(df_all)

