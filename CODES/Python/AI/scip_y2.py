from scipy import stats
data1 = [2.5, 3.5, 3.0, 4.0]
data2 = [3.0, 4.0, 2.0, 5.0]

t_stat, p_value = stats.ttest_ind(data1, data2)
print("t-statistic:", t_stat, "p-value:", p_value)
