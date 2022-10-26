import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix
import seaborn as sns
from matplotlib import pyplot as plt
path = 'C:\\Users\\sverme-adm\\Desktop\\data_neu\\results\\25-10-2022_14-30-08_results.csv'


# prepare data
# x as array 2d
# y as numbers, one for every unique value
df = pd.read_csv(path, delimiter='\t', decimal='.')
df.drop('date', axis=1, inplace=True)
y_str = df['name']
df.drop('name', axis=1, inplace=True)
x = df.values.tolist()

y_str_u = y_str.unique().tolist() #  identify names of uniqew samples
sample_dict = {} # create dict to classify numbers to specimen
for i in range(len(y_str_u)):
    sample_dict[y_str_u[i]] = i
print(sample_dict)

y = [sample_dict[i] for i in y_str] #creates a list with numbers as label for lda 

predictions = []
lda = LinearDiscriminantAnalysis(n_components=3)
for i in range(len(x)):
    _x = x.copy()
    _y = y.copy()
    test_x = _x.pop(i) 
    test_y = _y.pop(i) 
    lda.fit(_x, _y)
    new_item = [lda.predict(np.array(test_x).reshape(1, -1))[0], test_y]
    predictions.append(new_item)

print(predictions)
true_cnt = 0
for i in predictions:
    if i[0] == i[1]:
        true_cnt += 1
print((true_cnt/len(x))*100)


y_test = [i[1] for i in predictions]
y_pred = [i[0] for i in predictions]

print(y_test)
print(y_pred)

cm = confusion_matrix(y_test, y_pred)
print(cm)
sns.heatmap(cm, annot=True)
plt.show()
