import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def read():
    # 取消截断隐藏
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    # 读取CSV文件
    df = pd.read_csv('ICData.csv')
    return df

#任务一（1）读取
df_original=read()


def test(df):
    # 打印前五行
    print("数据集前五行：")
    print(df.head(5))
    # 打印行数和列数
    print()
    print(f"行数: {df.shape[0]}", end=' ')
    print(f"列数: {df.shape[1]}")
    # 2. 打印各列数据类型
    print(df.dtypes)

#任务一（1）输出
test(df_original)


def shift(df):
    # 将交易时间转换为datatime
    df['交易时间'] = pd.to_datetime(df['交易时间'])
    # 提取出来一列，是刷卡的具体小时，叫做hour
    df['hour'] = df['交易时间'].dt.hour
    # 提取出来一列，乘坐了多少站
    df['ride_stops'] = (df["上车站点"] - df["下车站点"]).abs()
    # 统计 ride_stops 列中 0 的个数（记录）
    zero_count = (df['ride_stops'] == 0).sum()
    print(f"构造ride_stops后删除异常记录(ride_stops==θ/无法计算)行数：{zero_count}")
    # 删除为 0 的行
    df = df[df['ride_stops'] != 0]
    #统计缺失值
    df_missing_value = df.isnull().sum()
    num = df_missing_value.sum()
    # 删除有缺失值的行
    df_cleaned = df.dropna()
    print('各列缺失值数量：')
    if num == 0:
        print('无缺失值')
    else:
        print(df_missing_value)

    return df_cleaned

#任务一（2）（3）（4）
df= shift(df_original)

def process(df):
    # 过滤刷卡类型为0的记录
    card_type_0 = df['刷卡类型'] == 0
    df_filtered = df[card_type_0].copy()

    # 提取小时数据为numpy数组
    hours = df_filtered['hour'].values

    # 计算每个小时的刷卡量
    hourly_counts = np.zeros(24, dtype=int)

    for h in range(24):
        hourly_counts[h] = np.sum(hours == h)

    return df_filtered, hours, hourly_counts

#任务二（1）数据处理
df_filtered, hours, hourly_counts=process(df)


def ea_to_tally(hours):
    # (a) 早晚时段刷卡量统计 - 使用numpy
    # 1. 早峰前时段: hour < 7
    morning_mask = hours < 7
    morning_count = np.sum(morning_mask)

    # 深夜时段: hour >= 22
    night_mask = hours >= 22
    night_count = np.sum(night_mask)

    # 计算全天总刷卡量
    total_count = len(hours)

    # 计算百分比
    morning_pct = (morning_count / total_count * 100) if total_count > 0 else 0
    night_pct = (night_count / total_count * 100) if total_count > 0 else 0

    # 打印统计结果
    print("=" * 50)
    print("时段刷卡量统计")
    print("=" * 50)
    print(f"全天总刷卡量: {total_count}")
    print(f"早峰前时段 (< 7:00): {morning_count} 次, 占比: {morning_pct:.2f}%")
    print(f"深夜时段 (>= 22:00): {night_count} 次, 占比: {night_pct:.2f}%")
    print("=" * 50)

#任务二（1）输出
ea_to_tally(hours)

def visualize_ea(hourly_counts):
    # (b) 24小时刷卡量分布可视化
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 6))

    # 为不同时段设置颜色
    colors = []
    for h in range(24):
        if h < 7 or h >= 22:
            colors.append('#FF6B6B')  # 红色
        else:
            colors.append('#6C5CE7')  # 紫色（常规时段）

    hours_all = np.arange(24)

    # 绘制柱状图
    bars = ax.bar(hours_all, hourly_counts, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)

    # 创建图例
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#FF6B6B', alpha=0.8, label='Early & Late Night')]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

    # 设置坐标轴标签和标题
    ax.set_xlabel('Hours (0~23)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Swipes', fontsize=12, fontweight='bold')
    ax.set_title('24-Hour Card Swipe Distribution', fontsize=14, fontweight='bold')

    # 设置x轴刻度，步长为2
    ax.set_xticks(np.arange(0, 24, 2))
    ax.set_xticklabels(np.arange(0, 24, 2))

    # 添加水平网格线
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
    ax.set_axisbelow(True)  # 网格线在柱状图下方

    # 调整布局并保存
    plt.tight_layout()
    plt.savefig('hour_distribution.png', dpi=150, bbox_inches='tight')
    print(f"\n图表已保存为: hour_distribution.png")
    plt.close()

