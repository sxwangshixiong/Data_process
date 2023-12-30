import os
from category_statistics import category_statistics
from time_monitoring import time_monitor


# 获取文件夹中的文件名列表
directory_path = "/home/sxwang//SOTAtest/231229MightyOutput/20231229_150659/20231229_152308991/result_out/df_5_20231229_161511211"
v = 0.35

# 调用函数处理文件
if __name__ == "__main__":
    all_filenames = [filename for filename in os.listdir(directory_path) if filename.endswith('T.jpg')]
    filenames = all_filenames
    average_difference = time_monitor(directory_path, filenames)
    average_difference = 0.001 * average_difference
    image_range = 720 * (1 - (average_difference * v) / 0.435)
    category_statistics(directory_path, int(image_range))
