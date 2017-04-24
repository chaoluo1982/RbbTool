import csv
import re

def findAllRbbRow(fileName):
    allRbbRow = {}
    tabInfo = []
    rbbPattern = re.compile(r'.*RBB(\d{2})_\d\D.*')
    with open(fileName, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        tabInfo = csvreader.__next__()
        for (i,s) in enumerate(tabInfo):
            tabInfo[i] = s.replace("\n", "").strip()
            
        for row in csvreader:
            if re.match(rbbPattern, row[0]):
                for (i,s) in enumerate(row):
                    row[i] = s.replace("\n", " ").strip()
                rbbName = row[0]
                allRbbRow[rbbName] = row
    return (tabInfo, allRbbRow)

"""convert "RBB22_1A or RBB22_1A + RBB22_1A" to RBB22_1A"""
"""convert "RBB22_1F + RBB22_1G" to RBB22_1F, RBB22_1G"""
" problem with RBB22_2K + RBB22_2L and RBB22_2K + RBB22_2L + RBB22_2M + RBB22_2N since we will have mutiple same values with possible different release"
def rbbNameConvert(rbbName):
    rbbNameList = []
    #"RBB22_1A or RBB22_1A + RBB22_1A"
    namePattern1= re.compile(r'^RBB(\d{2})_\d\D\s*or\s*RBB(\d{2})_\d\D.*')
    #"RBB22_1F + RBB22_1G"
    namePattern2= re.compile(r'^RBB(\d{2})_\d\D\s*\+\s*RBB(\d{2})_\d\D.*')
    #RBB32_1B (new)
    namePattern3= re.compile(r'^RBB(\d{2})_\d\D\s*\(new\).*')
    if re.match(namePattern1, rbbName):
        rbbNameList.append(rbbName.split()[0])
    elif re.match(namePattern2, rbbName):
        rbbList = rbbName.split("+")
        for rbb in rbbList:
            rbbNameList.append(rbb.strip())
    elif re.match(namePattern3, rbbName):
        rbbNameList.append(rbbName.split()[0])
    else:
        rbbNameList.append(rbbName)
    return rbbNameList


"""
map
Table 1A rbbSnsmr [{RBBName:RBBxx_xx, DUType: DUxxx, RANRelease: xxx}]

"""
def parseGsmRbbSnsmr(index, rbbRow, rbbSnsmr):  
    rbbNameList = rbbNameConvert(rbbRow[index])
    #rbbNameList = [rbbRow[index]]
    for rbbName in rbbNameList:
        rbbDUG20SnsmrRelease = rbbRow[index + 3]
        if (rbbDUG20SnsmrRelease != "-") and (rbbDUG20SnsmrRelease != "?"):
            rbbSnsmrItem = {}
            rbbSnsmrItem["DUType"] = "DUG20"
            rbbSnsmrItem["RBBName"] = rbbName
            #convert RANRelease': '16B (2RX - both RX on same radio) to "G16B"
            rbbSnsmrItem["RANRelease"] = "G"+ rbbDUG20SnsmrRelease.split()[0]      
            rbbSnsmr.append(rbbSnsmrItem)
        rbbBB52125216SnsmrRelease = rbbRow[index + 7]
        if (rbbBB52125216SnsmrRelease != "-") and (rbbBB52125216SnsmrRelease != "?"):
            rbbSnsmrItem = {}
            rbbSnsmrItem["DUType"] = "BB52125216"
            rbbSnsmrItem["RBBName"] = rbbName
            rbbSnsmrItem["RANRelease"] = "G"+ rbbBB52125216SnsmrRelease.split()[0]
            rbbSnsmr.append(rbbSnsmrItem)
        rbbBB66206630SnsmrRelease = rbbRow[index + 8]
        if (rbbBB66206630SnsmrRelease != "-") and (rbbBB66206630SnsmrRelease != "?"):
            rbbSnsmrItem = {}
            rbbSnsmrItem["DUType"] = "BB66206630"
            rbbSnsmrItem["RBBName"] = rbbName
            rbbSnsmrItem["RANRelease"] = "G"+ rbbBB66206630SnsmrRelease.split()[0]
            rbbSnsmr.append(rbbSnsmrItem)
    

 



(tabInfo, allRbbRow) = findAllRbbRow("RBBs.csv")

with open("rbbInfo.txt", "w") as rbbInfofile:
    for i in tabInfo:
        rbbInfofile.write("%s\n" % i)
    rbbInfofile.write("----------------------\n")
    for (rbbName, rbbRow) in allRbbRow.items():
        rbbInfofile.write("%s\n" % rbbName)
indexForSingleModeGsm = tabInfo.index("Singel mode GSM")

"here only GSM rbbSnsmr"
rbbSnsmr=[]
for (rbbName, rbbRow) in allRbbRow.items():
    parseGsmRbbSnsmr(indexForSingleModeGsm, rbbRow, rbbSnsmr)





        