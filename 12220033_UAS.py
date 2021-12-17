#12220033 - Sigit Prabowo

import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import json
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

##START HANDLER##
class csvHandler:
    def __init__(self,Namefile):
        self.Namefile = Namefile
        df = pd.read_csv(Namefile)
        self.data = {}
        for i in df:
            self.data[i]=df[i].tolist()
        self.dataFrame = df
    def csvToJson(self,Filejson):
        df = pd.read_csv(self.Namefile)
        li = []
        for i in range(len(df)):
            row = {}
            for j in df:
                try :
                    aa = float(df[j][i])
                except:
                    aa = str(df[j][i]) 
                row[j] = aa
            li.append(row)
        with open("{}.json".format(Filejson), "w") as write_file:
            json.dump(li,write_file)

class jsonHandler:
    def __init__(self,Namefile):
        self.Namefile = Namefile
        with open(Namefile, "r") as read_file:
            self.data = json.load(read_file)
        dic = {}
        key_li = list(self.data[0].keys())
        for key in key_li:
            dic[key] = []
        for i in self.data:
            for key in key_li:
                dic[key].append(i[key])
        self.dataFrame = pd.DataFrame(dic)
    def jsonToCsv(self,csvFile):
        self.dataFrame.to_csv("{}.csv".format(csvFile),index=False)
##END HANDLER##

#HEADER
st.title("Produksi Minyak Mentah Dunia")
st.markdown("*by: Sigit Prabowo (12220033)*")

ch_ = csvHandler("produksi_minyak_mentah.csv")
jh_ = jsonHandler("kode_negara_lengkap.json")

#Nomor 1
#a
df_ = ch_.dataFrame
df_info = jh_.dataFrame
negara_1 = df_info["name"].tolist()

negara = st.selectbox("Pilih Negara : ",negara_1) 

code = df_info[df_info["name"]==negara]["alpha-3"].tolist()[0]

st.write("Kode Negara : ",code)
st.write("Negara : ",negara)

x_1 = df_[df_["kode_negara"]==code]["tahun"].tolist()
y_1 = df_[df_["kode_negara"]==code]["produksi"].tolist()

reg = LinearRegression()
reg.fit(np.array(x_1).reshape(-1,1),np.array(y_1))
m = reg.coef_[0]
c = reg.intercept_
y_trend = [m*x+c for x in x_1]
if c >= 0:
    pers = "y={m:.2f}x+{c:.2f}".format(m=m,c=c)
else:
    pers = "y={m:.2f}x{c:.2f}".format(m=m,c=c)

dic = {"tahun":x_1,"produksi":y_1}
st.write(pd.DataFrame(dic))

#plott = st.selectbox("Pilih Tipe Plotting : ",["Tipe 1","Tipe 2"])

#if plott == "Tipe 1":
plt.title("Data Produksi {}".format(negara))
plt.plot(x_1,y_1,label="Actual")
plt.plot(x_1,y_trend,label="Trendline\n{}".format(pers))
plt.xlabel("Tahun")
plt.ylabel("Produksi")
plt.legend()
st.pyplot(plt)
"""
else:
    dic["trendline"] = y_trend
    figure = px.scatter(pd.DataFrame(dic),x="tahun",y="produksi",trendline="lowess",trendline_options=dict(frac=0.1))
    st.plotly_chart(figure)
"""
#b
st.write()
st.write()
st.header("JUMLAH PRODUKSI MINYAK MENTAH TERBESAR")


B = st.sidebar.number_input("(Bagian b) Berapa Banyak Negara?", min_value=1, max_value=None)
T = st.sidebar.number_input("(Bagian b) Tahun produksi", min_value=1971, max_value=2015)

df = df_
dfJ = df_info

df = df[df["tahun"]==T]
code_negara = df[df["tahun"]==T]["kode_negara"].tolist()
# produksi = df[df['tahun']==T]['produksi'].tolist()

produksi_max = []
negara_perthn = []

code_negara = list(dict.fromkeys(code_negara))
for code in code_negara:
    try:
        produksi = df[df["kode_negara"]==code]["produksi"].tolist()
        negara = dfJ[dfJ["alpha-3"]==code]["name"].tolist()[0]
        produksi_max.append(max(produksi))
        negara_perthn.append(negara)
    except:
        continue
        
dic = {"negara":negara_perthn,"produksi_max":produksi_max}
df__ = pd.DataFrame(dic)
df__ = df__.sort_values("produksi_max",ascending=False).reset_index()

plt.clf()


plt.title("{B} Negara dengan Produksi Terbesar pada Tahun {T}".format(B=B,T=T))
plt.bar(df__["negara"][:B],df__["produksi_max"][:B],width=0.9, bottom=None, align="center",
            color="lightgreen", edgecolor="green", data=None, zorder=3)
plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)
plt.xlabel("Negara")
plt.ylabel("Produksi_Maksimum")

st.write("Input Banyak Negara dan Tahun di Sisi Kiri")
st.pyplot(plt)

#c
st.write()
st.write()
st.header("JUMLAH PRODUKSI MINYAK MENTAH TERBESAR SECARA KUMULATIF KESELURUHAN TAHUN")


