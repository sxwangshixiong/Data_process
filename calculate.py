import pandas as pd
import os
import shutil
import numpy as np

from random_sampling import sort_and_filter, split_df


def sample_chose(df_all, df_dict, directory_path, directory_path_or, b1, n, key=None):
    all_avg_object_ratio = round(df_all['Average object ratio'].mean(), 3)
    all_avg_contour_ratio = round(df_all['Average contour ratio'].mean(), 3)
    all_avg_watershed_ratio = round(df_all['Average watershed ratio'].mean(), 3)
    #all_avg_avg_ratio = round(df_all['Average of averages ratio'].mean(), 3)
    all_avg_avg_ratio = 0.3 * all_avg_object_ratio + 0.4 * all_avg_contour_ratio + 0.3 * all_avg_watershed_ratio
    # 获取最接近all_avg_avg_ratio的n行
    df_all['deviation'] = abs(df_all['Average of averages ratio'] - all_avg_avg_ratio)
    df_all['deviation'] = pd.to_numeric(df_all['deviation'], errors='coerce')
    closest_n = df_all.nsmallest(n, 'deviation')
    print(closest_n)
    # 提取满足条件的filename
    selected_filenames = closest_n['filename'].tolist()
    print(selected_filenames)
    for key in selected_filenames:
        df_read = pd.read_csv(directory_path_or + "/result/output_" + str(key) + ".csv")
        selected_filenames = df_read['filename']
        print(selected_filenames)
        # 创建新的文件夹
        name = min(selected_filenames)
        new_folder_path = os.path.join(directory_path_or + "/result", str(key) + "_" + str(name))
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # 在directory_path下复制满足提取的filename的bmp文件
        for filename in selected_filenames:
            bmp_filename = filename + 'T.jpg'
            source_path = os.path.join(directory_path, bmp_filename)
            # 复制文件
            dst_path = os.path.join(new_folder_path, bmp_filename)
            shutil.copyfile(source_path, dst_path)


def average_caculate(df, key):
    # 计算并打印平均比例
    ratio_k = 1.2
    avg_object_ratio = ratio_k * round(df['object_ratio'].mean(), 3)
    avg_contour_ratio = ratio_k * round(df['contour_ratio'].mean(), 3)
    avg_watershed_ratio = ratio_k * round(df['watershed_ratio'].mean(), 3)
    avg_avg_ratio = 0.3 * avg_object_ratio + 0.4 * avg_contour_ratio + 0.3 * avg_watershed_ratio
    #avg_avg_ratio = ratio_k * round(df['avg_ratio'].mean(), 3)

    print('Average object ratio: ', avg_object_ratio, '%')
    print('Average contour ratio: ', avg_contour_ratio, '%')
    print('Average watershed ratio: ', avg_watershed_ratio, '%')
    print('Average of averages ratio: ', avg_avg_ratio, '%')


    return df, avg_object_ratio, avg_contour_ratio, avg_watershed_ratio, avg_avg_ratio

def data_average_caculate(df, directory_path, A, B, A11, B11, r):
    average_caculate(df, 0)
    df.to_excel(directory_path + "/result/output.xlsx")
    df = sort_and_filter(df, A, B11)
    df.to_excel(directory_path + "/result/output1.xlsx")
    df_dict, b1 = split_df(df, A, B, A11, B11, r)
    df_all = pd.DataFrame(
        columns=['filename', 'start time', 'Average object ratio', 'Average contour ratio', 'Average watershed ratio',
                 'Average of averages ratio'])
    for key, value in df_dict.items():
        i = str(key)[-1:]
        print(i)
        print("yes")
        print(b1)
        start_time = b1[int(i) - 1]
        print(start_time)
        print(key, ':', value, '\\n')
        df_dict[key].to_csv(directory_path + "/result/output_" + str(key) + ".csv")
        df, avg_object_ratio, avg_contour_ratio, avg_watershed_ratio, avg_avg_ratio = average_caculate(df_dict[key], key)
        df_all = pd.concat([df_all, pd.DataFrame([{'filename': key, 'start time': start_time, 'Average object ratio':
            avg_object_ratio, 'Average contour ratio': avg_contour_ratio, 'Average watershed ratio':
            avg_watershed_ratio, 'Average of averages ratio': avg_avg_ratio}])], ignore_index=True)

    df_all.to_excel(directory_path + "/result/output_All.xlsx")
    return df_all, df_dict, b1

