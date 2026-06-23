import pandas as pd
class data:
    def __init__(self):
        self.da=self.read()

    def read(self):
        # 取消截断隐藏
        pd.set_option('display.max_columns',None)
        pd.set_option('display.width', None)
        # 读取CSV文件
        df = pd.read_csv('ICData.csv')
        return df

    def test(self):
        # 打印前五行
        print("数据集前五行：")
        print(self.da.head(5))
        # 打印行数和列数
        print(f"行数: {self.da.shape[0]}",end=' ')
        print(f"列数: {self.da.shape[1]}")
        # 2. 打印各列数据类型
        print(self.da.dtypes)

    def shift(self):
        # 将交易时间转换为datatime
        self.da['交易时间'] = pd.to_datetime(self.da['交易时间'])
        # 提取出来一列，是刷卡的具体小时，叫做hour
        self.da['hour'] = self.da['交易时间'].dt.hour
        # 提取出来一列，乘坐了多少站
        self.da['ride_stops']=(self.da["上车站点"]-self.da["下车站点"]).abs()

    def delete(self):
        self.shift()
        # 统计 ride_stops 列中 0 的个数（记录）
        zero_count = (self.da['ride_stops'] == 0).sum()
        # 删除为 0 的行
        df = self.da[self.da['ride_stops'] != 0]
        # 删除有缺失值的行
        df1 = df.isnull().sum()
        num = df1.sum()
        df_cleaned = df.dropna()

        return zero_count,df1,num,df_cleaned

    def print_delete(self):
        zero_count,df1,num,_=self.delete()
        print(f"构造ride_stops后删除异常记录(ride_stops==θ/无法计算)行数：{zero_count}")
        print()
        # 打印各列缺失值数量
        print('各列缺失值数量：')
        if num==0:
            print('无缺失值')
        else:
            print(df1)

