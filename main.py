from pre_process import data
from time_analyse import time_analysis
from route_analyse import analyze_route_stops,visualize
from driver_derive import driver_deriving
from ranking_statistic import ranking_statistics
a=data()
b=time_analysis()
df=a.delete()[3]

num=input('请选择要检查的任务\n输入1————展示任务一\n输入2————展示任务二\n输入3————展示任务三\n输入4————展示任务四\n输入5————展示任务五\n输入6————展示任务六\n请输入：')
try:
    num=int(num)
    if num==1:
        a.test()
        a.print_delete()
    elif num == 2:
        b.ea_to_tally()
        b.visualize_ea()
    elif num == 3:
        print(analyze_route_stops(df).head(10))
        visualize(analyze_route_stops(df))
    elif num == 4:
        b.Peak_Hour_Factor()
    elif num == 5:
        driver_deriving()
    elif num == 6:
        ranking_statistics()
    else:
        print('请在1~6中选择')
except:
    print("输入错误")