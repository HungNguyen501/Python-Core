import pandas as pd

path = "D:\\Downloads\\"

pd.read_parquet(path+"temp1.parquet").to_csv(path+"temp1.csv", index=False,encoding='utf-8-sig')
pd.read_parquet(path+"temp2.parquet").to_csv(path+"temp2.csv",index=False,encoding='utf-8-sig')