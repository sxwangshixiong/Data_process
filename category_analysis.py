import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import seaborn as sns
import numpy as np

# Retrieve all .xlsx files from specified directory and its subdirectories
def get_files(dir_path):
    files = []
    for root, dirs, files_in_dir in os.walk(dir_path):
        for file in files_in_dir:
            if file.startswith('df') and file.endswith('.xlsx'):
                files.append(os.path.join(root, file))

    return files

dir_path = '/home/sxwang/SOTAtest/231219MightyOutput/20231219_154100/20231219_154141793/result_out'
files = get_files(dir_path)
print("files: ", files)

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
        print(frequency)
        frequency['Percentage'] = frequency['count'] / df.shape[0] * 100
        # Sort frequency DataFrame by 'Frequency' column in ascending order
        frequency = frequency.sort_values(by='Frequency')
        print(frequency)
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

def draw_sum_bar_chart(files, dir_path, fontsize=10, figsize=(10, 6)):
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
    plt.title('Quantity of waste from the random sampling at 1 minute from: Test_20231219_154141793')
    plt.xlabel('Batch of random sampling close to average density')
    plt.ylabel('Waste quantity of each random sampling')
    plt.xticks(rotation=0)
    plt.ylim(0, 125)
    plt.legend(bbox_to_anchor=(0., 0.94, 1., .102), loc='lower left', ncol=6, mode="expand", borderaxespad=0.1)

    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        ax.text(x+width/2,
                y+height/2,
                '{:.0f} ({:.2%})'.format(height, height/df_total.sum().sum()),
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=fontsize)

    for i, total_waste in enumerate(total_wastes):
        ax.text(i, total_waste+5, str(total_waste), color='black', ha='center')

    plt.savefig(dir_path + "/Quantity of waste from the random sampling at 1 minute from: Test_20231219_154141793.png")
    plt.show()

draw_sum_bar_chart(files, dir_path)
Frequency_reviews(files)
Number_of_manual_reviews(files)
