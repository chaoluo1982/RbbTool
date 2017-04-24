import csv
import re


###########################################################################################
#rules for RU combination in RBB
#Rule for LTE, radio group compatiblility
def isRadioGroupCompatible(RuGroup1, RuGroup2):
    radioGroupPattern = re.compile(r"^([1234567])")

    RuGroup1 = re.match(radioGroupPattern, RuGroup1).group()
    RuGroup2 = re.match(radioGroupPattern, RuGroup2).group()

    if RuGroup1 == RuGroup2:
        return True

    if 1 == int(RuGroup1):
        if (3 == int(RuGroup2)) or (6 == int(RuGroup2)):
            return True
        else:
            return False
        
    if 2 == int(RuGroup1):
        if (4 == int(RuGroup2)):
            return True
        else:
            return False
    if 3 == int(RuGroup1):
        if (6 == int(RuGroup2)) or (1 == int(RuGroup2)):
            return True
        else:
            return False
    if 4 == int(RuGroup1):
        if (5 == int(RuGroup2)) or (7 == int(RuGroup2)) or (2 == int(RuGroup2)):
            return True
        else:
            return False
    if 5 == int(RuGroup1):
        if (7 == int(RuGroup2)) or (4 == int(RuGroup2)):
            return True
        else:
            return False
    if 6 == int(RuGroup1):
        if (1 == int(RuGroup2)) or (3 == int(RuGroup2)):
            return True
        else:
            return False
        
    if 7 == int(RuGroup1):
        if (4 == int(RuGroup2)) or (5 == int(RuGroup2)):
            return True
        else:
            return False


#valid RUType(might be different name) according to RuTypeNameList
# like AIR 11 B8a B20p is AIR 11
def isValidRuType(RuTypeNameList, RuType):
    for RuTypeName in RuTypeNameList:

        samePattern = re.compile(r"^" + RuTypeName + r"B.*")
        if re.match(samePattern, RuType):

            return True
    return False
  
#Rule mainremote cannot be mixed
def isMainRemote(RuType):
    mrruPattern = re.compile(r'.*mRRU.*')
    rruPattern = re.compile(r'^RRU.*')
    ruPattern = re.compile(r'^RU.*')
    airPattern = re.compile(r'^AIR.*')
    radioPattern = re.compile(r'^Radio.*')
    if re.match(mrruPattern, RuType):
        return True
    elif re.match(rruPattern, RuType): 
        return True
    elif re.match(ruPattern, RuType):
        return False
    elif re.match(airPattern, RuType):
        return True
    elif re.match(radioPattern, RuType):
        return True
    else:
        return "NotNormalRadio"

#rule, outpower <=20, must be considered as micro radio unit(small cells) cannot be mixed with >20 macro radio unit
def isMicroRadio(outputPower):
    outPutPowerPattern = re.compile(r'^\d+')
    if re.match(outPutPowerPattern, outputPower) is None:
        #raise Exception("this is an error!")
        return False
    if int(outputPower) <= 20:
        return True
    else:
        return False
    
    
#Rule cascading
def hasCascadeSupport(RuType):
    air11Pattern = re.compile(r'^AIR11.*')
    air21Pattern = re.compile(r'^AIR21.*') 
    RRUL11Pattern = re.compile(r'^RRUL11.*')
    RRUS31Pattern = re.compile(r'^RRUS31.*')
    RRU22Pattern = re.compile(r'^RRU22$')
    RRU22F2Pattern = re.compile(r'^RRU22F2.*')
    RRU22F3Pattern = re.compile(r'^RRU22F3.*')
    RRU8xPattern = re.compile(r'^RRU[LS]8.*')
    if re.match(air11Pattern, RuType):
        return False
    elif re.match(air21Pattern, RuType): 
        return False
    elif re.match(RRUL11Pattern, RuType):
        return False
    elif re.match(RRUS31Pattern, RuType):
        return False
    elif re.match(RRU22F2Pattern, RuType):
        return False
    elif re.match(RRU22F3Pattern, RuType):
        return False
    elif re.match(RRU22Pattern, RuType):
        return False
    elif re.match(RRU8xPattern, RuType):
        return False
    else:
        return True

