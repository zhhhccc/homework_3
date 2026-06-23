# 赵浩程-25361186-第三次人工智能编程作业

仓库链接: https://github.com/zhhhccc/homework_3

### 不小心把代码分成了四个文件，想更正时为时已晚，求老师与助教原谅，少扣一点点分，|>_<|，在main文件中可以运行全部代码，谢谢老师，谢谢助教老师

## 1. 任务拆解与 AI 协作策略

本次作业包含 6 个数据分析任务，整体采用“分阶段 + 逐步验证 + 逐步加入自己的想法”的 AI 协作方式，而不是一次性生成完整代码。  
我将整个作业分为了六个小文件，每个小文件中包含一个任务，将这些任务分不同的对话输入给AI，让AI完成  
除了让AI读文件，我还会告诉AI我还有什么在这个任务中可以利用的已知内容，例如：已经转化为dataframe并命名为df的ICDaTa，或者更简单一点，我只需要告诉AI，我有一个dataframe里面有一列叫hour  

详细思路如下：

### （1）任务一
- 先让 AI 帮我把 ICData.csv 转化为dataframe
- 告诉AI我有dataframe，并把文件传给AI，让它帮我完成：
  - 时间解析（hour 字段）
  - ride_stops 构造
  - 缺失值处理
- 为了方便以后使用，我把这些个函数手动封装为类，避免import多个函数（不过使用完后感觉便捷性提升并不大）


### （2）任务二
- 告诉AI我有hour列，并把文件传给AI，让它帮我完成：
  - numpy 时间段统计
  - matplotlib 24小时分布图

### （3）任务三
- 告诉AI我有df，单独要求 AI 按“严格函数签名”实现 analyze_route_stops
- 在让AI在之前不变的基础上完成可视化

### （4）任务四
- 告诉AI我有转化为datetime的列，并把文件传给AI，让它帮我完成粒度计算
- 我发现任务四与任务二都趋近于时间的处理，有可以共同利用的数据，于是我自己添加__init__，将它们手动封装到了一个类里

### （5）任务五与任务六
- 告诉AI我有df以及各个列的名称，让AI分别完成任务就行

---

## 2. 核心 Prompt 迭代记录——括号内为实例

### ❌ 初代 Prompt
> 仅仅将六个任务分对话传给AI
> （我只把任务二的文件内容传给了AI）

### ❌ AI 生成的问题
- AI只知道有什么要求，不知道有什么内容可以利用，它虽然会给你多种假设，但你自己去选择用哪种情况明显极其浪费时间，而且它的假设不一定包含你的情况
- （AI自己生成了一段刷卡时间的数组与测试代码，自己修改极其麻烦）

---

### ✅ 优化后的 Prompt
> 1. 已知：……（已经有一个用pandas处理过的dataframe数据，'hour'列为交易时间，也含有'交易类型'列）
> 2. 任务文件（任务二.docx）
> 3. 自己的其他要求：写成函数等等(写成两个函数)

### ✅ 优化效果
- 代码与已知完全搭配
- 有函数，逻辑清晰

---

## 3. Debug 记录

### ❌ 报错现象1：旧版本弃用
FutureWarning: Passing palette without assigning hue is deprecated and will be removed in v0.14.0.   
Assign the y variable to hue and set legend=False for the same effect.  
ax = sns.barplot(

- 错误原因：这是 Seaborn 的一个 FutureWarning（未来版本弃用警告），不是错误，你的代码现在还能正常运行，但以后版本（v0.14.0+）会不再支持这种写法。
- Seaborn 新版本规定： 不能单独使用 palette，除非你同时指定 hue

### ✅ 解决方法：
```python
ax = sns.barplot(
        data=top15,
        y='线路号',
        x='mean_stops',
        hue='线路号',
        palette=palette,
        errorbar=None,  # 禁用自带误差棒，手动绘制
        orient='h',
        legend=False
    )
```

## 4. 人工代码审查
```python
def Peak_Hour_Factor(self):  
    # 定义一个方法：计算高峰小时系数（Peak Hour Factor, PHF）

    peak_hour = np.argmax(self.hourly_counts)  
    # 在 hourly_counts（每小时客流量数组）中找到最大值的索引
    # 这个索引对应“客流最高的小时”

    peak_hour_volume = self.hourly_counts[peak_hour]  
    # 取出该高峰小时对应的总刷卡量（客流量）

    print(f"高峰小时：{peak_hour:02d}:00 ~ {peak_hour + 1:02d}:00，刷卡量：{peak_hour_volume} 次")  
    # 输出高峰小时信息
    # :02d 表示两位数格式（如 08:00）

    peak_df = self.df1[
        (self.df1['交易时间'].dt.hour == peak_hour)
    ].copy()  
    # 从原始数据 df1 中筛选出“高峰小时内”的所有记录
    # .dt.hour 提取时间中的“小时”
    # .copy() 防止后续修改触发 SettingWithCopyWarning

    peak_df = peak_df.set_index('交易时间')  
    # 将“交易时间”设置为索引
    # 方便后续按时间重采样（resample）

    count_5min = peak_df.resample('5min').size()  
    # 按 5 分钟进行重采样统计
    # .size() 表示每个5分钟区间内的记录数（刷卡次数）

    max5 = count_5min.max()  
    # 找到高峰小时内，5分钟粒度下的最大客流量

    max5_time = count_5min.idxmax()  
    # 找到最大5分钟客流发生的时间点

    PHF5 = peak_hour_volume / (12 * max5)  
    # 计算高峰小时系数 PHF（基于5分钟粒度）
    # 公式：PHF = 小时总流量 / (12 × 最大5分钟流量)
    # 12 = 1小时 / 5分钟 = 12个区间
```