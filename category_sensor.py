import pandas as pd
import os
import datetime
import re
from glob import glob

dir_path = '/home/sxwang/SOTAtest/231215MightyOutput/20231215_172140641'  # directory path
result_dir_path = dir_path + "/result_out"

# Get the list of directories that start with "df"
directories = [dir for dir in os.listdir(result_dir_path) if dir.startswith('df')]
print(directories)

# Initialize an empty DataFrame to store filenames and times
df_f = pd.DataFrame(columns=['Filename', 'Time'])

# Loop through directories and extract filenames and times
for directory in directories:
    # Get the list of filenames in the directory
    full_path = os.path.join(result_dir_path, directory)  # Join the base path with the directory
    filenames = os.listdir(full_path)

    # Extract the last 9 characters of the filename and convert to time format
    for filename in filenames:
        # Check if the last nine characters match the time format
        if re.match("\\d{9}", filename[:-4][-9:]):
            time = pd.to_datetime(filename[:-4][-9:], format='%H%M%S%f')
            df_f.loc[len(df_f)] = {'Filename': filename, 'Time': time}

# Get the list of csv files in the path
csv_files = glob(dir_path + "/20231215_172123.csv")

# Initialize an empty DataFrame to store the rows that meet the condition
df_v = pd.DataFrame()

# Loop through csv files and extract the rows that meet the condition
for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    # Convert the first column to datetime format
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y/%m/%d_%H:%M:%S.%f')

    # Loop through the times in df_f
    for time in df_f['Time']:
        # Calculate the end time of the interval
        end_time = time + pd.Timedelta(minutes=1)

        # Extract the rows that meet the condition and append to df_v
        for i in range(len(df)):
            try:
                # print(df.iloc[i, 0])
                df.iloc[i, 0] = pd.to_datetime(df.iloc[i, 0])
            except ValueError:
                continue
        # 将第一列转换为 datetime 格式
        #df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y/%m/%d_%H:%M:%S.%f')
        df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors='coerce')

        # 现在，比较应该可以工作了
        df_v = pd.concat([df_v, df[(df.iloc[:, 0] >= time) & (df.iloc[:, 0]) < end_time]])

    print(df_v)

