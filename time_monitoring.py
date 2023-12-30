import pandas as pd
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt


# Get the list of filenames in the folder
#directory_path = "/home/sxwang/SOTAtest/231215MightyOutput/20231215_172140641"
#filenames = os.listdir(directory_path + "/raw")

def time_monitor(directory_path, filenames):
    # Initialize an empty list for times
    times = []

    # Loop through filenames and convert the last nine characters to datetime if possible

    for filenames in filenames:
        try:
            # time = pd.to_datetime(filenames[:-4][-9:], format='%H%M%S%f')
            time = pd.to_datetime(filenames[:-5][-8:], format='%H%M%S%f') #T
            print(time)
            # labeled
            #time = pd.to_datetime(filenames[:-8][-9:], format='%H%M%S%f')
            times.append(time)
        except ValueError:
            pass  # If the conversion fails, just ignore this filename and move on to the next

    # Sort the list of times
    times.sort()

    # Calculate the difference between adjacent times, storing in df_t, and convert microseconds to milliseconds
    df_t = pd.DataFrame({'Time': times[:-1], 'Difference': [((j - datetime.datetime(1900, 1, 1)).total_seconds() - (i - datetime.datetime(1900, 1, 1)).total_seconds())*1000 for i, j in zip(times[:-1], times[1:])]})

    print(df_t)

    # Create a line plot
    fig1, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_t['Time'].apply(lambda x: x.time().strftime('%H:%M:%S.%f')[:-3]), df_t['Difference'])  # Convert datetime.time to string and trim microseconds to 3 digits
    ax.scatter(df_t['Time'].apply(lambda x: x.time().strftime('%H:%M:%S.%f')[:-3]), df_t['Difference'], s=10, color='red')  # Convert datetime.time to string and trim microseconds to 3 digits
    ax.set_ylim(0, 2500)  # Set the limit for y-axis
    ax.set_ylim(0, 2500)  # Set the limit for y-axis
    # Add a marker

    # Set the title and axis labels
    # ax.set_title('File path: ' + str(directory_path))
    ax.set_title('Time of per sensor photograph (per image): ' + str(directory_path)[-23:])
    ax.set_xlabel('Test Time (h:m:s:ms)')
    ax.set_ylabel('Time Difference (ms)')

    # Reduce the number of xticks
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))

    # Save the plot to a file
    plt.savefig(directory_path + '/test_time_difference.png')

    # Display the plot
    plt.show()

    # Create a scatter plot

    fig2, ax1 = plt.subplots(figsize=(10, 6))
    ax1.scatter(df_t['Time'].apply(lambda x: x.time().strftime('%H:%M:%S.%f')[:-3]), df_t['Difference'], s=10,
                color='red')  # Convert datetime.time to string and trim microseconds to 3 digits

    # 计算平均值
    average_difference = np.mean(df_t['Difference'])

    # 添加平均值的横线
    ax1.axhline(average_difference, color='red', linewidth=1)

    # 添加平均值的标签
    ax1.text(0.01, average_difference + 50, 'Average time: {:.2f} ms'.format(average_difference), color='red')

    ax1.set_ylim(0, 2500)  # 设置y轴的范围

    # 设置标题和坐标轴的标签
    ax1.set_title('Time of per sensor photograph (per image): ' + str(directory_path)[-23:])
    ax1.set_xlabel('Test Time (h:m:s:ms)')
    ax1.set_ylabel('Time Difference (ms)')

    # 减少x轴刻度的数量
    ax1.xaxis.set_major_locator(plt.MaxNLocator(8))

    # 保存图到文件
    plt.savefig(directory_path + '/test_time_difference_scatter.png')

    # 显示图
    plt.show()

    return average_difference