#Rule RAN support
def hasRanSupport(supportValue):
    return (supportValue == 'X')

#Rule band compatible
def isBandCompatible(band1, band2):
    return (band1 == band2)


#Rule for DU support
def isDuTypeSupport(duType):
    if duType:
        return True
    else:
        return False


#Rule for CC support
def isAnalogueCrossConnectSupport(ccSupport):
    if ccSupport:
        return True
    else:
        return False


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
    with open(fileName, newline='') as csvfile:
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
                
################################################################################################                

class RBB:
    rbbName = ""
    allRuInfo = []
    duType = ""
    ran = ""
   
    
    def generateRBBRuList()
        getattr(self, "generateRBBRuListFor" + ran)()
        

    def print(self):
        self.printToTxt(self.duType + "_" + self.ran + "_" + self.rbbName, self.RBBRuList)
    
    def printToTxt(self, fileName, RBBRuList):
        RBBRuListWithBand = []
        RBBRuListWithoutBand = []
        for RBBRuListItem in RBBRuList:
            RBBRuListItemInfoWBand = ""
            RBBRuListItemInfoWOBand = ""
            for (i, ru) in enumerate(RBBRuListItem):
                RBBRuListItemInfoWBand += "RU%s: (RuType:%s, Band:%s, KRC:%s), " % (i+1, ru["RUType"], ru["Band"], ru["KRC"])
                RBBRuListItemInfoWOBand += "RU%s: (RuType:%s), " % (i+1, ru["RUType"])
            RBBRuListWithBand.append(RBBRuListItemInfoWBand)
            if RBBRuListItemInfoWOBand not in RBBRuListWithoutBand:
                RBBRuListWithoutBand.append(RBBRuListItemInfoWOBand)

        fileName = "%s.txt" % fileName
        with open(fileName, "w") as rbbInfofile:
            rbbInfofile.write("WithoutBandInfo:\n")
            for info in RBBRuListWithoutBand:
                rbbInfofile.write("%s\n" % info)
            rbbInfofile.write("\n\nWithBandInfo:\n")
            for info in RBBRuListWithBand:
                rbbInfofile.write("%s\n" % info)


