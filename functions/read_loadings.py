import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


df = pd.read_csv('loadings.csv', decimal='.', delimiter=',', index_col=0)
df_abs= df.abs()
df_sum = df_abs[df.columns[0]] + df_abs[df.columns[1]] + df_abs[df.columns[2]]
df_abs['sum'] = df_sum
print(df_abs)
print(df_sum)


fig = plt.figure(tight_layout=True, figsize=(12,8))
gs = gridspec.GridSpec(3, 1)

i = 0
for col in df.columns:
    ax = fig.add_subplot(gs[i, 0])
    ax.axhline(y = 0, color = 'r', linestyle = '-')
    ax.plot(df[col])
    ax.set_ylabel('Intensity loadings', fontsize= 7)
    ax.set_xlabel('ret. time [min]')
    ax.grid(True)
    ax.set_title(col)
    i +=1
    df_sort = df[col].sort_values(ascending=True)
    print(f'max from {col}')
    print(df_sort.head(10))



fig.tight_layout()
plt.show()

figPC1 = df_abs.plot()
plt.show()

