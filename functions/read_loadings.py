import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


df = pd.read_csv('loadings.csv', decimal='.', delimiter=',', index_col=0)
df_abs= df.abs()
df_sum = df_abs[df.columns[0]] + df_abs[df.columns[1]] + df_abs[df.columns[2]]
df_abs['sum'] = df_sum

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(4, 1)

i = 0
for col in df_abs.columns:
    ax = fig.add_subplot(gs[i, 0])
    ax.plot(df_abs[col])
    ax.set_ylabel('ret. time')
    ax.set_xlabel(col)
    i +=1
    df_sort = df_abs[col].sort_values(ascending=False).abs()
    print(f'max from {col}')
    print(df_sort[0:5])




fig.tight_layout()
plt.show()

