import os

def driver_deriving():
    from pre_process import data
    a = data()
    df = a.delete()[3]
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