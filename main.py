import pandas as pd

path = "D:\\Projects\\Python\\data\\data\\"

pd.read_parquet(path+"new.parquet").to_csv(path+"new.csv", index=False,encoding='utf-8-sig')
pd.read_parquet(path+"old.parquet").to_csv(path+"old.csv",index=False,encoding='utf-8-sig')