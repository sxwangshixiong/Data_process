import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import seaborn as sns
import numpy as np

# 获取目录及其所有子目录下的所有.xlsx文件
# def get_files(dir_path):
#     files = []
#     for root, dirs, files_in_dir in os.walk(dir_path):
#         for file in files_in_dir:
#             if file.startswith('vdf') and file.endswith('.xlsx'):
#                 files.append(os.path.join(root, file))
#     return files


def get_files(dir_path):
    files = []
    for root, dirs, files_in_dir in os.walk(dir_path):
        for file in files_in_dir:
            if file.startswith('vdf') and file.endswith('.xlsx'):
                files.append(os.path.join(root, file))

    return files, len(files)


def draw_sum_bar_chart(files, dir_path, fontsize=10, figsize=(10, 6)):

        # Sort the files in increasing order of the number after 'df_'
    #files = sorted(files, key=lambda x: int(x.split('_')[1]) if x.split('_')[1].isdigit() else float('inf'))
    # 设置类别颜色
    colors = {
        'pcb': (152 / 255, 223 / 255, 138 / 255),
        'rubber': (196 / 255, 156 / 255, 148 / 255),
        'tube': (255 / 255, 152 / 255, 150 / 255),
        'wire': (197 / 255, 176 / 255, 213 / 255),
        'can': (255 / 255, 187 / 255, 120 / 255),
        'painted_metal': (174 / 255, 199 / 255, 232 / 255)
    }

    # 准备数据
    data = []
    total_wastes = []
    for i, file in enumerate(files, start=1):
        # 将Excel文件加载到pandas DataFrame中
        df = pd.read_excel(file)
        df.iloc[:, 1:21] = df.iloc[:, 1:21].apply(pd.to_numeric, errors='coerce')
        df.iloc[:, 1:21] = df.iloc[:, 1:21] - df.iloc[0, 1:21]

        dff = df
        dff.iloc[:, 1:21] = dff.iloc[:, 1:21].apply(pd.to_numeric, errors='coerce')
        dff.iloc[:, 1:21] = dff.iloc[:, 1:21].diff()

        print(dff)
        # 计算各类总数
        sums = dff[['pcb', 'rubber', 'tube', 'wire', 'can', 'painted_metal']].sum()
        data.append(sums)
        total_wastes.append(sums.sum())

    # 创建DataFrame
    df_total = pd.DataFrame(data, index=[os.path.basename(file)[:-5] for file in files])

    # 处理文件名，将df_2一行显示，20231215去掉，剩下173245321第二行显示
    df_total.index = [i.replace('_20231219_', ': ') for i in df_total.index]

    # 创建柱形图
    fig, ax = plt.subplots(figsize=figsize)
    df_total.plot(kind='bar', stacked=True, color=[colors[col] for col in df_total.columns], ax=ax, width=0.65)  # 设置宽度为0.8
    # plt.title('Quantity of waste detected by sensor during the 1-minute random sampling from: Test_20231215_172140641')
    plt.title('Quantity of waste detected by sensor during the 1-minute random sampling from: Test_20231219_154141793')
    plt.xlabel('Batch of random sampling close to average density')
    plt.ylabel('Waste quantity of each random sampling')
    plt.xticks(rotation=0)  # 横坐标横着写
    plt.ylim(0, 125)  # 设置y轴范围
    plt.legend(bbox_to_anchor=(0., 0.94, 1., .102), loc='lower left', ncol=6, mode="expand", borderaxespad=0.1)

    # 添加每一类的百分比和数量
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        ax.text(x+width/2,
                y+height/2,
                '{:.0f} ({:.2%})'.format(height, height/df_total.sum().sum()),  # 数量和比例加括号
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=fontsize)

    # 添加总废料数量
    for i, total_waste in enumerate(total_wastes):
        ax.text(i, total_waste+5, str(total_waste), color='black', ha='center')

    #plt.savefig(dir_path + "/Quantity of waste detected by sensor during the 1-minute random sampling from: Test_20231215_172140641.png")
    plt.savefig(dir_path + "/Quantity of waste detected by sensor during the 1-minute random sampling from: Test_20231219_154141793.png")
    plt.show()