#任务二（2）
visualize_ea(hourly_counts)

def analyze_route_stops(df, route_col='线路号', stops_col='ride_stops'):
    # 按线路号分组，计算均值和标准差
    result = df.groupby(route_col)[stops_col].agg(
        mean_stops='mean',
        std_stops='std'
    ).reset_index()

    # 按 mean_stops 降序排列
    result = result.sort_values('mean_stops', ascending=False).reset_index(drop=True)

    return result

#任务三（1）
print(analyze_route_stops(df).head(10))

def visualize(df):
    # 可视化（均值最高的前15条线路）
    top15 = df.head(15).copy()

    plt.figure(figsize=(15, 10))
    palette = sns.color_palette("Blues_d", n_colors=len(top15))

    # 绘制水平条形图
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

    for patch, (_, row) in zip(ax.patches, top15.iterrows()):
        x_right = patch.get_x() + patch.get_width()
        y_center = patch.get_y() + patch.get_height() / 2

        ax.errorbar(
            x=x_right,
            y=y_center,
            xerr=row['std_stops'],
            fmt='none',
            color='black',
            capsize=3,
            elinewidth=1.5
        )

    # 标题与标签（英文）
    ax.set_title("Top 15 Routes: Mean Ride Stops", fontsize=14)
    ax.set_xlabel("Mean Ride Stops", fontsize=12)
    ax.set_ylabel("Route ID", fontsize=12)

    # 方案1：固定 0~25（按你的要求）
    ax.set_xlim(0, 24)
    ax.grid(axis='x',alpha=0.3, linestyle='--', linewidth=0.7)
    ax.set_axisbelow(True)  # 网格线在柱状图下方

    # 调整布局并保存
    plt.tight_layout()
    plt.savefig("route_stops.png", dpi=150)
    plt.close()  # 关闭图形释放内存
    print('图表已保存为: route_stops.png')

#任务三（2）
visualize(analyze_route_stops(df))

def Peak_Hour_Factor(hourly_counts,df):
    # 定义一个方法：计算高峰小时系数（Peak Hour Factor, PHF）

    peak_hour = np.argmax(hourly_counts)
    # 在 hourly_counts（每小时客流量数组）中找到最大值的索引
    # 这个索引对应“客流最高的小时”

    peak_hour_volume = hourly_counts[peak_hour]
    # 取出该高峰小时对应的总刷卡量（客流量）

    print(f"高峰小时：{peak_hour:02d}:00 ~ {peak_hour + 1:02d}:00，刷卡量：{peak_hour_volume} 次")
    # 输出高峰小时信息
    # :02d 表示两位数格式（如 08:00）

    peak_df = df[
        (df['交易时间'].dt.hour == peak_hour)
    ].copy()
    # 从原始数据 df 中筛选出“高峰小时内”的所有记录
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

    print(
        f"最大5分钟刷卡量（{max5_time:%H:%M}~"
        f"{(max5_time + pd.Timedelta(minutes=5)):%H:%M}）："
        f"{max5} 次",
        end=' '
    )

    print(
        f"PHF5 = {peak_hour_volume} / (12 × {max5}) = {PHF5:.4f}"
    )
    #输出

    count_15min = peak_df.resample('15min').size()

    max15 = count_15min.max()
    max15_time = count_15min.idxmax()

    PHF15 = peak_hour_volume / (4 * max15)

    print(
        f"最大15分钟刷卡量（{max15_time:%H:%M}~"
        f"{(max15_time + pd.Timedelta(minutes=15)):%H:%M}）："
        f"{max15} 次",
        end=' '
    )

    print(
        f"PHF15 = {peak_hour_volume} / (4 × {max15}) = {PHF15:.4f}"
    )
    #与以上类似

#任务四
Peak_Hour_Factor(hourly_counts,df_filtered)

