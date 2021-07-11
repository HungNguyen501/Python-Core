from bs4 import BeautifulSoup as bs
import pandas as pd

file_path = "D:\\Projects\\Python\\crawl_website\\CTTBK_Student_Group_Info.html"

soup = bs(open(file_path, encoding="utf8"))
list_students = soup.find_all("tr", class_="dxgvDataRow")

list_dict = []
for s in list_students:
    info = s.find_all("td")
    row = {"MSSV":info[0].text, "Ho":info[1].text, "Dem":info[2].text, "Ten":info[3].text, "Ngay sinh":info[4].text, "Lop":info[5].text, "Chuong trinh dao tao":info[6].text, "Trang thai":info[7].text}
    list_dict.append(row)

df = pd.DataFrame(list_dict)
print(df.shape)
df.to_csv("D:\\Projects\\Python\\crawl_website\\CTTBK_Student_Group_Info.csv", index=False, encoding="utf-8-sig")

