from pre_process import data
from time_analyse import time_analysis

a=data()
a.test()
df=a.delete()

b=time_analysis()
b.ea_to_tally()
b.visualize_ea()