def driver_deriving(df):
    df["线路号"] = df["线路号"].astype(int)
    df["车辆编号"] = df["车辆编号"].astype(int)
    df["驾驶员编号"] = df["驾驶员编号"].astype(int)

    # === 1. 筛选线路号 ===
    df_filtered = df[(df["线路号"] >= 1101) & (df["线路号"] <= 1120)]

    # === 2. 创建输出文件夹 ===
    folder_name = "线路驾驶员信息"
    os.makedirs(folder_name, exist_ok=True)

    # 用于保存输出路径
    output_paths = []

    # === 3. 按线路号分组 ===
    for line, group in df_filtered.groupby("线路号"):

        # 去重：车辆编号 -> 驾驶员编号
        relation = (
            group[["车辆编号", "驾驶员编号"]]
            .drop_duplicates()
            .sort_values("车辆编号")  # 按车辆编号升序
        )

        # 文件路径
        file_path = os.path.join(folder_name, f"{line}.txt")

        # 写入文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"线路号: {line}\n")
            for _, row in relation.iterrows():
                car = int(row["车辆编号"])
                driver = int(row["驾驶员编号"])
                f.write(f"{row['车辆编号']}\t{row['驾驶员编号']}\n")

        output_paths.append(file_path)

    # === 4. 打印结果 ===
    print("文件生成完成，共20个文件：\n")
    for path in output_paths:
        print(path)

#任务五
driver_deriving(df_filtered)

def ranking_statistics(df):

    # 定义一个内部函数：用于统计某一列的Top10频次
    def top10(col):
        return df[col].value_counts().head(10).reset_index()

    # 分别统计四个维度的Top10
    driver = top10("驾驶员编号")   # 最常出现的10个驾驶员
    route = top10("线路号")       # 最常出现的10条线路
    station = top10("上车站点")    # 最常出现的10个上车站点
    vehicle = top10("车辆编号")    # 最常出现的10辆车

    # 统一列名，方便后续处理
    driver.columns = ["entity", "count"]
    route.columns = ["entity", "count"]
    station.columns = ["entity", "count"]
    vehicle.columns = ["entity", "count"]

    # 构造用于热力图的数据结构（每一行是一个类别）
    heatmap_df = pd.DataFrame({
        "Driver": driver["count"].values,
        "Route": route["count"].values,
        "Boarding Station": station["count"].values,
        "Vehicle": vehicle["count"].values
    })

    # 设置行索引为 Top1 ~ Top10
    heatmap_df.index = [f"Top{i}" for i in range(1, 11)]

    # 转置，使类别作为行，排名作为列（更适合heatmap展示）
    heatmap_df = heatmap_df.T

    # ===== 打印 Top10 车辆 =====
    vehicle_top10 = df["车辆编号"].value_counts().head(10)

    print("\n===== Top10 Vehicle =====")
    for i, (vehicle_id, cnt) in enumerate(vehicle_top10.items(), 1):
        print(f"Top{i}: {vehicle_id}  Count={cnt}")

    # ===== 打印 Top10 驾驶员 =====
    driver_top10 = df["驾驶员编号"].value_counts().head(10)

    print("\n===== Top10 Driver =====")
    for i, (driver_id, cnt) in enumerate(driver_top10.items(), 1):
        print(f"Top{i}: {driver_id} Count={cnt}")

    # ===== 打印 Top10 线路 =====
    route_top10 = df["线路号"].value_counts().head(10)

    print("\n===== Top10 Route =====")
    for i, (route_id, cnt) in enumerate(route_top10.items(), 1):
        print(f"Top{i}: {route_id} Count={cnt}")

    # ===== 打印 Top10 上车站点 =====
    station_top10 = df["上车站点"].value_counts().head(10)

    print("\n===== Top10 Boarding Station =====")
    for i, (station_id, cnt) in enumerate(station_top10.items(), 1):
        print(f"Top{i}: {station_id} Count={cnt}")

    # ===== 绘制热力图 =====
    plt.figure(figsize=(12, 5))

    # 使用YlOrRd颜色映射展示频次强弱
    sns.heatmap(heatmap_df, annot=True, fmt=".0f", cmap="YlOrRd")

    # 图表标题与坐标说明
    plt.title("Service Performance Heatmap (Top10 Entities)", fontsize=14)
    plt.xlabel("Top Ranking")
    plt.ylabel("Category")

    # x轴标签不旋转
    plt.xticks(rotation=0)

    # 保存图片
    plt.savefig("performance_heatmap.png", dpi=150, bbox_inches="tight")
    print('图表已保存为: performance_heatmap.png')

    print(
        """结论：从热力图可以看出客流呈现明显集中趋势，少数线路和站点承担了主要客流量，其中Top1的线路或站点显著高于其他排名，说明存在明显的核心交通枢纽。部分司机和车辆服务人次较高，可能集中在高峰线路或热门区域运营，整体分布呈现头部集中、长尾分布特征。""")

#任务六
ranking_statistics(df_filtered)