B_1 = st.sidebar.number_input("(Bagian c) Berapa Banyak Negara?", min_value=1, max_value=None)

df = df_
dfJ = df_info

code_negara = df["kode_negara"].tolist()
code_negara = list(dict.fromkeys(code_negara))

jumlah_produksi = []
negara_ = []

for code in code_negara:
    try:
        produksi = df[df["kode_negara"]==code]["produksi"].tolist()
        negara = dfJ[dfJ["alpha-3"]==code]["name"].tolist()[0]
        jumlah_produksi.append(np.sum(np.array(produksi)))
        negara_.append(negara)
    except:
        continue
        
dic = {"negara":negara_,"jumlah_produksi":jumlah_produksi}
df__ = pd.DataFrame(dic)
df__ = df__.sort_values("jumlah_produksi",ascending=False).reset_index()

plt.clf()


plt.title("{B} Negara dengan Produksi Terbesar Kumulatif".format(B=B_1))
plt.bar(df__["negara"][:B_1],df__["jumlah_produksi"][:B_1],width=0.9, bottom=None, align="center",
            color="lightgreen", edgecolor="green", data=None, zorder=3)
plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)
plt.xlabel("Negara")
plt.ylabel("Jumlah_Produksi")

st.write("Input Banyak Negara di Sisi Kiri")
st.pyplot(plt)

#d
st.write()
st.write()
st.header("SUMMARY")

T_ = st.sidebar.number_input("(Bagian d) Summary Tahun Produksi", min_value=1971, max_value=2015)

df = ch_.dataFrame
dfJ = jh_.dataFrame

year = list(dict.fromkeys(df["tahun"].tolist()))

dic_max = {"negara":[],
            "kode_negara":[],
            "region":[],
            "sub_region":[],
            "produksi":[],
            "tahun":year}
dic_min = {"negara":[],
            "kode_negara":[],
            "region":[],
            "sub_region":[],
            "produksi":[],
            "tahun":year}
dic_zero = {"negara":[],
            "kode_negara":[],
            "region":[],
            "sub_region":[],
            "produksi":[],
            "tahun":year}

for t in year:
    df_per_year = df[df["tahun"]==t]
    produksi = np.array(df_per_year["produksi"].tolist())
    max_produksi = max(produksi)
    min_produksi = min([p for p in produksi if p != 0])
    nol_produksi = min([p for p in produksi if p == 0])
    # maksimum
    code_negara = df_per_year[df_per_year["produksi"]==max_produksi]["kode_negara"].tolist()[0]
    if code_negara == "WLD":
        code_negara = "WLF"
    dic_max["negara"].append(dfJ[dfJ["alpha-3"]==code_negara]["name"].tolist()[0])
    dic_max["kode_negara"].append(code_negara)
    dic_max["region"].append(dfJ[dfJ["alpha-3"]==code_negara]["region"].tolist()[0])
    dic_max["sub_region"].append(dfJ[dfJ["alpha-3"]==code_negara]["sub-region"].tolist()[0])
    dic_max["produksi"].append(max_produksi)
    # minimum != 0
    code_negara = df_per_year[df_per_year["produksi"]==min_produksi]["kode_negara"].tolist()[0]
    if code_negara == "WLD":
        code_negara = "WLF"
    dic_min["negara"].append(dfJ[dfJ["alpha-3"]==code_negara]["name"].tolist()[0])
    dic_min["kode_negara"].append(code_negara)
    dic_min["region"].append(dfJ[dfJ["alpha-3"]==code_negara]["region"].tolist()[0])
    dic_min["sub_region"].append(dfJ[dfJ["alpha-3"]==code_negara]["sub-region"].tolist()[0])
    dic_min["produksi"].append(min_produksi)
    # zero == 0
    code_negara = df_per_year[df_per_year["produksi"]==nol_produksi]["kode_negara"].tolist()[0]
    if code_negara == "WLD":
        code_negara = "WLF"
    dic_zero["negara"].append(dfJ[dfJ["alpha-3"]==code_negara]["name"].tolist()[0])
    dic_zero["kode_negara"].append(code_negara)
    dic_zero["region"].append(dfJ[dfJ["alpha-3"]==code_negara]["region"].tolist()[0])
    dic_zero["sub_region"].append(dfJ[dfJ["alpha-3"]==code_negara]["sub-region"].tolist()[0])
    dic_zero["produksi"].append(nol_produksi)

df_max = pd.DataFrame(dic_max)
df_min = pd.DataFrame(dic_min)
df_nol = pd.DataFrame(dic_zero)

st.write("Info Produksi Maksimum Tahun ke-{}".format(T_))
st.write(df_max[df_max["tahun"]==T_])

st.write("Tabel Maks Setiap Tahun")
st.write(df_max)

st.write("Info Produksi Minimum (Not Zero) Tahun ke-{}".format(T_))
st.write(df_min[df_min["tahun"]==T_])

st.write("Tabel Min (Not Zero) Setiap Tahun")
st.write(df_min)

st.write("Info Produksi Zero Tahun ke-{}".format(T_))
st.write(df_nol[df_nol["tahun"]==T_])

st.write("Tabel Zero Setiap Tahun")
st.write(df_nol)