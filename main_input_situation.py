import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import config as cfg
from scipy.interpolate import UnivariateSpline


def create_chart(value_min, value_max, t):

    # Read the Excel file
    dir_path_test = cfg.dir_path_test240126 # Test
    # dir_path_test = cfg.dir_path

    dir_path = dir_path_test + '/result_out/'
    df = pd.read_excel(dir_path + 'output1.xlsx')
    test_name = 'Test_' + dir_path_test[-18:]

    # Specify the format of the date/time strings
    date_format = '%Y%m%d_%H%M%S%f'

    # Calculate the time difference and convert it to minutes
    print(df.iloc[0, 2], df.iloc[0, 1])
    if len(str(df.iloc[0, 2])) == 18:
        x_f = 0
    elif len(str(df.iloc[0, 1])) == 18:
        x_f = -1
    df['TimeDifference'] = (pd.to_datetime(df.iloc[:, (2 + x_f)], format=date_format) - pd.to_datetime(df.iloc[:, (2 + x_f)], format=date_format).min()).dt.total_seconds() / 60

    # Copy the first 9 columns of the original dataframe to a new one
    output2 = df.iloc[:, :(9 + x_f)].copy()

    # Add the time difference as the 10th column
    output2['TimeDifference'] = df['TimeDifference']

    # Save the new dataframe to an Excel file
    output2.to_excel(dir_path + 'output2.xlsx', index=False)

    # Extract the 7th column
    df5 = df.iloc[:, (6 + x_f)]

    # Calculate the sum of the time when df5 <= 5
    value_sum = df.loc[df5 <= 5, 'TimeDifference'].sum()

    # Plot the time difference against the 7th column based on the condition
    plt.scatter(df.loc[df5 > 5, 'TimeDifference'], df5[df5 > 5], color=(180/255, 180/255, 180/255), s=1)
    plt.scatter(df.loc[df5 <= 5, 'TimeDifference'], df5[df5 <= 5], color=(100/255, 100/255, 100/255), s=1)
    plt.text(value_min + 1, 0, 'Sum of proportion < 5%: ' + str(value_sum) + 'min', color='k')
    # Calculate the average of the 7th column


    average = df5.mean()

    # Draw a horizontal line representing the average
    plt.axhline(y=average, color=(100/255, 100/255, 100/255))

    x = df['TimeDifference']
    y = df5
    # x = df.loc[df5 > 5, 'TimeDifference']
    # y = df5[df5 > 5]
    # 使用UnivariateSpline函数来拟合数据
    spline = UnivariateSpline(x, y, k=5, s=350000)
    # average_1 = spline(x).mean()
    # # Draw a horizontal line representing the average
    # plt.axhline(y=average_1, color=(100/255, 100/255, 100/255))
    # plt.text(0, average_1 + 5.5, 'Average proportion: ' + str(average_1)[:6] + '%', color='k')
    # 绘制原始数据和拟合曲线
    # plt.scatter(x, y, color='blue', label='Original data')
    plt.plot(x, spline(x), color=(31/255, 119/255, 180/255), label='Fitted spline', linewidth=0.8)


    if value_max == 0:
        value_max = int(df['TimeDifference'].max())
    # Get n evenly spaced numbers between 0 and the maximum time difference
    n_values = np.linspace(value_min, value_max, num=5)

    for n in n_values:
        # Find the value in the time difference column that is closest to n
        closest_x = df.iloc[(df['TimeDifference'] - n).abs().argsort()[:1]]

        # Get the corresponding value from the 9th column
        y1 = closest_x.iloc[:, (8 + x_f)].values[0]
        print(y1)
        # Plot the point and annotate it with the value from the 9th column
        plt.plot(closest_x['TimeDifference'], average, 'ro', markersize=5)
        plt.text(0, average + 2.5, 'Average proportion: ' + str(average)[:6] + '%', color='k')
        if int(str(y1)[:1]) >= 2:
            time_name = '0' + str(y1)[:1] + ':' + str(y1)[1:3]
        else:
            time_name = str(y1)[:2] + ':' + str(y1)[2:4]
        plt.text(closest_x['TimeDifference'] + 1, average + 0.5, time_name, color='red')

    # Set the size of the plot
    plt.gcf().set_size_inches(10, 6)

    # Set the title and labels of the plot
    plt.title("The proportion of the conveyor belt covered with material during the " + test_name + "_" + str(t))
    plt.xlabel('Test time (minutes)')
    plt.ylabel('Proportion (%)')
    plt.xlim(value_min, value_max)  # 设置y轴范围
    # Show the plot
    plt.savefig(dir_path + "/The proportion of the conveyor belt covered with material during the " + test_name + "_" + str(t) + ".png")
    plt.show()

    max_value_x = int(df['TimeDifference'].max())
    return max_value_x, value_sum

max_value_x, value_sum = create_chart(0, 0, 0)
t = 0
for i in range(int(max_value_x / 60) + 1):
    value_min = 0 + 60 * t
    value_max = 60 + 60 * t
    print(str(t + 1) + "th is begin")
    create_chart(value_min, value_max, t + 1)
    print(str(t + 1) + "th is end")
    t += 1
