import csv
import re
import sys
import os
#############################################################################################
#handle Radio capability Excel in RS    
"""
Map Table RuDataList

RUType:xx
KRC:xx
Band:xx
numberOfTx:
numberOfRx:
L:
G:
W:
...

"""
def parseAllRUInfo(fileName):
    RuDataList = []
    #the column title in the excel
    tabInfo = []
    with open(fileName) as csvfile:
        csvreader = csv.reader(csvfile)
        bandPattern = re.compile(r'^\d+\D*')
        
        #from line 5, we have the column title info, so we jump line 1 to 4
        for i in range(4):
            csvreader.__next__()
        tabInfo = csvreader.__next__()
        #remove whitespace and return line the tabinfo string list
        for (i,s) in enumerate(tabInfo):
            tabInfo[i] = s.replace("\n", "").replace(" ", "").strip()
        #print (tabInfo)
        
        #from line 8, we have the RU data info, so here we jump line 6 and line 7
        for i in range(2):
            csvreader.__next__()
        for row in csvreader:
            if re.match(bandPattern, row[1]):
                RuData={}
                RuData["Band"] = row[tabInfo.index("Band")].replace("\n", "").strip()
                RuData["RUType"] = (row[tabInfo.index("Radio")].replace("\n", "")).replace(" ", "").strip()
                RuData["KRC"] = row[tabInfo.index("Productnumber")].replace("\n", "").strip()
                RuData["RuGroup"] = row[tabInfo.index("RadioGroup")].replace("\n", "").strip()
                RuData["OutputPower"] = row[tabInfo.index("Outputpower[W]")].replace("\n", "").strip()
                
                RuData["NumOfTx"] = row[tabInfo.index("#TX")].replace("\n", "").strip()
                RuData["NumOfRx"] = row[tabInfo.index("#RX")].replace("\n", "").strip()
                #supported RAN standard and RAN standard combination
                
                for i in range(12):
                    columnIndex = tabInfo.index("W")+i
                    RuData[tabInfo[columnIndex]]=row[columnIndex].replace("\n", "").strip()

                ##This is special, kind of hardcoded based on Excel
                ccSupportIndex = tabInfo.index("DUG20") - 2
                RuData["AnalogueCrossConnect"] = row[ccSupportIndex].replace("\n", "").strip()
                
                for i in range(17):
                    columnIndex = tabInfo.index("DUG20") + i
                    RuData[tabInfo[columnIndex]]=row[columnIndex].replace("\n", "").strip()
                    
                RuDataList.append(RuData)
              
    return RuDataList
                