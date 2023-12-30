import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import seaborn as sns
import numpy as np

# Retrieve all .xlsx files from specified directory and its subdirectories
def get_files(dir_path, flag):
    if flag == 1:
        sign = 'df'
    else:
        sign = 'vdf'
    files = []
    for root, dirs, files_in_dir in os.walk(dir_path):
        for file in files_in_dir:
            if file.startswith(sign) and file.endswith('.xlsx'):
                files.append(os.path.join(root, file))

    return files, len(files)


def Frequency_reviews(files):
    for i, file in enumerate(files, start=1):
        # 读取Excel文件并加载到pandas DataFrame
        df = pd.read_excel(file)

        # 将第二列转换为时间格式
        df.iloc[:, 1] = df.iloc[:, 1].apply(lambda x: x[-13:-3].replace("_", ""))
        df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1], format='%H%M%S%f').dt.time
        start_time = df.iloc[1, 1]

        # 将'datetime.time'对象转换为午夜后的秒数
        df.iloc[:, 1] = df.iloc[:, 1].apply(lambda t: t.hour*3600 + t.minute*60 + t.second + t.microsecond/1e6)
        df.iloc[:, 1] = df.iloc[:, 1] - df.iloc[1, 1]

        # 新增第七类，该数值为前面六类的总和
        df['all_types_of_wastes'] = df[['pcb', 'rubber', 'tube', 'wire', 'can', 'painted_metal']].sum(axis=1)

        # 计算不同数量下的频次并转换为百分比
        frequency = df['all_types_of_wastes'].value_counts().reset_index().rename(columns={'index': 'Number of wastes', 'all_types_of_wastes': 'Frequency'})
        # print(frequency)
        frequency['Percentage'] = frequency['count'] / df.shape[0] * 100
        # Sort frequency DataFrame by 'Frequency' column in ascending order
        frequency = frequency.sort_values(by='Frequency')
        # print(frequency)
        # 绘制火柴图
        plt.figure(figsize=(10, 6))

        sns.barplot(x='count', y='Frequency', data=frequency, orient='h')

        # 在条形图上显示百分比
        for i in range(frequency.shape[0]):
            plt.text(frequency.iloc[i, 1]+1, i, f"{frequency.iloc[i, 2]:.2f}%", va='center')

        plt.xlabel('Frequency')
        plt.ylabel('Number of wastes')
        plt.title(f'Frequency of waste quantity in each sensor photograph: {os.path.basename(file)[:-5]}')  # Remove the suffix .xlsx in the title
        plt.xlim(0, 40)
        plt.ylim(-0.5, 10)

        # 保存图形到文件
        plt.savefig(dir_path + f"/Frequency of waste quantity in each sensor photograph: {os.path.basename(file)[:-5]}.png")
        # plt.show()
def Number_of_manual_reviews(files):
    for i, file in enumerate(files, start=1):
        df = pd.read_excel(file)

        df.iloc[:, 1] = df.iloc[:, 1].apply(lambda x: x[-13:-3].replace("_", ""))
        df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1], format='%H%M%S%f').dt.time
        start_time = df.iloc[1, 1]

        df.iloc[:, 1] = df.iloc[:, 1].apply(lambda t: t.hour*3600 + t.minute*60 + t.second + t.microsecond/1e6)
        df.iloc[:, 1] = df.iloc[:, 1] - df.iloc[1, 1]

        cols = ['pcb', 'rubber', 'tube', 'wire', 'can', 'painted_metal']
        plt.figure(figsize=(10, 6))
        for col in cols:
            if (df[col] != 0).any():
                plt.plot(df.iloc[:, 1], df[col], '.', label=col)

        df['all_types_of_wastes'] = df[cols].sum(axis=1)
        plt.plot(df.iloc[:, 1], df['all_types_of_wastes'], '.', color=(100/255, 100/255, 100/255), label='all_types_of_wastes')
        plt.plot(df.iloc[:, 1], df['all_types_of_wastes'], color=(150/255, 150/255, 150/255), linewidth=1)

        plt.xlabel(f'1 min after random sampling time: {start_time}')
        plt.ylabel('Number of wastes')
        plt.xlim(0, 60)
        plt.ylim(0, 10)
        plt.title(f'Number of wastes per sensor photograph (per image): {os.path.basename(file)[:-5]}')
        plt.legend()

        plt.savefig(dir_path + f"/Number of wastes per sensor photograph (per image): {os.path.basename(file)[:-5]}.png")

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

