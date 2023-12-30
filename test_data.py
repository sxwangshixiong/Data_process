import os
from time_monitoring import time_monitor


# 获取文件夹中的文件名列表
# directory_path = "/home/sxwang//SOTAtest/231215MightyOutput/20231215_172140641/raw"
# directory_path = "/home/sxwang//SOTAtest/231215MightyOutput/20231215_172140641/result_out/df_2_20231215_173249104"
# directory_path = "/home/sxwang//SOTAtest/231215MightyOutput/20231215_154026102/raw"
# directory_path = "/home/sxwang//SOTAtest/231219MightyOutput/20231219_154100/20231219_154141793/raw_images"
directory_path = "/home/sxwang//SOTAtest/231219MightyOutput/20231219_091139/20231219_091143700/raw"
# all_filenames = os.listdir(directory_path)
all_filenames = [filename for filename in os.listdir(directory_path) if filename.endswith('.bmp')]

filenames = all_filenames

# directory_path = "/home/sxwang/SOTAtest/231215MightyOutput/20231215_162334_labeled/labeled"
# all_filenames = os.listdir(directory_path)
# # 保留文件名末尾为'seg.png'的文件
# filenames = [filename for filename in all_filenames if filename.endswith('seg.png')]

# 调用函数处理文件
time_monitor(directory_path, filenames)
