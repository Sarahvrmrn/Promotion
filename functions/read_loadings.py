import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


df = pd.read_csv('loadings.csv', decimal='.', delimiter=',', index_col=0)
df_abs= df.abs()
df_sum = df_abs[df.columns[0]] + df_abs[df.columns[1]] + df_abs[df.columns[2]]
df_abs['sum'] = df_sum
print(df_abs)
print(df_sum)


#fig_df = cluster.pcaplot(x=df[0], y=df[1],  labels=df.columns.values, 
#var1=round(pca.explained_variance_ratio_[0]*100, 2), var2=round(pca.explained_variance_ratio_[1]*100, 2)) 

#fig_df.show()

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
    print(df_sort.head(10))



fig.tight_layout()
plt.show()

figPC1 = df_abs.plot()
plt.show()