def draw_sum_bar_chart(files, dir_path, figsize, test_name, flag):
    colors = {
        'pcb': (152 / 255, 223 / 255, 138 / 255),
        'rubber': (196 / 255, 156 / 255, 148 / 255),
        'tube': (255 / 255, 152 / 255, 150 / 255),
        'wire': (197 / 255, 176 / 255, 213 / 255),
        'can': (255 / 255, 187 / 255, 120 / 255),
        'painted_metal': (174 / 255, 199 / 255, 232 / 255)
    }
    if flag == 1:
        data = []
        total_wastes = []
        for i, file in enumerate(files, start=1):
            df = pd.read_excel(file)

            sums = df[['pcb', 'rubber', 'tube', 'wire', 'can', 'painted_metal']].sum()
            data.append(sums)
            total_wastes.append(sums.sum())
    else:
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

    df_total = pd.DataFrame(data, index=[os.path.basename(f)[:-5] for f in files])

    df_total.index = [i.replace('_' + str(test_date) + '_', ': ') for i in df_total.index]
    df_total = df_total.apply(pd.to_numeric, errors='coerce')

    fig, ax = plt.subplots(figsize=figsize)
    df_total.plot(kind='bar', stacked=True, color=[colors[col] for col in df_total.columns], ax=ax, width=0.65)
    if flag == 1:
        plt.title('Quantity of waste from the random sampling at 1 minute from: ' + test_name)
        plt.xlabel('Batch of random sampling close to average density')
        plt.ylabel('Waste quantity of each random sampling')
    else:
        plt.title('Quantity of waste detected by sensor during the 1-minute random sampling from: ' + test_name)
        plt.xlabel('Batch of random sampling close to average density')
        plt.ylabel('Waste quantity of each random sampling')

    plt.xticks(rotation=0)
    plt.ylim(0, value_max)
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

    plt.savefig(dir_path + "/Quantity of waste from the random sampling at 1 minute from: " + test_name + ".png")
    plt.show()

def draw_sum_bar_chart_for_sensor(dir_path, figsize, test_name, flag):
    files, df_number = get_files(dir_path, flag)
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
    df_total.index = [i.replace('_' + str(test_date) + '_', ': ') for i in df_total.index]

    # 创建柱形图
    fig, ax = plt.subplots(figsize=figsize)
    df_total.plot(kind='bar', stacked=True, color=[colors[col] for col in df_total.columns], ax=ax,
                  width=0.65)  # 设置宽度
    plt.title('Quantity of waste detected by sensor during the 1-minute random sampling from: ' + test_name)
    plt.xlabel('Batch of random sampling close to average density')
    plt.ylabel('Waste quantity of each random sampling')
    plt.xticks(rotation=0)  # 横坐标横写
    plt.ylim(0, value_max)  # 设置y轴范围
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

    plt.savefig(dir_path + "/Quantity of waste detected by sensor during the 1-minute random sampling from: " + test_name + ".png")
    plt.show()


dir_path = '/home/sxwang/SOTAtest/231219MightyOutput/20231219_133013/20231219_135601721/result_out'
test_name = 'Test_' + '20231219_135601721'
test_date = 20231219
flag = 1
value_max = 125
files, df_number = get_files(dir_path, flag)

print("files: ", files)

draw_sum_bar_chart(files, dir_path, (10, 6), test_name, 1)
draw_sum_bar_chart_for_sensor(dir_path, (10, 6), test_name, 0)
Frequency_reviews(files)
Number_of_manual_reviews(files)
