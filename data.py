
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')

# 读取数据
df = pd.read_csv('/home/sxwang/SOTAtest/231212test/20231212T.csv')

# 删除第一列字符不是23/12/12的行
df = df[df.iloc[:, 0] == '23/12/12']
# 删除所有空白的列
df = df.dropna(how='all', axis=1)
# 删除第二列内容末尾的"下午"两个字
df.iloc[:, 1] = df.iloc[:, 1].str.rstrip('下午')
# 删除第三列内容开始的{
df.iloc[:, 2] = df.iloc[:, 2].str.lstrip('{')


# 创建曲线图
plt.figure(figsize=(10, 6))
plt.plot(df.index, df.iloc[:, 3], label='pcb')
plt.plot(df.index, df.iloc[:, 5], label='rubber')
plt.plot(df.index, df.iloc[:, 7], label='tube')
plt.plot(df.index, df.iloc[:, 9], label='wire')
plt.plot(df.index, df.iloc[:, 11], label='can')
plt.plot(df.index, df.iloc[:, 13], label='painted_metal')

# 设置标题和坐标轴标签
plt.title('waste')
plt.xlabel('time')
plt.ylabel('data')
# 设置坐标轴刻度
plt.xticks(range(min(df.index), max(df.index) + 1, 1000))
plt.yticks(np.arange(min(df.iloc[:, 5]), max(df.iloc[:, 5]) + 1, 100))


# 添加图例
plt.legend()
# 显示图形
plt.show()


# 将整理后的数据输出到新文件
df.to_csv('/home/sxwang/SOTAtest/231212test/20231212T1.csv', index=False)
