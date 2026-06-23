import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pre_process import data
a=data()
df = a.delete()

class time_analysis:
    def __init__(self):
        self.df1,self.hours,self.hourly_counts=self.process(df)

    def process(self,df):
        # 过滤刷卡类型为0的记录
        card_type_0 = df['刷卡类型'] == 0
        df_filtered = df[card_type_0].copy()

        # 提取小时数据为numpy数组
        hours = df_filtered['hour'].values

        # 计算每个小时的刷卡量
        hourly_counts = np.zeros(24, dtype=int)

        for h in range(24):
            hourly_counts[h] = np.sum(hours == h)

        return df_filtered,hours,hourly_counts

    def ea_to_tally(self):

        # (a) 早晚时段刷卡量统计 - 使用numpy
        # 1. 早峰前时段: hour < 7
        morning_mask = self.hours < 7
        morning_count = np.sum(morning_mask)

        # 深夜时段: hour >= 22
        night_mask = self.hours >= 22
        night_count = np.sum(night_mask)

        # 计算全天总刷卡量
        total_count = len(self.hours)

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

    def visualize_ea(self):

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
        bars = ax.bar(hours_all, self.hourly_counts, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)

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

    def Peak_Hour_Factor(self):
        peak_hour = np.argmax(self.hourly_counts)
        peak_hour_volume = self.hourly_counts[peak_hour]

        print(f"高峰小时：{peak_hour:02d}:00 ~ {peak_hour + 1:02d}:00，刷卡量：{peak_hour_volume} 次")

        peak_df = self.df1[
            (self.df1['交易时间'].dt.hour == peak_hour)
        ].copy()

        peak_df = peak_df.set_index('交易时间')

        count_5min = peak_df.resample('5min').size()

        max5 = count_5min.max()
        max5_time = count_5min.idxmax()

        PHF5 = peak_hour_volume / (12 * max5)

        print(
            f"最大5分钟刷卡量（{max5_time:%H:%M}~"
            f"{(max5_time + pd.Timedelta(minutes=5)):%H:%M}）："
            f"{max5} 次",
            end=' '
        )

        print(
            f"PHF5 = {peak_hour_volume} / (12 × {max5}) = {PHF5:.4f}"
        )

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
