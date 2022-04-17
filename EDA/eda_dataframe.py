import pandas as pd
import sweetviz

df_file1 = pd.read_csv("Python\\EDA\\data\\file1.csv")
df_file2 = pd.read_csv("Python\\EDA\\data\\file2.csv")
# print(df_file1.info)

eda_file1 = sweetviz.analyze(source=df_file1)
eda_file1.show_html()

eda_compare = sweetviz.compare(source=df_file1, compare=df_file2)
eda_compare.show_html()