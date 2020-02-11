import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
root = tk.Tk()
root.withdraw()
Path2BoM = filedialog.askopenfilename().replace("/","\\")
BoM = pd.DataFrame(pd.read_csv(Path2BoM,error_bad_lines=False,sep=";")).fillna('')

res_base = "https://lv.farnell.com/w/c/passive-components/resistors-fixed-value/"
res_tht = "through-hole-resistors"
res_smd = "chip-smd-resistors"
res_end = "?"
res_param1 = "resistance="
res_param2 = "resistance-tolerance="
res_param3 = "resistor-case-style="
res_param4 = "power-rating="
res_param5 = "voltage-rating="
res_param6 = "resistor-element-type="
res_param7 = "temperature-coefficient="
res_type = {
    "Base":'',
    "THT":res_tht,
    "SMD":res_smd,
}

cap_base = "https://lv.farnell.com/w/c/passive-components/capacitors/"
ceramic = "ceramic-capacitors/"
ceramic_tht = "leaded-ceramic-multilayer-mlcc-capacitors/"
ceramic_smd = "smd-ceramic-multilayer-mlcc-capacitors/"

elect = "aluminium-electrolytic-capacitors/"
elect_tht = "leaded-aluminium-electrolytic-capacitors/"
elect_smd = "smd-aluminium-electrolytic-capacitors/"

film = "film-capacitors/"

tantalum = "tantalum-capacitors/"
tantalum_tht = "leaded-tantalum-capacitors/"
tantalum_smd = "smd-tantalum-capacitors/"

cap_end = "prl/results?"

cap_param1 = "capacitance="
cap_param2 = "voltage-rating="
cap_param3 = "ceramic-capacitor-case="
cap_param4 = "capacitance-tolerance="

cer_cap_base = {
    "Base":ceramic,
    "THT":ceramic_tht,
    "SMD":ceramic_smd
}
elect_cap_base = {
    "Base":elect,
    "THT":elect_tht,
    "SMD":elect_smd
}
film_cap_base = {
    "Base":film,
    "THT":'',
    "SMD":''
}
tantalum_cap_base = {
    "Base":tantalum,
    "THT":tantalum_tht,
    "SMD":tantalum_smd
}  

case_style = {
    "01005":"01005-0402-metric-",
    "0201":"0201-0603-metric-",
    "0402":"0402-1005-metric-",
    "0406":"0406-1016-metric-",
    "0508":"0508-1220-metric-",
    "0603":"0603-1608-metric-",
    "0612":"0612-1632-metric-",
    "0805":"0805-2012-metric-",
    "1020":"1020-2550-metric-",
    "1206":"1206-3216-metric-",
    "1206":"1206-3216-metric-",
    "1210":"1210-3225-metric-",
    "1218":"1218-3045-metric-",
    "1225":"1225-3064-metric-",
    "1812":"1812-4532-metric-",
    "2010":"2010-5025-metric-",
    "2512":"2512-6432-metric-",
}

cap_dict = {
    "Base":cap_base,
    "Ceramic":cer_cap_base,
    "Electrolytic":elect_cap_base,
    "Film":film_cap_base,
    "Tantalum":tantalum_cap_base,
    "End":cap_end,
    "Value":cap_param1,
    "Voltage":cap_param2,
    "Footprint":cap_param3,
    "Tol":cap_param4
}
res_dict = {
    "Base":res_base,
    "Res":res_type,
    "End":res_end,
    "Value":res_param1,
    "Tol":res_param2,
    "Footprint":res_param3,
    "Power":res_param4,
    "Voltage":res_param5,
    #"Type":res_param6,
    "Temperature":res_param7,
    #"Res":dict()
}

packaging="packaging=each|cuttape"
available= "range=inc-in-stock"
search = "st="
sorting = "sort=P_PRICE"
query_dict = {
    "Resistor":res_dict,
    "Capacitor":cap_dict,
    }
Search = {
    "Search":"https://lv.farnell.com/search?st="
}

links2farnell = np.empty(0)
for index, line in BoM.iterrows():
    component = query_dict.get(line['Description'],Search)
    link = ""
    if(component is not Search):
        if(line["Description"] == "Resistor"):
            line["Value"] = line["Value"].replace("K","k")
            line["Value"] += "ohm"
        if(line["Description"] == "Capacitor"):
            line["Value"] = line["Value"].replace("F","f")
        link += component.get("Base")
        link += component.get(line["Type"]).get("Base")
        link += component.get(line["Type"]).get(line["PackageDescription"])
        link += component.get("End")
        link += component.get("Value",'') + line.get("Value") + "&"
        link += component.get("Tol",'') + line.get("Tol",'') + "&"
        link += component.get("Footprint",'') + case_style.get(line.get("Footprint",''),'') + "&"
        link += component.get("Power",'') + line.get("Power",'') + "&"
        link += component.get("Voltage",'') + line.get("Voltage",'') + "&"
        link += component.get("Temperature",'') + line.get("Temperature",'') + "&"
        link += packaging + "&"
        link += available + "&"
        link += sorting + "&"
    else:
        link += component.get("Search") + line['DesignItemId'] + "&"
        link += packaging + "&"
        link += available + "&"
        link += sorting + "&"
    links2farnell = np.append(links2farnell,link)
BoM["Links"] = links2farnell
BoM.to_csv(Path2BoM,index=False,sep=";")