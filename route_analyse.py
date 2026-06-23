import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def analyze_route_stops(df, route_col='线路号', stops_col='ride_stops'):
    # 按线路号分组，计算均值和标准差
    result = df.groupby(route_col)[stops_col].agg(
        mean_stops='mean',
        std_stops='std'
    ).reset_index()

    # 按 mean_stops 降序排列
    result = result.sort_values('mean_stops', ascending=False).reset_index(drop=True)

    return result


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