#####################################################################################################################################                
#Typical RBB with 2RU cpri cacading and analogue Cross connect
#RBB22_1A, RBB22_2D, RBB42_1B, RBB42_2E            
class RBBSNSMRWith2RUCascadeAndCC(RBB):

    
    validRuTypeList1 = []
    validRuTypeList2 = []


    #validRuTypeList1 is for RU1
    #validRuTypeList2 is for RU2 
    def __init__(self, rbbName, duType, ran, validRuTypeList1, validRuTypeList2, allRuInfo):
        self.rbbName = rbbName
        self.validRuTypeList1 = validRuTypeList1
        self.validRuTypeList2 = validRuTypeList2
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran

    def print(self):
        self.printToTxt(self.duType + "_" + self.rbbName, self.RBBRuList) 
    
    def generateRBBRuListForW(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["W"]) and hasRanSupport(ru2["W"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                #Rule: RU1 and RU2 should support cascade
                                if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList

    def generateRBBRuListForG(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["G"]) and hasRanSupport(ru2["G"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                #Rule: RU1 and RU2 should support cascade
                                if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
                                                            
        return self.RBBRuList


    def generateRBBRuListForL(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["L"]) and hasRanSupport(ru2["L"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ):

                                #Rule: RU1 and RU2 should RU group compatible
                                if (isRadioGroupCompatible(ru1["RuGroup"], ru2["RuGroup"])):                                
                        
                                    #Rule: RU1 and RU2 should support cascade
                                    if (hasCascadeSupport(ru1["RUType"]) ):
                                        #Rule: all radios should be same remote or mainmacro, no mix
                                        if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                                #Rule: all radios should be same band
                                                if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                        #Rule: all radios should be micro or macro, no mix because of power difference
                                                        if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                            
                                                                RBBRuListItem = [ru1, ru2]
                                                                self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList                                                            

#####################################################################################################################################                
#Typical RBB with 2RU analogue Cross connect, but without cpri cascading
# RBB20_2A
# RBB22_2B, RBB22_2J
# RBB42_2D
class RBBSNSMRWith2RUCC(RBB):

    validRuTypeList1 = []
    validRuTypeList2 = []


    #validRuTypeList1 is for RU1
    #validRuTypeList2 is for RU2 
    def __init__(self, rbbName, duType, ran, validRuTypeList1, validRuTypeList2, allRuInfo):
        self.rbbName = rbbName
        self.validRuTypeList1 = validRuTypeList1
        self.validRuTypeList2 = validRuTypeList2
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran

    def print(self):
        self.printToTxt(self.duType + "_" + self.rbbName, self.RBBRuList)            
    
    def generateRBBRuListForW(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["W"]) and hasRanSupport(ru2["W"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                ##Rule: RU1 should support cascade
                                #if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList

    def generateRBBRuListForG(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["G"]) and hasRanSupport(ru2["G"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                ##Rule: RU1 should support cascade
                                #if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
                                                            
        return self.RBBRuList



    def generateRBBRuListForL(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["L"]) and hasRanSupport(ru2["L"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ):

                                #Rule: RU1 and RU2 should RU group compatible
                                if (isRadioGroupCompatible(ru1["RuGroup"], ru2["RuGroup"])):                                
                        
                                    ##Rule: RU1 should support cascade
                                    #if (hasCascadeSupport(ru1["RUType"]) ):
                                        #Rule: all radios should be same remote or mainmacro, no mix
                                        if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                                #Rule: all radios should be same band
                                                if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                        #Rule: all radios should be micro or macro, no mix because of power difference
                                                        if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                            
                                                                RBBRuListItem = [ru1, ru2]
                                                                self.RBBRuList.append(RBBRuListItem)
                                                            
        return self.RBBRuList
        
#####################################################################################################################################    
#Typical RBB with 2RU with cpri cascading, but without analog cross connect

# RBB14_1A
# RBB22_1C
# RBB24_1A, RBB24_1B
# RBB44_1B

class RBBSNSMRWith2RUCascade(RBB):

    validRuTypeList1 = []
    validRuTypeList2 = []

    #validRuTypeList1 is for RU1
    #validRuTypeList2 is for RU2 
    def __init__(self, rbbName, duType, ran, validRuTypeList1, validRuTypeList2, allRuInfo):
        self.rbbName = rbbName
        self.validRuTypeList1 = validRuTypeList1
        self.validRuTypeList2 = validRuTypeList2
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran

    def print(self):
        self.printToTxt(self.duType + "_" + self.rbbName, self.RBBRuList)        
    
    def generateRBBRuListForW(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["W"]) and hasRanSupport(ru2["W"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                #Rule: RU1 should support cascade
                                if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                                                        
                                                        if (self.rbbName == "RBB221C" and (self.duType == "DUWV1102030" or self.duType == "DUWV2113141" )):
                                                             #only support main remote radio unit for W G1
                                                             if (isMainRemote(ru1["RUType"])) and (isMainRemote(ru1["RUType"])):
                                                                 RBBRuListItem = [ru1, ru2]
                                                                 self.RBBRuList.append(RBBRuListItem)
                                                        else:                                                                                                       
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList
    
    def generateRBBRuListForG(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["G"]) and hasRanSupport(ru2["G"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                #Rule: RU1 should support cascade
                                if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList



    def generateRBBRuListForL(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["L"]) and hasRanSupport(ru2["L"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ):

                                #Rule: RU1 and RU2 should RU group compatible
                                if (isRadioGroupCompatible(ru1["RuGroup"], ru2["RuGroup"])):                                
                        
                                    #Rule: RU1 should support cascade
                                    if (hasCascadeSupport(ru1["RUType"]) ):
                                        #Rule: all radios should be same remote or mainmacro, no mix
                                        if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                                #Rule: all radios should be same band
                                                if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                        #Rule: all radios should be micro or macro, no mix because of power difference
                                                        if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                            
                                                                RBBRuListItem = [ru1, ru2]
                                                                self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList


#####################################################################################################################################    
#Typical RBB with 2RU without cpri cascading, but without analog cross connect

# RBB14_2A
# RBB22_2A, RBB22_2E
# RBB24_2A
# RBB44_2C

class RBBSNSMRWith2RU(RBB):

    validRuTypeList1 = []
    validRuTypeList2 = []


    #validRuTypeList1 is for RU1
    #validRuTypeList2 is for RU2 
    def __init__(self, rbbName, duType, ran, validRuTypeList1, validRuTypeList2, allRuInfo):
        self.rbbName = rbbName
        self.validRuTypeList1 = validRuTypeList1
        self.validRuTypeList2 = validRuTypeList2
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran
        
    def print(self):
        self.printToTxt(self.duType + "_" + self.rbbName, self.RBBRuList)
        
    def generateRBBRuListForW(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["W"]) and hasRanSupport(ru2["W"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                ##Rule: RU1 should support cascade
                                #if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList

    def generateRBBRuListForG(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["G"]) and hasRanSupport(ru2["G"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                ##Rule: RU1 should support cascade
                                #if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList                                                    



    def generateRBBRuListForL(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["L"]) and hasRanSupport(ru2["L"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ):

                                #Rule: RU1 and RU2 should RU group compatible
                                if (isRadioGroupCompatible(ru1["RuGroup"], ru2["RuGroup"])):                                
                        
                                    ##Rule: RU1 should support cascade
                                    #if (hasCascadeSupport(ru1["RUType"]) ):
                                        #Rule: all radios should be same remote or mainmacro, no mix
                                        if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                                #Rule: all radios should be same band
                                                if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                        #Rule: all radios should be micro or macro, no mix because of power difference
                                                        if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                            
                                                                RBBRuListItem = [ru1, ru2]
                                                                self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList                                                    
  

#####################################################################################################################################
# RBB with 2RU, RU2 should be RU without TX capability, RU1 should support CPRI cascading
# RBB12_1C, RBB12_1D
# RBB14_1A
# RBB24_1B


class RBBSNSMRWith2RUCascadeWithRxOnlyRU(RBB):


    validRuTypeList1 = []
    validRuTypeList2 = []


    #validRuTypeList1 is for RU1
    #validRuTypeList2 is for RU2, RX only RU    
    def __init__(self, rbbName, duType, ran, validRuTypeList1, validRuTypeList2, allRuInfo):
        self.rbbName = rbbName
        self.validRuTypeList1 = validRuTypeList1
        self.validRuTypeList2 = validRuTypeList2
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran        
        
    def print(self):
        self.printToTxt(self.duType + "_" + self.rbbName, self.RBBRuList)
        
    def generateRBBRuListForW(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["W"]) and hasRanSupport(ru2["W"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                #Rule: RU1 should support cascade
                                if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    ##Rule: all radios should be micro or macro, no mix because of power difference
                                                    #if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList

    def generateRBBRuListForG(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["G"]) and hasRanSupport(ru2["G"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                #Rule: RU1 should support cascade
                                if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
                                                            
        return self.RBBRuList



    def generateRBBRuListForL(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["L"]) and hasRanSupport(ru2["L"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ):

                                #Rule: RU1 and RU2 should RU group compatible
                                if (isRadioGroupCompatible(ru1["RuGroup"], ru2["RuGroup"])):                                
                        
                                    #Rule: RU1 should support cascade
                                    if (hasCascadeSupport(ru1["RUType"]) ):
                                        #Rule: all radios should be same remote or mainmacro, no mix
                                        if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                                #Rule: all radios should be same band
                                                if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                        #Rule: all radios should be micro or macro, no mix because of power difference
                                                        if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                            
                                                                RBBRuListItem = [ru1, ru2]
                                                                self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList                                                   
    

#####################################################################################################################################
# RBB with 2RU, RU2 should be RU without TX capability, no cpri cascading
# RBB12_2B
# RBB12_2C
# RBB14_2A
# RBB24_2B

class RBBSNSMRWith2RUWithRxOnlyRU(RBB):

    validRuTypeList1 = []
    validRuTypeList2 = []


    #validRuTypeList1 is for RU1
    #validRuTypeList2 is for RU2, RX only RU    
    def __init__(self, rbbName, duType, ran, validRuTypeList1, validRuTypeList2, allRuInfo):
        self.rbbName = rbbName
        self.validRuTypeList1 = validRuTypeList1
        self.validRuTypeList2 = validRuTypeList2
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran
        
    def print(self):
        self.printToTxt(self.duType + "_" + self.rbbName, self.RBBRuList)
        
    def generateRBBRuListForW(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["W"]) and hasRanSupport(ru2["W"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                ##Rule: RU1 should support cascade
                                #if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    ##Rule: all radios should be micro or macro, no mix because of power difference
                                                    #if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList

    def generateRBBRuListForG(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["G"]) and hasRanSupport(ru2["G"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ): 
                        
                                ##Rule: RU1 should support cascade
                                #if (hasCascadeSupport(ru1["RUType"]) ):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                        
                                                            RBBRuListItem = [ru1, ru2]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList



    def generateRBBRuListForL(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList1 = []
        validRuList2 = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList1, ru["RUType"])):
                validRuList1.append(ru)
                
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList2, ru["RUType"])):
                validRuList2.append(ru)                
        
        for ru1 in validRuList1:
            for ru2 in validRuList2:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["L"]) and hasRanSupport(ru2["L"])):
                        ##Rule: all radios should have CC support
                        #if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) ):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ):

                                #Rule: RU1 and RU2 should RU group compatible
                                if (isRadioGroupCompatible(ru1["RuGroup"], ru2["RuGroup"])):                                
                        
                                    ##Rule: RU1 should support cascade
                                    #if (hasCascadeSupport(ru1["RUType"]) ):
                                        #Rule: all radios should be same remote or mainmacro, no mix
                                        if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                                #Rule: all radios should be same band
                                                if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                        #Rule: all radios should be micro or macro, no mix because of power difference
                                                        if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):
                            
                                                                RBBRuListItem = [ru1, ru2]
                                                                self.RBBRuList.append(RBBRuListItem)
         return self.RBBRuList                                                   

        
#####################################################################################################################################                
#Typical RBB with 3RU cpri cacading and analogue Cross connect
#RBB32_1A and RBB32_1B                
class RBBSNSMRWith3RUCascadeAndCC(RBB):
    validRuList = []
    validRuTypeList = []

    
    def __init__(self, rbbName, duType, ran, validRuTypeList, allRuInfo):
        self.rbbName = rbbName
        self.validRuTypeList = validRuTypeList
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran

    def print(self):
        self.printToTxt(self.duType + "_" + self.rbbName, self.RBBRuList)

        
    def generateRBBRuListForW(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList, ru["RUType"])):
                validRuList.append(ru)
        
        for ru1 in validRuList:
            for ru2 in validRuList:
                for ru3 in validRuList:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["W"]) and hasRanSupport(ru2["W"]) and hasRanSupport(ru3["W"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru3["AnalogueCrossConnect"])):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) and isDuTypeSupport(ru3[self.duType])): 
                        
                                #Rule: RU1 and RU2 should support cascade
                                if (hasCascadeSupport(ru1["RUType"]) and hasCascadeSupport(ru2["RUType"])):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                        if (isMainRemote(ru2["RUType"]) == isMainRemote(ru3["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                if (isBandCompatible(ru2["Band"], ru3["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):  
                                                        if (isMicroRadio(ru2["OutputPower"]) == isMicroRadio(ru3["OutputPower"])):
                                                            RBBRuListItem = [ru1, ru2, ru3]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList

    def generateRBBRuListForG(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList, ru["RUType"])):
                validRuList.append(ru)
        
        for ru1 in validRuList:
            for ru2 in validRuList:
                for ru3 in validRuList:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["G"]) and hasRanSupport(ru2["G"]) and hasRanSupport(ru3["G"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru3["AnalogueCrossConnect"])):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) and isDuTypeSupport(ru3[self.duType])): 
                        
                                #Rule: RU1 and RU2 should support cascade
                                if (hasCascadeSupport(ru1["RUType"]) and hasCascadeSupport(ru2["RUType"])):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                        if (isMainRemote(ru2["RUType"]) == isMainRemote(ru3["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                if (isBandCompatible(ru2["Band"], ru3["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):  
                                                        if (isMicroRadio(ru2["OutputPower"]) == isMicroRadio(ru3["OutputPower"])):
                                                            RBBRuListItem = [ru1, ru2, ru3]
                                                            self.RBBRuList.append(RBBRuListItem)
          return self.RBBRuList     
                     
#####################################################################################################################################
#Typical RBB with 3RU with analogue Cross connect, RUs are not CPRI cascaded.
#RBB32_3A and RBB32_3B                
class RBBSNSMRWith3RUCC(RBB):
    validRuList = []
    validRuTypeList = []

    
    def __init__(self, rbbName, duType, ran, validRuTypeList, allRuInfo):
        self.rbbName = rbbName
        self.validRuTypeList = validRuTypeList
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran



      
    
    def generateRBBRuListForW(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList, ru["RUType"])):
                validRuList.append(ru)
        
        for ru1 in validRuList:
            for ru2 in validRuList:
                for ru3 in validRuList:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["W"]) and hasRanSupport(ru2["W"]) and hasRanSupport(ru3["W"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru3["AnalogueCrossConnect"])):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) and isDuTypeSupport(ru3[self.duType])): 
                        
                                ##Rule: RU1 and RU2 should support cascade
                                #if (hasCascadeSupport(ru1["RUType"]) and hasCascadeSupport(ru2["RUType"])):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                        if (isMainRemote(ru2["RUType"]) == isMainRemote(ru3["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                if (isBandCompatible(ru2["Band"], ru3["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):  
                                                        if (isMicroRadio(ru2["OutputPower"]) == isMicroRadio(ru3["OutputPower"])):
                                                            RBBRuListItem = [ru1, ru2, ru3]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList

    def generateRBBRuListForG(self):
        self.RBBRuList = []
        RBBRuListItem = []
        validRuList = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList, ru["RUType"])):
                validRuList.append(ru)
        
        for ru1 in validRuList:
            for ru2 in validRuList:
                for ru3 in validRuList:
                    #Rule: all radios should support W
                    if (hasRanSupport(ru1["G"]) and hasRanSupport(ru2["G"]) and hasRanSupport(ru3["G"])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru3["AnalogueCrossConnect"])):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) and isDuTypeSupport(ru3[self.duType])): 
                        
                                #Rule: RU1 and RU2 should support cascade
                                #if (hasCascadeSupport(ru1["RUType"]) and hasCascadeSupport(ru2["RUType"])):
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                        if (isMainRemote(ru2["RUType"]) == isMainRemote(ru3["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                if (isBandCompatible(ru2["Band"], ru3["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):  
                                                        if (isMicroRadio(ru2["OutputPower"]) == isMicroRadio(ru3["OutputPower"])):
                                                            RBBRuListItem = [ru1, ru2, ru3]
                                                            self.RBBRuList.append(RBBRuListItem)
        return self.RBBRuList
     
                             
######################################################################################################################################

######################################################################################################################################
#mixed mode case        
class RBBMM2RUSharedRU1:

    def __init__(self, duType1, ran1, duType2, ran2, RBBClass1, RBBClass2):
        self.duType1 = duType1
        self.ran1 = ran1
        self.duType2 = duType1
        self.ran2 = ran1    2
        self.rbbName1 = RBBClass1.rbbName
        self.rbbName2 = RBBClass2.rbbName
        self.rbbName1 = RBBClass1.rbbName
        self.rbbName2 = RBBClass2.rbbName

        
    def print(self):
        self.printToTxt(self.duType + "_" + self.rbbName, self.RBBRuList)
        
    def generateRBBRuListForWG(self):
        RBBRuList = self.generateRBBRuListForW()
        RBBRuList += self.generateRBBRuListForG()
        
        for RBBRuListItem in RBBRuList:
            ru1 = RBBRuListItem[0]
            if (hasRanSupport(ru1["G+W"]) and isDuTypeSupport(ru1[self.duType])
            if 
######################################################################################################################################
#main program        
        
RuDataList = parseAllRUInfo("RadioCapability.csv")


"""
map
based on RBB, RuTypelist, we find its function,
we go through all possible duType and standard,

RBBSNSMR:
{RBB2RU: (RuTypeList1, RuTypeList2, StandardList, ClassName)}
duTypelist
"""
RBB2RUMap = {}
RUTypeRBB221A = ["RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW01", "RUW02"]
RBB221AStandardList = ["W", "G"]
RBB2RUMap["RBB221A"] = (RUTypeRBB221A, RUTypeRBB221A, RBB221AStandardList, "RBBSNSMRWith2RUCascadeAndCC" )



#RBB32_1A
RUTypeRBB321A = ["RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUS01", "RUS02", "RUS03", "RUW01"]
#generate RBB32_1A RU list for DUWV1102030, single mode  
wcdmaRBB321ARuList = RBBSNSMRWith3RUCascadeAndCC("RBB321A", "DUWV1102030", RUTypeRBB321A, RuDataList)
wcdmaRBB321ARuList.generateRBBRuListForW()
#generate RBB32_1A RU list for DUG20, single mode 
gsmRBB321ARuList = RBBSNSMRWith3RUCascadeAndCC("RBB321A", "DUG20", RUTypeRBB321A, RuDataList)
gsmRBB321ARuList.generateRBBRuListForG()


#RBB32_1B
RUTypeRBB321B = ["RRUS01", "RRUS02", "RUS01", "RUS02", "RUS03"]
#generate RBB32_1B RU list for DUWV1102030, single mode  
wcdmaRBB321BRuList = RBBSNSMRWith3RUCascadeAndCC("RBB321B", "DUWV1102030", RUTypeRBB321B, RuDataList)
wcdmaRBB321BRuList.generateRBBRuListForW()
#generate RBB32_1B RU list for DUG20, single mode 
gsmRBB321BRuList = RBBSNSMRWith3RUCascadeAndCC("RBB321B", "DUG20", RUTypeRBB321B, RuDataList)
gsmRBB321BRuList.generateRBBRuListForG()

#RBB32_3A
RUTypeRBB323A = ["RRUS01", "RRUS02", "RUS01", "RUS02", "RUS03"]
#generate RBB32_3A RU list for DUG20, single mode 
gsmRBB323ARuList = RBBSNSMRWith3RUCC("RBB323A", "DUG20", RUTypeRBB323A, RuDataList)
gsmRBB323ARuList.generateRBBRuListForG()


#RBB22_1A
#AIR 11 is handled specially.

#generate RBB22_1A RU list for DUWV1102030, single mode  
wcdmaRBB221ARuList = RBBSNSMRWith2RUCascadeAndCC("RBB221A", "DUWV1102030", RUTypeRBB221A, RuDataList)
wcdmaRBB221ARuList.generateRBBRuListForW()


#RBB12_1C
RU1TypeRBB121C = ["Radio2212", "Radio2217", "Radio2219", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB121C = ["RRUSA2", "RRUSA3", "Radio0208"]
wcdmaRBB121CRuList = RBBSNSMRWith2RUCascadeWithRxOnlyRU("RBB121C", "DUWV1102030", RU1TypeRBB121C, RU2TypeRBB121C, RuDataList)
wcdmaRBB121CRuList.generateRBBRuListForW()

#RBB22_1C
RUTypeRBB221C = ["RRU22", "RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW02"]
#generate RBB22_1A RU list for DUWV1102030, single mode  
wcdmaRBB221CRuList = RBBSNSMRWith2RUCascade("RBB221C", "DUWV1102030", RUTypeRBB221C, RuDataList)
wcdmaRBB221CRuList.generateRBBRuListForW()
        