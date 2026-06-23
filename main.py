from pre_process import data
from time_analyse import time_analysis
from route_analyse import analyze_route_stops,visualize
from driver_derive import driver_deriving

a=data()
a.test()
df=a.delete()[3]
a.print_delete()


b=time_analysis()
b.ea_to_tally()
b.visualize_ea()


print(analyze_route_stops(df).head(10))
visualize(analyze_route_stops(df))


b.Peak_Hour_Factor()


driver_deriving()