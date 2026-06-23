import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def ranking_statistics():
    from pre_process import data
    a = data()
    df = a.delete()[3]

    def top10(col):
        return df[col].value_counts().head(10).reset_index()

    driver = top10("驾驶员编号")
    route = top10("线路号")
    station = top10("上车站点")
    vehicle = top10("车辆编号")

    driver.columns = ["entity", "count"]
    route.columns = ["entity", "count"]
    station.columns = ["entity", "count"]
    vehicle.columns = ["entity", "count"]

    heatmap_df = pd.DataFrame({
        "Driver": driver["count"].values,
        "Route": route["count"].values,
        "Boarding Station": station["count"].values,
        "Vehicle": vehicle["count"].values
    })

    heatmap_df.index = [f"Top{i}" for i in range(1, 11)]
    heatmap_df = heatmap_df.T

    vehicle_top10 = df["车辆编号"].value_counts().head(10)

    print("\n===== Top10 Vehicle =====")
    for i, (vehicle_id, cnt) in enumerate(vehicle_top10.items(), 1):
        print(f"Top{i}: {vehicle_id}  Count={cnt}")

    driver_top10 = df["驾驶员编号"].value_counts().head(10)

    print("===== Top10 Driver =====")
    for i, (driver_id, cnt) in enumerate(driver_top10.items(), 1):
        print(f"Top{i}: {driver_id} Count={cnt}")

    route_top10 = df["线路号"].value_counts().head(10)

    print("\n===== Top10 Route =====")
    for i, (route_id, cnt) in enumerate(route_top10.items(), 1):
        print(f"Top{i}: {route_id} Count={cnt}")

    station_top10 = df["上车站点"].value_counts().head(10)

    print("\n===== Top10 Boarding Station（上车站点）=====")
    for i, (station_id, cnt) in enumerate(station_top10.items(), 1):
        print(f"Top{i}: {station_id} Count={cnt}")

    plt.figure(figsize=(12, 5))
    sns.heatmap(heatmap_df, annot=True, fmt=".0f", cmap="YlOrRd")

    plt.title("Service Performance Heatmap (Top10 Entities)", fontsize=14)
    plt.xlabel("Top Ranking")
    plt.ylabel("Category")

    plt.xticks(rotation=0)
    plt.savefig("performance_heatmap.png", dpi=150, bbox_inches="tight")

    print(
        """结论：从热力图可以看出客流呈现明显集中趋势，少数线路和站点承担了主要客流量，其中Top1的线路或站点显著高于其他排名，说明存在明显的核心交通枢纽。部分司机和车辆服务人次较高，可能集中在高峰线路或热门区域运营，整体分布呈现头部集中、长尾分布特征。""")