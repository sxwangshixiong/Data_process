import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# 函数1: 按照'b'排序并筛选在[A,B]区间内的数据
def sort_and_filter(df, A, B):
    df['a'] = df['filename'].str[:8]
    df['b'] = df['filename'].str[-9:]
    df1 = df[['a', 'b']]
    print("df1:", df1)
    print("df:", df)
    #df = pd.concat([df1, df], axis=1)
    #print(df)
    #df = df.drop_duplicates('b')
    df = df[(df['b'].astype(int) >= A) & (df['b'].astype(int) <= B)]
    df = df.sort_values(by='b')
    return df

# 函数2: 随机选取b，并按照选取结果进行分割
def split_df_A(df, A, B, A1, B1, r):
    global b1

    df_dict = {}
    for i in range(r):
        if B[-7:] == 0000000:
            b1 = np.random.randint(A, (B - 10000000) + 5900000)
        else:
            b1 = np.random.randint(A, B-100000)

        if b1[-7:] >= 6000000:
            b1 = (b1 + 10000000) - 6000000
        else:
            b1 = b1

        if b1[-5:] >= 50000:
            df_i = df[(df['b'].astype(int) >= b1) & (df['b'].astype(int) < ((b1 + 100000) - 60000))]
        else:
            df_i = df[(df['b'].astype(int) >= b1) & (df['b'].astype(int) < b1 + 100000)]
        df_dict['df_'+str(i+1)] = df_i
    print(df_dict)
    return df_dict, b1
def split_df(df, A, B, A11, B11, r):
    global b1
    df_dict = {}
    b1_values = []  # List to store each b1
    for i in range(r):
        if A11 == 0 or B11 == 0:
            b1 = np.random.randint(A, B - 100000)
        else:
            if np.random.choice([True, False]):
                b1 = np.random.randint(A, B - 100000)
            else:
                b1 = np.random.randint(A11, B11 - 100000)

        if int(str(b1)[-7:]) >= 6000000:
            b1 = (b1 + 10000000) - 6000000
        else:
            b1 = b1

        if int(str(b1)[-5:]) >= 60000:
            b1 = (b1 + 100000) - 60000
        else:
            b1 = b1
        print("b1:", b1)
        if int(str(b1)[-5:]) >= 50000:
            df_i = df[(df['b'].astype(int) >= b1) & (df['b'].astype(int) < ((b1 + 100000) - 60000))]
        else:
            df_i = df[(df['b'].astype(int) >= b1) & (df['b'].astype(int) < b1 + 100000)]
        # df_i = df[(df['b'].astype(int) >= b1) & (df['b'].astype(int) < b1 + 100000)]
        df_dict['df_'+str(i+1)] = df_i
        b1_values.append(b1)  # Add b1 to the list
    print(df_dict)
    return df_dict, b1_values  # Return the list of b1 values

def split_df_C(df, A, B, A11, B11, r):
    global b1
    # Convert B to a datetime object
    A_datetime = datetime.strptime(str(A), '%H%M')
    B_datetime = datetime.strptime(str(B), '%H%M')
    A11_datetime = datetime.strptime(str(A11), '%H%M')
    B11_datetime = datetime.strptime(str(B11), '%H%M')
    # Calculate A as B minus 1 minute
    B_time = B_datetime - timedelta(minutes=1)
    B11_time = B11_datetime - timedelta(minutes=1)

    print('A:', A)
    print('B:', B)
    df_dict = {}
    b1_values = []  # List to store each b1
    for i in range(r):
        if A11 == 2359 or B11 == 2359:
            b1 = np.random.randint(A_datetime, B_time)
        else:
            if np.random.choice([True, False]):
                b1 = np.random.randint(A_datetime, B_time)
            else:
                b1 = np.random.randint(A11_datetime, B11_time)
        b1_max = b1 + timedelta(minutes=1)
        b1 = int(b1)
        b1_max = int(b1_max)
        b1_values.append(b1)  # Add b1 to the list
        df_i = df[(df['b'].astype(int) >= b1) & (df['b'].astype(int) < b1_max)]
        df_dict['df_'+str(i+1)] = df_i
    # print(df_dict)
    return df_dict, b1_values  # Return the list of b1 values