def draw_text(ax, s, total_waste, total_wastes, i, counter):
    if i == counter:
        ax.text(i - 1, total_waste + 5, str(total_waste), color='black', ha='center')
        min_i = s * (i - 1)
        max_i = s * i
        t = 0
        single_waste = [ax.patches[j] for j in [i - 1, s + i - 1, 2 * s + i - 1, 3 * s + i - 1, 4 * s + i - 1, 5 * s + i - 1]]
        print("single_waste: ", single_waste)
        print("total_wastes: ", total_wastes)
        single_waste_sum = 0
        for p in single_waste:
            height = p.get_height()
            single_waste_sum += height

        for p in single_waste:
            width, height = p.get_width(), p.get_height()
            x, y = p.get_xy()
            ax.text(x + width / 2,
                    y + height / 2,
                    # '{:.0f} ({:.2%})'.format(height, height / total_wastes[t]),
                    '{:.0f} ({:.2%})'.format(height, height / single_waste_sum),
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=10)
        t += 1

def draw_sum_bar_chart_A(files, dir_path, fontsize=10, figsize=(10, 6)):
    colors = {
        'pcb': (152 / 255, 223 / 255, 138 / 255),
        'rubber': (196 / 255, 156 / 255, 148 / 255),
        'tube': (255 / 255, 152 / 255, 150 / 255),
        'wire': (197 / 255, 176 / 255, 213 / 255),
        'can': (255 / 255, 187 / 255, 120 / 255),
        'painted_metal': (174 / 255, 199 / 255, 232 / 255)
    }

    data = []
    total_wastes = []
    for i, file in enumerate(files, start=1):
        df = pd.read_excel(file)

        sums = df[['pcb', 'rubber', 'tube', 'wire', 'can', 'painted_metal']].sum()
        data.append(sums)
        total_wastes.append(sums.sum())

    df_total = pd.DataFrame(data, index=[os.path.basename(f)[:-5] for f in files])

    df_total.index = [i.replace('_20231219_', ': ') for i in df_total.index]
    df_total = df_total.apply(pd.to_numeric, errors='coerce')

    fig, ax = plt.subplots(figsize=figsize)
    df_total.plot(kind='bar', stacked=True, color=[colors[col] for col in df_total.columns], ax=ax, width=0.65)
    plt.title('Quantity of waste detected by sensor during the 1-minute random sampling from: Test_20231219_154141793')
    plt.xlabel('Batch of random sampling close to average density')
    plt.ylabel('Waste quantity of each random sampling')
    plt.xticks(rotation=0)
    plt.ylim(0, 125)
    plt.legend(bbox_to_anchor=(0., 0.94, 1., .102), loc='lower left', ncol=6, mode="expand", borderaxespad=0.1)

    counter = 1
    for df in range(df_number):
        for i, p in enumerate(ax.patches):
            total_waste = total_wastes[counter - 1]
            draw_text(ax, df_number, total_waste, total_wastes, i, counter)
            # print(total_waste)
            # print(i)
        counter += 1
        df += 1

        plt.savefig(dir_path + "/Quantity of waste detected by sensor during the 1-minute random sampling from: Test_20231219_154141793.png")
        plt.show()



# dir_path = '/home/sxwang/SOTAtest/231215MightyOutput/20231215_172140641/result_out'  # 目录路径
# dir_path = '/home/sxwang/SOTAtest/231215MightyOutput/20231215_154026102/result_out'  # 目录路径
# dir_path = '/home/sxwang/SOTAtest/231219MightyOutput/20231219_154100/20231219_154141793/result_out'
dir_path = '/home/sxwang/SOTAtest/231219MightyOutput/20231219_154100/20231219_154141793/result_out'
files, df_number = get_files(dir_path)
draw_sum_bar_chart(files, dir_path)

