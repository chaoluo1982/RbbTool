import csv
import re
import sys
import os

###########################################################################################
#we need do some special handling regarding our suscipious input with "?"
# we choose the earliest release allowed for this (RAN, duType, RBB) and all (RAN, DUType, RU, release)
def getReleaseInfo(RBBRuListItem, duType, ran, rbbrelease):
    release = ""
    questionMark = False
    
    for ru in RBBRuListItem:
        ruRelease = ru[duType]
        if ruRelease == "?":
            questionMark = True
            continue
        if (not release):
            release = ruRelease
        else:
            if release < ruRelease:
                release = ruRelease

    if (not release):
        release = rbbrelease
    else:
        if release < rbbrelease:
            release = rbbrelease
        
    if questionMark:
        return ran + release + "?"
    else:
        return ran + release
                
                    
      
    
def getRanCombination(ran1, ran2, ruExample):
    ranCombination1 = ran1 + "+" + ran2
    ranCombination2 = ran2 + "+" + ran1
    if ranCombination1 in ruExample.keys():
        ranCombination = ranCombination1
    elif ranCombination2 in ruExample.keys():
        ranCombination = ranCombination2
    else:
        raise Exception("this is an error!")
    return ranCombination
    

            
#rules for RU combination in RBB
#Rule for LTE, radio group compatiblility
def isRadioGroupCompatible(RuGroup1, RuGroup2):
    radioGroupPattern = re.compile(r"^([1234567])")

    if re.match(radioGroupPattern, RuGroup1):
        RuGroup1 = re.match(radioGroupPattern, RuGroup1).group()
        if re.match(radioGroupPattern, RuGroup2):
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
    return True

#special limitaiton regrading ruTypes combination
#RRUW03 can only be combiend with RRUW03 and RRU22, special rules for RRUW03
#VmRRUS12 can only be combined with VmRRUS12, buliding practice limitation
def ruTypeCombinationAllowed(RuType1, RuType2):
    RuTypeNameList1 = ["RRUW03"]
    RuTypeNameList2 = ["RRUW03", "RRU22"]
    rule1 = checkruTypeCombinationRules(RuTypeNameList1, RuTypeNameList2, RuType1, RuType2)
    rule1 = rule1 and checkruTypeCombinationRules(RuTypeNameList1, RuTypeNameList2, RuType2, RuType1)

    RuTypeNameList1 = ["RIR12"]    
    RuTypeNameList2 = ["RRUS11", "RRUS12"]
    rule2 = checkruTypeCombinationRules(RuTypeNameList1, [], RuType1, RuType2)
    rule2 =  rule2 and checkruTypeCombinationRules(RuTypeNameList1, RuTypeNameList2, RuType2, RuType1)

    
    RuTypeNameList1 = ["VmRRUS12"]
    RuTypeNameList2 = ["VmRRUS12"]
    rule3 = checkruTypeCombinationRules(RuTypeNameList1, RuTypeNameList2, RuType1, RuType2)
    rule3 = rule3 and checkruTypeCombinationRules(RuTypeNameList1, RuTypeNameList2, RuType2, RuType1)

    if (rule1 and rule2 and rule3):
        return True
    else:
        return False
    
    

# when RU is in RuTypeNameList1, then other RU should be in RuTypeNameList2
def checkruTypeCombinationRules(RuTypeNameList1, RuTypeNameList2, RuType1, RuType2):
    if isValidRuType(RuTypeNameList1, RuType1):
        if isValidRuType(RuTypeNameList2, RuType2):
            return True
        else:
            return False      
    return True
        
        
    

#valid RUType(might be different name) according to RuTypeNameList
# like AIR 11 B8a B20p is AIR 11
def isValidRuType(RuTypeNameList, RuType):
    for RuTypeName in RuTypeNameList:

        pattern1 = re.compile(r"^" + RuTypeName + r"B.*")
        pattern2 = re.compile(r"^" + RuTypeName + r"$")
        if re.match(pattern1, RuType) or re.match(pattern2, RuType)  :
            return True
    return False
  
#Rule mainremote cannot be mixed
def isMainRemote(RuType):
    mrruPattern = re.compile(r'.*mRRU.*')
    rruPattern = re.compile(r'^RRU.*')
    ruPattern = re.compile(r'^RU.*')
    airPattern = re.compile(r'^AIR.*')
    radioPattern = re.compile(r'^Radio.*')
    rirPattern = re.compile(r'^RIR.*')
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
    elif re.match(rirPattern, RuType):
        return True
    else:
        return "NotNormalRadio"

#rule, outpower <=20, must be considered as micro radio unit(small cells) cannot be mixed with >20 macro radio unit
def isMicroRadio(outputPower):
    outPutPowerPattern = re.compile(r'^\d+')
    if re.match(outPutPowerPattern, outputPower) is None:
        #raise Exception("this is an error!")
        return False
    if float(outputPower) <= 15:
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
    rirPattern = re.compile(r'^RIR.*')
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
    elif re.match(rirPattern, RuType):
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
    duType = ""
    ran = ""

    def generateRBBRuList(self):
        pass

    def print(self, printDirectory):
        #map, RUTypeList: ReleaseInfo
        RBBRuListWithBand = {}
        RBBRuListWithoutBand = {}
        
        for RBBRuListItem in self.RBBRuList:
            RBBRuListItemInfoWBand = ""
            RBBRuListItemInfoWOBand = ""
            
            for (i, ru) in enumerate(RBBRuListItem):
                if i < (len(RBBRuListItem) - 1):                    
                    RBBRuListItemInfoWBand += "RU%s: (RuType:%s, Band:%s, KRC:%s), " % (i+1, ru["RUType"], ru["Band"], ru["KRC"])
                    RBBRuListItemInfoWOBand += "RU%s: (RuType:%s), " % (i+1, ru["RUType"])
            RBBRuListItemInfoWBandRelease = RBBRuListItem[-1]            
            RBBRuListWithBand[RBBRuListItemInfoWBand] = RBBRuListItemInfoWBandRelease

            #speicali handling regarding release info for same RuType
            RBBRuListItemInfoWOBandRelease = RBBRuListItem[-1]
            if RBBRuListItemInfoWOBand not in RBBRuListWithoutBand.keys():
                RBBRuListWithoutBand[RBBRuListItemInfoWOBand] = RBBRuListItemInfoWOBandRelease
            else:
                currentRelease = RBBRuListWithoutBand[RBBRuListItemInfoWOBand]
                #here currentRelease is not certain, so we rely on other reliable release info,
                #if there is no reliable release info, we choose the earliest one
                #if all release info are reliable, we still choose earliest one
                if "?" in currentRelease:
                    if "?" in RBBRuListItemInfoWOBandRelease:
                        if currentRelease > RBBRuListItemInfoWOBandRelease:
                            RBBRuListWithoutBand[RBBRuListItemInfoWOBand] = RBBRuListItemInfoWOBandRelease
                    else:
                        RBBRuListWithoutBand[RBBRuListItemInfoWOBand] = RBBRuListItemInfoWOBandRelease
                else:
                    if "?" not in RBBRuListItemInfoWOBandRelease:
                        if currentRelease > RBBRuListItemInfoWOBandRelease:
                            RBBRuListWithoutBand[RBBRuListItemInfoWOBand] = RBBRuListItemInfoWOBandRelease
                    

        try:
            os.stat(printDirectory)
        except:
            os.mkdir(printDirectory) 
                
        fileName = printDirectory + "\\" + self.duType + "\\" + self.ran + "_" + self.rbbName + ".txt"

        directory = os.path.dirname(fileName)
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)  

        with open(fileName, "w") as rbbInfofile:
            rbbInfofile.write("WithoutBandInfo:\n")
            for (ruInfo, releaseinfo) in RBBRuListWithoutBand.items():            
                rbbInfofile.write("%s %s\n" % (ruInfo, releaseinfo))
            rbbInfofile.write("\n\nWithBandInfo:\n")
            for (ruInfo, releaseinfo) in RBBRuListWithBand.items(): 
                rbbInfofile.write("%s %s\n" % (ruInfo, releaseinfo))

#####################################################################################################################################                
#Typical RBB with 1RU
class RBBSNSMRWith1RU(RBB):
    validRuTypeList = []


    def __init__(self, rbbName, rbbrelease, duType, ran, validRuTypeList, allRuInfo):
        self.rbbName = rbbName
        self.rbbrelease = rbbrelease
        self.validRuTypeList = validRuTypeList
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran
        self.RBBRuList = []
    
    def generateRBBRuList(self):
        RBBRuListItem = []
        validRuList = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList, ru["RUType"])):
                validRuList.append(ru)
            
          
        for ru in validRuList:
            #Rule: all radios should support RAN
            if (hasRanSupport(ru[self.ran])):
                #Rule support the DuType
                if (isDuTypeSupport(ru[self.duType])):
                    
                    RBBRuListItem = [ru]
                    release = getReleaseInfo(RBBRuListItem, self.duType, self.ran, self.rbbrelease)
                    RBBRuListItem = RBBRuListItem + [release]
                    self.RBBRuList.append(RBBRuListItem)
        


#####################################################################################################################################                
#Typical RBB with 2RU 

class RBBSNSMR2RU(RBB):
    validRuTypeList1 = []
    validRuTypeList2 = []

    #validRuTypeList1 is for RU1
    #validRuTypeList2 is for RU2 
    def __init__(self, rbbName, rbbrelease, duType, ran, validRuTypeList1, validRuTypeList2, allRuInfo):
        self.rbbName = rbbName
        self.rbbrelease = rbbrelease
        self.validRuTypeList1 = validRuTypeList1
        self.validRuTypeList2 = validRuTypeList2
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran
        self.RBBRuList = []
    
    def generateRBBRuList(self):
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
                #Rule: all radios should support RAN
                if (hasRanSupport(ru1[self.ran]) and hasRanSupport(ru2[self.ran])):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) ):                         
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                #handle special rules regarding ruType combination
                                                if (ruTypeCombinationAllowed(ru1["RUType"], ru2["RUType"])):
                                                        #Rule: RU1 and RU2 should RU group compatible for LTE
                                                        if (self.ran == "L") and (not isRadioGroupCompatible(ru1["RuGroup"], ru2["RuGroup"])):                                                           
                                                            continue                                                          
                                                        RBBRuListItem = [ru1, ru2]
                                                        release = getReleaseInfo(RBBRuListItem, self.duType, self.ran, self.rbbrelease)
                                                        RBBRuListItem = RBBRuListItem + [release]
                                                        self.RBBRuList.append(RBBRuListItem)

#####################################################################################################################################                
#Typical RBB with 2RU without cpri cacading and analogue Cross connect, RU2 RX only
        
# RBB with 2RU, RU2 should be RU without TX capability, no cpri cascading
# RBB12_2B
# RBB12_2C
# RBB14_2A
# RBB24_2B        
class RBBSNSMRWith2RURU2RXOnly(RBBSNSMR2RU):
    pass

                
#####################################################################################################################################                
#Typical RBB with 2RU without cpri cacading and analogue Cross connect, both capable of TX
# RBB22_2A, RBB22_2E
# RBB24_2A
# RBB44_2C          
class RBBSNSMRWith2RU(RBBSNSMR2RU):
    
    def generateRBBRuList(self):
        RBBSNSMR2RU.generateRBBRuList(self)
        RBBRuListItem = []
        newRBBRuList = []

        for RBBRuListItem in self.RBBRuList:
            if (RBBRuListItem[1]["RUType"] == "RIR12"):
                newRBBRuList.append(RBBRuListItem)
            else:
                #Rule: all radios should be micro or macro, no mix because of power difference
                if (isMicroRadio(RBBRuListItem[0]["OutputPower"]) == isMicroRadio(RBBRuListItem[1]["OutputPower"])):
                    #G1 WCDMA does not support macro radio unit for RBB22_2A
                    if (self.rbbName == "RBB222A" and (self.duType in ["DUWV1102030", "DUWV2113141"])):
                         if (isMainRemote(RBBRuListItem[0]["RUType"]) and isMainRemote(RBBRuListItem[1]["RUType"])):
                             newRBBRuList.append(RBBRuListItem)
                    else:            
                      newRBBRuList.append(RBBRuListItem)
            
                
        self.RBBRuList = newRBBRuList


#####################################################################################################################################                
#Typical RBB with 2RU cpri cacading and analogue Cross connect
#RBB22_1A, RBB22_2D, RBB42_1B, RBB42_2E            
class RBBSNSMRWith2RUCascadeAndCC(RBBSNSMR2RU):
 
    
    def generateRBBRuList(self):
        RBBSNSMR2RU.generateRBBRuList(self)
        RBBRuListItem = []
        newRBBRuList = []

        for RBBRuListItem in self.RBBRuList:
            #Rule: all radios should be micro or macro, no mix because of power difference
            if (isMicroRadio(RBBRuListItem[0]["OutputPower"]) == isMicroRadio(RBBRuListItem[1]["OutputPower"])):
                if (hasCascadeSupport(RBBRuListItem[0]["RUType"])):
                    for ru in RBBRuListItem[0:-1]:
                        if (not isAnalogueCrossConnectSupport(ru["AnalogueCrossConnect"])):
                            break
                    else:
                        newRBBRuList.append(RBBRuListItem)
        self.RBBRuList = newRBBRuList

####################################################################################################################################                
#Typical RBB with 2RU with cpri cascading, but without analog cross connect


# RBB22_1C
# RBB24_1A
# RBB44_1B
class RBBSNSMRWith2RUCascade(RBBSNSMR2RU):
    def generateRBBRuList(self):
        RBBSNSMR2RU.generateRBBRuList(self)
        RBBRuListItem = []
        newRBBRuList = []

        for RBBRuListItem in self.RBBRuList:
            #Rule: all radios should be micro or macro, no mix because of power difference
            if (isMicroRadio(RBBRuListItem[0]["OutputPower"]) == isMicroRadio(RBBRuListItem[1]["OutputPower"])):
                if (hasCascadeSupport(RBBRuListItem[0]["RUType"])):
                    #G1 WCDMA does not support macro radio unit for RBB22_1C
                    if (self.rbbName == "RBB221C" and (self.duType in ["DUWV1102030", "DUWV2113141"])):
                         if (isMainRemote(RBBRuListItem[0]["RUType"]) and isMainRemote(RBBRuListItem[1]["RUType"])):
                             newRBBRuList.append(RBBRuListItem)
                    else:            
                      newRBBRuList.append(RBBRuListItem)
        self.RBBRuList = newRBBRuList
                                                    
#################################################################################################################################### 
# RBB with 2RU, RU2 should be RU without TX capability, RU1 should support CPRI cascading
# RBB12_1C, RBB12_1D
# RBB14_1A
# RBB24_1B
class RBBSNSMRWith2RUCascadeRU2RXOnly(RBBSNSMR2RU):
    def generateRBBRuList(self):
        RBBSNSMR2RU.generateRBBRuList(self)
        RBBRuListItem = []
        newRBBRuList = []

        for RBBRuListItem in self.RBBRuList:
                if (hasCascadeSupport(RBBRuListItem[0]["RUType"])):
                      newRBBRuList.append(RBBRuListItem)
        self.RBBRuList = newRBBRuList
                                                         

#####################################################################################################################################                
#Typical RBB with 2RU analogue Cross connect, but without cpri cascading
# RBB20_2A
# RBB22_2B, RBB22_2J
# RBB42_2D

class RBBSNSMRWith2RUCC(RBBSNSMR2RU):
    def generateRBBRuList(self):
        RBBSNSMR2RU.generateRBBRuList(self)
        RBBRuListItem = []
        newRBBRuList = []

        for RBBRuListItem in self.RBBRuList:
            #Rule: all radios should be micro or macro, no mix because of power difference
            if (isMicroRadio(RBBRuListItem[0]["OutputPower"]) == isMicroRadio(RBBRuListItem[1]["OutputPower"])):
            #if (hasCascadeSupport(RBBRuListItem[0]["RUType"])):
                #the last element in RBBRuListItem is release, should not be checked
                for ru in RBBRuListItem[0:-1]:
                    if (not isAnalogueCrossConnectSupport(ru["AnalogueCrossConnect"])):
                        break
                else:
                    newRBBRuList.append(RBBRuListItem)
        self.RBBRuList = newRBBRuList

        

#####################################################################################################################################
#Typical RBB with 3RU with analogue Cross connect, RUs are not CPRI cascaded.
#RBB32_3A and RBB32_3B
#LTE has no support for 3 RU        
class RBBSNSMRWith3RUCC(RBB):
    validRuList = []
    validRuTypeList = []

    
    def __init__(self, rbbName, rbbrelease, duType, ran, validRuTypeList, allRuInfo):
        self.rbbName = rbbName
        self.rbbrelease = rbbrelease
        self.validRuTypeList = validRuTypeList
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran
        self.RBBRuList = []
      
    
    def generateRBBRuList(self):
        
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
                    if (hasRanSupport(ru1[self.ran]) and hasRanSupport(ru2[self.ran]) and hasRanSupport(ru3[self.ran])):
                        #Rule: all radios should have CC support
                        if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru3["AnalogueCrossConnect"])):
                            #Rule support the DuType
                            if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType]) and isDuTypeSupport(ru3[self.duType])): 
                                    #Rule: all radios should be same remote or mainmacro, no mix
                                    if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                        if (isMainRemote(ru2["RUType"]) == isMainRemote(ru3["RUType"])):
                                            #Rule: all radios should be same band
                                            if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                if (isBandCompatible(ru2["Band"], ru3["Band"])):
                                                    #Rule: all radios should be micro or macro, no mix because of power difference
                                                    if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):  
                                                        if (isMicroRadio(ru2["OutputPower"]) == isMicroRadio(ru3["OutputPower"])):
                                                            
                                                            #handle special rules regarding ruType combination
                                                            if (ruTypeCombinationAllowed(ru1["RUType"], ru2["RUType"])):
                                                                if (ruTypeCombinationAllowed(ru2["RUType"], ru3["RUType"])):
                                                            
                                                                    #Rule: RU1 and RU2 should RU group compatible for LTE
                                                                    if (self.ran == "L") and ((not isRadioGroupCompatible(ru1["RuGroup"], ru2["RuGroup"])) or (not isRadioGroupCompatible(ru2["RuGroup"], ru3["RuGroup"]))):                                                           
                                                                        contintue
                                                                    RBBRuListItem = [ru1, ru2, ru3]
                                                                    release = getReleaseInfo(RBBRuListItem, self.duType, self.ran, self.rbbrelease)
                                                                    RBBRuListItem = RBBRuListItem + [release]
                                                                    self.RBBRuList.append(RBBRuListItem)
        
        

        
#####################################################################################################################################                
#Typical RBB with 3RU cpri cacading and analogue Cross connect
#RBB32_1A and RBB32_1B                
class RBBSNSMRWith3RUCascadeAndCC(RBBSNSMRWith3RUCC):
    
    def generateRBBRuList(self):
        RBBSNSMRWith3RUCC.generateRBBRuList(self)
        RBBRuListItem = []
        newRBBRuList = []

        for RBBRuListItem in self.RBBRuList:
            if (hasCascadeSupport(RBBRuListItem[0]["RUType"])) and (hasCascadeSupport(RBBRuListItem[1]["RUType"])) :
                  newRBBRuList.append(RBBRuListItem)
        self.RBBRuList = newRBBRuList

    
                             
######################################################################################################################################

#####################################################################################################################################
#Typical RBB with 4RU with analogue Cross connect, RUs are not CPRI cascaded.
#RBB43_4A
      
class RBBSNSMRWith4RUCC(RBB):
    validRuList = []
    validRuTypeList = []

    
    def __init__(self, rbbName, rbbrelease, duType, ran, validRuTypeList, allRuInfo):
        self.rbbName = rbbName
        self.rbbrelease = rbbrelease
        self.validRuTypeList = validRuTypeList
        self.allRuInfo = allRuInfo
        self.duType = duType
        self.ran = ran
        self.RBBRuList = []
      
    
    def generateRBBRuList(self):
        
        RBBRuListItem = []
        validRuList = []
        
        #find all valid RU based on validRuTypeList
        for ru in self.allRuInfo:
            if (isValidRuType(self.validRuTypeList, ru["RUType"])):
                validRuList.append(ru)
        
        for ru1 in validRuList:
            for ru2 in validRuList:
                for ru3 in validRuList:
                    for ru4 in validRuList:
                        #Rule: all radios should support W
                        if (hasRanSupport(ru1[self.ran]) and hasRanSupport(ru2[self.ran])
                            and hasRanSupport(ru3[self.ran]) and hasRanSupport(ru4[self.ran])):
                            #Rule: all radios should have CC support
                            if (isAnalogueCrossConnectSupport(ru1["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru2["AnalogueCrossConnect"])
                                and isAnalogueCrossConnectSupport(ru3["AnalogueCrossConnect"]) and isAnalogueCrossConnectSupport(ru4["AnalogueCrossConnect"])):
                                #Rule support the DuType
                                if (isDuTypeSupport(ru1[self.duType]) and isDuTypeSupport(ru2[self.duType])
                                    and isDuTypeSupport(ru3[self.duType]) and isDuTypeSupport(ru4[self.duType])): 
                                        #Rule: all radios should be same remote or mainmacro, no mix
                                        if (isMainRemote(ru1["RUType"]) == isMainRemote(ru2["RUType"])):
                                            if (isMainRemote(ru2["RUType"]) == isMainRemote(ru3["RUType"])):
                                                if (isMainRemote(ru3["RUType"]) == isMainRemote(ru4["RUType"])):
                                                    #Rule: all radios should be same band
                                                    if (isBandCompatible(ru1["Band"], ru2["Band"])):
                                                        if (isBandCompatible(ru2["Band"], ru3["Band"])):
                                                            if (isBandCompatible(ru3["Band"], ru4["Band"])):
                                                                #Rule: all radios should be micro or macro, no mix because of power difference
                                                                if (isMicroRadio(ru1["OutputPower"]) == isMicroRadio(ru2["OutputPower"])):  
                                                                    if (isMicroRadio(ru2["OutputPower"]) == isMicroRadio(ru3["OutputPower"])):
                                                                        if (isMicroRadio(ru3["OutputPower"]) == isMicroRadio(ru4["OutputPower"])):                                                                        
                                                                            #handle special rules regarding ruType combination
                                                                            if (ruTypeCombinationAllowed(ru1["RUType"], ru2["RUType"])):
                                                                                if (ruTypeCombinationAllowed(ru2["RUType"], ru3["RUType"])):
                                                                                    if (ruTypeCombinationAllowed(ru3["RUType"], ru4["RUType"])):                                                                            
                                                                                        #Rule: RU1 and RU2 should RU group compatible for LTE
                                                                                        if ((self.ran == "L")
                                                                                            and ((not isRadioGroupCompatible(ru1["RuGroup"], ru2["RuGroup"]))
                                                                                                 or (not isRadioGroupCompatible(ru2["RuGroup"], ru3["RuGroup"]))
                                                                                                 or (not isRadioGroupCompatible(ru3["RuGroup"], ru4["RuGroup"])))):                                                           
                                                                                            contintue
                                                                                        RBBRuListItem = [ru1, ru2, ru3, ru4]
                                                                                        release = getReleaseInfo(RBBRuListItem, self.duType, self.ran, self.rbbrelease)
                                                                                        RBBRuListItem = RBBRuListItem + [release]
                                                                                        self.RBBRuList.append(RBBRuListItem)


#####################################################################################################################################                
#Typical RBB with 4RU cpri cacading and analogue Cross connect
#RBB43_1A                
class RBBSNSMRWith4RUCascadeAndCC(RBBSNSMRWith4RUCC):
    
    def generateRBBRuList(self):
        RBBSNSMRWith4RUCC.generateRBBRuList(self)
        RBBRuListItem = []
        newRBBRuList = []

        for RBBRuListItem in self.RBBRuList:
            if (hasCascadeSupport(RBBRuListItem[0]["RUType"])
                and (hasCascadeSupport(RBBRuListItem[1]["RUType"])) and (hasCascadeSupport(RBBRuListItem[2]["RUType"]))):
                  newRBBRuList.append(RBBRuListItem)
        self.RBBRuList = newRBBRuList


######################################################################################################################################
#mixed mode case, multi node single baseband, mixed mode radio, one RU is shared
#here assumption is that we use mixed mode release
#RBBRuList should be aggregation of two single mode cases, and remove some item accoording to rule
class RBBMM1RUShared(RBB):
    
    def __init__(self, rbbName, duType, ran, ranmmrelease, RBBRuList, sharedRuNumber, peerrbbName, peerduType, peerran, peerranmmrelease, peerRBBRuList, peersharedRuNumber):
        self.rbbName = rbbName 
        self.duType = duType
        self.ran = ran
        self.ranmmrelease = ranmmrelease
        self.RBBRuList = RBBRuList
        self.sharedRuNumber = sharedRuNumber
        self.peerrbbName = peerrbbName 
        self.peerduType = peerduType
        self.peerran = peerran
        self.peerranmmrelease = peerranmmrelease
        self.peerRBBRuList = peerRBBRuList
        self.peersharedRuNumber = peersharedRuNumber
        self.rbbName +=  "_RU" + str(self.sharedRuNumber) +"MixedModeWith_" + self.peerduType + "_" + self.peerran + "_" + self.peerrbbName
        
    def generateRBBRuList(self):
        
        RBBRuListItem = []
        peerRBBRuListItem = []
        newRBBRuList = []
        release = self.ran + self.ranmmrelease


        ranCombination = getRanCombination(self.ran, self.peerran, self.RBBRuList[0][0])
                
        
        #shared RU should support RAN combination and supported by peer(DU,RAN)
        for RBBRuListItem in self.RBBRuList:
            if (hasRanSupport(RBBRuListItem[self.sharedRuNumber - 1][ranCombination])):
                for peerRBBRuListItem in self.peerRBBRuList:
                    if (RBBRuListItem[self.sharedRuNumber - 1] == peerRBBRuListItem[self.peersharedRuNumber - 1]):

                        if release > RBBRuListItem[-1]:
                            RBBRuListItem[-1] = release

                        newRBBRuList.append(RBBRuListItem)
                        break
        self.RBBRuList = newRBBRuList        
            
##########################################################Data base input section############################################################################
     


"""
map
based on RBB, RuTypelist, we find its function,
we go through all possible duType and standard,

RBBSNSMR:
{RBB2RU: (RuTypeList1, RuTypeList2, StandardList, ClassName)}
duTypelist
"""
thisModule = sys.modules[__name__]
RuDataList = parseAllRUInfo("RadioCapability.csv")

"""
fileName = "AllRuDataFromRUCapabilities.txt"
with open(fileName, "w") as rbbInfofile:
    for info in RuDataList:
        rbbInfofile.write("%s\n" % info)
"""

duTypeListMap = {"W": ("DUWV1102030", "DUWV2113141", "6501W", "5212W", "5216W", "IDUW"),
                 "L": ("DUL20", "DUS31", "DUS41", "6501L", "5212L", "5216L", "IDUL"),
                 "G": ("DUG20", "5212G", "5216G"),
                 }
duTypeRbbMap = {}

#in chapter 2 node and sector configuration in RS
# RBB which could be used together with DuType DUWV1102030,
duTypeRbbMap["DUWV1102030"] = [("RBB101A", "15A"), ("RBB111A", "15A"), ("RBB121A", "15A"), ("RBB141A", "15A"), ("RBB142A", "15A"), ("RBB221A", "15A"), ("RBB221B", "15A"),
                               ("RBB221C", "15A"), ("RBB222A", "15A"), ("RBB222B", "15A"), ("RBB221F", "15B"),
                               ("RBB221G", "15B"), ("RBB222E", "15A"), ("RBB241A", "15A"), ("RBB241B", "15A"), ("RBB242B", "15A"), ("RBB321A", "15A"),
                               ("RBB421B", "15A"), ("RBB422D", "15A"), ("RBB441B", "15B"), ("RBB441D", "15A"), ("RBB442C", "15B")]

duTypeRbbMap["DUG20"] = [("RBB111A", "14B"), ("RBB121A", "14B"), ("RBB221A", "14B"), ("RBB221B", "14B"), ("RBB222B", "14B"), ("RBB222D", "14B"), ("RBB241A", "14B"), ("RBB242A", "14B"),
                         ("RBB323A", "14B"), ("RBB323B", "14B"), ("RBB421B", "14B"), ("RBB422D", "14B"), ("RBB422E", "14B"), ("RBB434A", "14B"), ("RBB442C", "14B")]

duTypeRbbMap["DUS41"] = [("RBB101A", "14B"), ("RBB111C", "14B"), ("RBB111D", "14B"), ("RBB112A", "14B"), ("RBB112B", "14B"), ("RBB121A", "14B"), ("RBB121C", "17A"), ("RBB121D", "17A"), ("RBB122A", "15B"), ("RBB122B", "17A"),
                         ("RBB122C", "17A"), ("RBB141A", "14B"), ("RBB142A", "14B"),
                         ("RBB201A", "14B"), ("RBB201B", "14B"), ("RBB202A", "14B"), ("RBB202B", "16B"), ("RBB221B", "14B"), ("RBB221C", "14B"), ("RBB221F", "14B"), ("RBB221G", "14B"), ("RBB221H", "14B"),
                         ("RBB222A", "14B"), ("RBB222C", "14B"), ("RBB222E", "14B"), ("RBB222K", "14B"), ("RBB222L", "14B"), ("RBB222M", "14B"),
                         ("RBB241A", "14B"), ("RBB241B", "14B"), ("RBB241C", "17A"), ("RBB242A", "14B"), ("RBB242B", "14B"), ("RBB242D", "17A"), ("RBB441B", "14B"), ("RBB441D", "14B"), ("RBB442C", "14B"), ("RBB442F", "14B")]

duTypeRbbMap["5216G"] = [("RBB101A", "16B"), ("RBB111A", "16B"), ("RBB111C", "17Q1"), ("RBB111D", "17Q1"), ("RBB121A", "16B"),  ("RBB201A", "16B"),  ("RBB202A", "16B"),  ("RBB221A", "16B"),
                         ("RBB221B", "16B"), ("RBB222B", "16B"), 
                         ("RBB241A", "16B"), ("RBB242A", "16B"), ("RBB321A", "16B"), ("RBB321B", "16B"), ("RBB323A", "16B"), ("RBB323B", "16B"), ("RBB421B", "16B"), ("RBB422D", "16B"),
                         ("RBB431A", "16B"), ("RBB434A", "16B"), ("RBB441B", "16B"), ("RBB442C", "16B")]


duTypeRbbMap["5216W"] = [("RBB101A", "16A"), ("RBB111A", "16A"), ("RBB111C", "16B"), ("RBB111D", "16B"), ("RBB121A", "16A"), ("RBB121C", "17A"), ("RBB121D", "17A"),
                         ("RBB122B", "17A"), ("RBB122C", "17A"), ("RBB141A", "17A"), ("RBB142A", "17A"),
                         ("RBB201A", "16B"), ("RBB202A", "16B"), ("RBB221A", "16B"), ("RBB221B", "16A"), ("RBB221C", "16A"), ("RBB221F", "16B"), ("RBB221G", "16B"),
                         ("RBB222A", "16A"), ("RBB222B", "16B"), ("RBB222E", "16A"), 
                         ("RBB241A", "16A"), ("RBB241B", "17A"), ("RBB242A", "16A"), ("RBB242B", "17A"), ("RBB321A", "16B"),
                         ("RBB321B", "16B"), ("RBB421B", "16B"), ("RBB422D", "16B"), ("RBB441B", "16B"), ("RBB441D", "16B"), ("RBB442C", "16B")]

duTypeRbbMap["5216L"] = [("RBB101A", "16A"), ("RBB111A", "16A"), ("RBB111C", "15B"), ("RBB111D", "15B"), ("RBB112A", "16B"), ("RBB112B", "16B"), ("RBB121A", "15B"),
                         ("RBB121C", "17A"), ("RBB121D", "17A"), ("RBB122A", "16B"), ("RBB122B", "17A"), ("RBB122C", "17A"), ("RBB141A", "16A"),
                         ("RBB142A", "16A"), ("RBB201A", "16B"), ("RBB201B", "16A"), ("RBB202A", "16B"), ("RBB202B", "16B"), ("RBB221B", "15B"), ("RBB221C", "15B"),
                         ("RBB221F", "16A"), ("RBB221G", "16A"), ("RBB221H", "16A"),
                         ("RBB222A", "15B"), ("RBB222C", "16B"), ("RBB222E", "16A"), ("RBB222K", "16B"), ("RBB222L", "16B"),
                         ("RBB241A", "16A"), ("RBB241B", "16A"), ("RBB241C", "17A"), ("RBB242A", "16A"), ("RBB242B", "16A"), ("RBB242D", "17A"),
                         ("RBB441B", "16A"), ("RBB441D", "16A"), ("RBB442C", "16A"), ("RBB442F", "16B")]


standardList = ["W", "G", "L"]

######################################## 1 RU cases in RBB ###################################################################
#RBB10_1A #RBB11_1A#RBB11_1C#RBB11_1D#RBB11_2A#RBB11_2B#RBB12_1A#RBB12_2A#RBB20_1A#RBB20_1B#RBB20_2B#RBB22_1B#RBB22_1F#RBB22_1G#RBB22_1H#RBB22_1J#RBB22_2C#RBB22_2K
#RBB22_2L#RBB22_2M#RBB22_2N#RBB24_1C#RBB24_2D#RBB44_1D#RBB44_1E#RBB44_1F#RBB44_2F#RBB44_2G#RBB44_2H#RBB88_1A#RBB88_2A


RBB1RUMap = {}

RUTypeRBB101A = ["RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW01", "RUW02"]

RUTypeRBB111A = ["AIR11", "RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW01", "RUW02"]


RUTypeRBB111C = ["AIR11", "AIR21", "RUS12mRBS6501radiopart", "mRRUS12", "mRRUS61", "Radio2203", "Radio2212", "Radio2217", "Radio2237", "Radio2218", "Radio2219", "RRU2208", "RRU2216",
                 "RRU22F1", "RRUL62", "RRUL63", "RRUS01", "RRUS02", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s", "RRUS61", "RRUS62", "RRUW02", "RUL01", "RUS01",
                 "RUS02", "RUS03", "RUW02", "VmRRUS12"]


RUTypeRBB111D= ["mRRUS12", "mRRUS61", "Radio2203", "Radio2212", "Radio2217", "Radio2218", "Radio2219", "Radio2237", "RRU2208", "RRU2216", "RRU22F1", "RRUL62", "RRUL63",
                 "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s", "RRUS61", "RRUS62", "VmRRUS12"]


RUTypeRBB112A= ["Radio2203", "Radio2212", "Radio2217", "Radio2218", "Radio2219", "RRU2208", "RRU2216", "RRUL62", "RRUL63",
                  "RRUS13", "RRUS14", "RRUS14s", "RRUS62", "RUS03"]

#why RUS03 is not here in RBB112B??
RUTypeRBB112B= ["Radio2203", "Radio2212", "Radio2217", "Radio2218", "Radio2219", "RRU2208", "RRU2216", "RRUL62", "RRUL63",
                  "RRUS13", "RRUS14", "RRUS14s", "RRUS62"]  

RUTypeRBB121A= ["AIR21", "RUS12mRBS6501radiopart", "mRRUS12", "RRU22", "RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01",
                 "RUS02", "RUS03", "RUW01", "RUW02"]

RUTypeRBB122A= ["RRUS01", "RRUS02", "RUS03"]

RUTypeRBB201A= ["RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RUTypeRBB201B= ["Radio2012", "RRUE2"]

RUTypeRBB202B= ["Radio2012"]

RUTypeRBB221B= ["IRU2242", "RUS12mRBS6501radiopart", "mRRUS12", "mRRUS61", "Radio2203", "Radio2212", "Radio2217", "Radio2218", "Radio2219", "Radio2237", "RIR12", "RRU2208", "RRU2216",
                 "RRU22F1", "RRUL11", "RRUL62", "RRUL63", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s", "RRUS61", "RRUS62", "VmRRUS12"]

RUTypeRBB221F= ["Radio4407", "Radio4412", "Radio8808", "RRU22F2", "RRU22F3", "RRUL82", "RRUS32", "RRUS72", "RRUS82"]
RUTypeRBB221G= ["Radio4407", "Radio4412", "Radio8808", "RRU22F2", "RRU22F3", "RRUL82", "RRUS32", "RRUS72", "RRUS82"]

RUTypeRBB221H= ["Radio8808", "RRU22F3", "RRUL82", "RRUS82"]
RUTypeRBB221J= ["Radio8808", "RRUL82", "RRUS82"]

RUTypeRBB222C= ["Radio2203", "Radio2212", "Radio2217", "Radio2218", "Radio2219", "RRU2208", "RRU2216", "RRUL62", "RRUL63",
                "RRUS12", "RRUS13", "RRUS14", "RRUS14s", "RRUS62"]

RUTypeRBB222K= ["Radio4407", "Radio4412", "Radio8808", "RRU22F3", "RRUL82", "RRUS32", "RRUS72", "RRUS82"]
RUTypeRBB222L= ["Radio4407", "Radio4412", "Radio8808", "RRU22F3", "RRUL82", "RRUS32", "RRUS72", "RRUS82"]

RUTypeRBB222M= ["Radio8808", "RRU22F3", "RRUL82", "RRUS82"]
RUTypeRBB222N= ["Radio8808", "RRUL82", "RRUS82"]

RUTypeRBB241C= ["AIR2488"]
RUTypeRBB242D= ["AIR2488"]

RUTypeRBB441D= ["AIR32", "Radio4407", "Radio4412", "RRUS31", "RRUS32", "RRUS72"]
RUTypeRBB441E= ["Radio8808", "RRUS82"]
RUTypeRBB441F= ["Radio8808", "RRUS82"]
RUTypeRBB442F= ["AIR32", "Radio4407", "Radio4412", "RRUS31", "RRUS32", "RRUS72"]
RUTypeRBB442G= ["Radio8808", "RRUS82"]
RUTypeRBB442H= ["Radio8808", "RRUS82"]
RUTypeRBB881A= ["Radio8808", "RRUL81", "RRUL82", "RRUS82"]
RUTypeRBB882A= ["Radio8808", "RRUL81", "RRUL82", "RRUS82"]



RUTypeAIRRBB221A = ["AIR11"]
RUTypeAIRRBB221C = ["AIR11", "AIR21"]
RUTypeAIRRBB222A = ["AIR11", "AIR21"]
RUTypeAIRRBB222B = ["AIR11"]

RUTypeAIRRBB241A = ["AIR21"]
RUTypeAIRRBB242A = ["AIR21"]


RBBListFor1RU = ["RBB101A", "RBB111A", "RBB111C", "RBB111D", "RBB112A", "RBB112B", "RBB121A", "RBB122A", "RBB201A", "RBB201B", "RBB202B",
                 "RBB221B", "RBB221F", "RBB221G", "RBB221H", "RBB221J", "RBB222C", "RBB222K", "RBB222L", "RBB222M", "RBB222N", "RBB241C",
                 "RBB242D", "RBB441D", "RBB441E", "RBB441F", "RBB442F", "RBB442G", "RBB442H", "RBB881A", "RBB882A", "AIRRBB221A", "AIRRBB221C",
                 "AIRRBB222A", "AIRRBB222B", "AIRRBB241A", "AIRRBB242A"]


for RBB in RBBListFor1RU:
    RUType = "RUType" + RBB
    RBB1RUMap[RBB] = (getattr(thisModule, RUType), "RBBSNSMRWith1RU" )
 


######################################## 2 RU cases in RBB ###################################################################
RBB2RUMap = {}
#in chapter RBB in RS
#RBB22_1A, RBB22_2D, RBB42_1B, RBB42_2E

RU1TypeRBB221A = ["RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW01", "RUW02"]
RU2TypeRBB221A = ["RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW01", "RUW02"]

RBB221ARBBClass = "RBBSNSMRWith2RUCascadeAndCC" 

RU1TypeRBB222D = ["RRUS01", "RRUS02"]
RU2TypeRBB222D = ["RRUS01", "RRUS02"]

RBB222DRBBClass = "RBBSNSMRWith2RUCascadeAndCC" 

RU1TypeRBB421B = ["RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB421B = ["RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]

RBB421BRBBClass = "RBBSNSMRWith2RUCascadeAndCC" 

RU1TypeRBB422E = ["RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB422E = ["RRUS12", "RRUS13", "RRUS14", "RRUS14s"]

RBB422ERBBClass = "RBBSNSMRWith2RUCascadeAndCC"

# RBB22_1C
# RBB24_1A
# RBB44_1B

RU1TypeRBB221C = ["RRU22", "RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW02"]
RU2TypeRBB221C = RU1TypeRBB221C

RBB221CRBBClass = "RBBSNSMRWith2RUCascade"

RU1TypeRBB241A = ["RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW01", "RUW02"]
RU2TypeRBB241A = RU1TypeRBB241A

RBB241ARBBClass = "RBBSNSMRWith2RUCascade"

RU1TypeRBB441B = ["mRRUS12", "mRRUS61", "Radio2203", "Radio2212", "Radio2217", "Radio2218", "Radio2219", "Radio2237",
                  "RRU2208", "RRU2216", "RRU22F1", "RRUL63", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s", "RRUS61", "RRUS62", "VmRRUS12"]
RU2TypeRBB441B = RU1TypeRBB441B

RBB441BRBBClass = "RBBSNSMRWith2RUCascade"

# RBB with 2RU, RU2 should be RU without TX capability, RU1 should support CPRI cascading
# RBB12_1C, RBB12_1D
# RBB14_1A
# RBB24_1B

#RBB2RUMap["RBB141A"] = (RU1TypeRBB141A, RU2TypeRBB141A, RBB141AStandardList, "RBBSNSMRWith2RUCascadeRU2RXOnly" )

RU1TypeRBB121C = ["Radio2212", "Radio2217", "Radio2219", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB121C = ["RRUSA2", "RRUSA3", "Radio0208"]

RBB121CRBBClass = "RBBSNSMRWith2RUCascadeRU2RXOnly"

RU1TypeRBB121D = ["Radio2212", "Radio2217", "Radio2219", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB121D = ["RRUSA2", "RRUSA3", "Radio0208"]

RBB121DRBBClass = "RBBSNSMRWith2RUCascadeRU2RXOnly"

RU1TypeRBB141A = ["RRUW01", "RRUW02", "RRUS01"]
RU2TypeRBB141A = ["RRUSA2", "RRUSA3", "Radio0208"]

RBB141ARBBClass = "RBBSNSMRWith2RUCascadeRU2RXOnly"

RU1TypeRBB241B = ["Radio2212", "Radio2217", "Radio2219", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB241B = ["RRUSA2", "RRUSA3", "Radio0208"]

RBB241BRBBClass = "RBBSNSMRWith2RUCascadeRU2RXOnly"


# RBB22_2A, RBB22_2E
# RBB24_2A
# RBB44_2C    
RU1TypeRBB222A = ["RRU22", "RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW02"]
RU2TypeRBB222A = ["RRU22", "RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW02"]

RBB222ARBBClass = "RBBSNSMRWith2RU"

RU1TypeRBB222E = ["mRRUS12", "Radio2203", "Radio2212", "Radio2217", "Radio2219", "Radio2237",
                  "RRU22F1", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s", "VmRRUS12"]
RU2TypeRBB222E = RU1TypeRBB222E

RBB222ERBBClass = "RBBSNSMRWith2RU"

RU1TypeRBB242A = ["RRUS01", "RRUS02", "RRUW02", "RUL01", "RUS01", "RUS02", "RUS03", "RUW02"]
RU2TypeRBB242A = RU1TypeRBB242A

RBB242ARBBClass = "RBBSNSMRWith2RU"

RU1TypeRBB442C = [ "Radio2203", "Radio2212", "Radio2217", "Radio2218", "Radio2219", "Radio2237", "mRRUS12", "mRRUS61", "RIR12",
                  "RRU2208", "RRU2216", "RRU22F1", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s", "RIR12", "RRUS61", "RRUS62", "RRUL63", "VmRRUS12"]
RU2TypeRBB442C = RU1TypeRBB442C

RBB442CRBBClass = "RBBSNSMRWith2RU"


# RBB with 2RU, RU2 should be RU without TX capability, no cpri cascading
# RBB12_2B
# RBB12_2C
# RBB14_2A
# RBB24_2B

RU1TypeRBB122B = ["Radio2212", "Radio2217", "Radio2219", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB122B = ["RRUSA2", "RRUSA3", "Radio0208"]

RBB122BRBBClass = "RBBSNSMRWith2RURU2RXOnly"

RU1TypeRBB122C = ["Radio2212", "Radio2217", "Radio2219", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB122C = ["RRUSA2", "RRUSA3", "Radio0208"]

RBB122CRBBClass = "RBBSNSMRWith2RURU2RXOnly"

RU1TypeRBB142A = ["RRUW01", "RRUW02", "RRUS01"]
RU2TypeRBB142A = ["RRUSA2", "RRUSA3", "Radio0208"]

RBB142ARBBClass = "RBBSNSMRWith2RURU2RXOnly"

RU1TypeRBB242B = ["Radio2212", "Radio2217", "Radio2219", "RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB242B = ["RRUSA2", "RRUSA3", "Radio0208"]

RBB242BRBBClass = "RBBSNSMRWith2RURU2RXOnly"

RBBListFor2RU = ["RBB221A", "RBB222D", "RBB421B", "RBB422E", "RBB221C", "RBB241A", "RBB441B", "RBB121C", "RBB121D", "RBB141A", "RBB241B", "RBB122B",
                 "RBB122C", "RBB142A", "RBB242B", "RBB222A", "RBB222E", "RBB242A", "RBB442C"]

for RBB in RBBListFor2RU:
    RU1Type = "RU1Type" + RBB
    RU2Type = "RU2Type" + RBB
    RBBClass = RBB + "RBBClass"
    #RBB2RUMap["RBB221A"] = (RUTypeRBB221A, RUTypeRBB221A, RBB221AStandardList, "RBBSNSMRWith2RUCascadeAndCC" )
    RBB2RUMap[RBB] = (getattr(thisModule, RU1Type), getattr(thisModule, RU2Type), getattr(thisModule, RBBClass) )
 
######################################## 3 RU cases in RBB ###################################################################


RBB3RUMap = {}

RUTypeRBB321A = ["RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUS01", "RUS02", "RUS03", "RUW01"]

RBB321ARBBClass = "RBBSNSMRWith3RUCascadeAndCC"
                    
RUTypeRBB321B = ["RRUS01", "RRUS02", "RUS01", "RUS02", "RUS03"]

RBB321BRBBClass = "RBBSNSMRWith3RUCascadeAndCC"

RUTypeRBB323A = ["RRUS01", "RRUS02", "RUS01", "RUS02", "RUS03"]

RBB323ARBBClass = "RBBSNSMRWith3RUCC"

RUTypeRBB323B = ["RRUS01", "RRUS02", "RUS01", "RUS02", "RUS03"]
RBB323BRBBClass = "RBBSNSMRWith3RUCC"


RBBListFor3RU = ["RBB321A", "RBB321B", "RBB323A", "RBB323B"]

for RBB in RBBListFor3RU:
    RUType = "RUType" + RBB
    RBBClass = RBB + "RBBClass"
    #RBB2RUMap["RBB221A"] = (RUTypeRBB221A, RUTypeRBB221A, "RBBSNSMRWith2RUCascadeAndCC" )
    RBB3RUMap[RBB] = (getattr(thisModule, RUType), getattr(thisModule, RBBClass) )




######################################## 4 RU cases in RBB ###################################################################
                    
RBB4RUMap = {}

RUTypeRBB431A = ["RRUS01", "RRUS02", "RUS01", "RUS02", "RUS03"]
RBB431ARBBClass = "RBBSNSMRWith4RUCascadeAndCC"

RUTypeRBB434A = ["RRUS01", "RRUS02", "RUS01", "RUS02", "RUS03"]
RBB434ARBBClass = "RBBSNSMRWith4RUCC"
                    
RBBListFor4RU = ["RBB431A", "RBB434A"]

for RBB in RBBListFor4RU:
    RUType = "RUType" + RBB
    RBBClass = RBB + "RBBClass"
    RBB4RUMap[RBB] = (getattr(thisModule, RUType), getattr(thisModule, RBBClass) )


######################################## 2A MNSBMMR in RBB ###################################################################
#MNSBMMRList
#MNSBMMRListItem (RBBInfo1, RBBInfo2)
#RBBInfo: RBBName, DUType, RAN, release, sharedRUNumber
MNSBMMR1RUSharedList = []

## MNSBMMR RBB release tables with 1 RU shared
#get this info from RS doc
" W+G MNSBMMR cases: DUWV1102030 + DUG20 "
RBBInfo1 = ["RBB221A", "DUWV1102030", "W","15A", 2]
RBBInfo2 = ["RBB111A", "DUG20", "G","14B", 1]
MNSBMMR1RUSharedList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB101A", "DUWV1102030", "W","16B", 1]
RBBInfo2 = ["RBB323A", "DUG20", "G","16B", 3]
MNSBMMR1RUSharedList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB101A", "DUWV1102030", "W","16B", 1]
RBBInfo2 = ["RBB323B", "DUG20", "G","16B", 3]
MNSBMMR1RUSharedList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB101A", "DUWV1102030", "W","16B", 1]
RBBInfo2 = ["RBB434A", "DUG20", "G","16B", 3]
MNSBMMR1RUSharedList.append((RBBInfo1, RBBInfo2))

 
               
######################################## Function ###################################################################

def generateAllSingleModeRBBRuList():
    printDirectory = ".\\rbbresult_singlemoderelease" 
    for ran in standardList:
        for duType in duTypeListMap[ran]:
            if duType in duTypeRbbMap.keys():
                #for all standard and DUType combination, we check its supported RBBs, and try to generate single mode RBBRUlist for them
                for suppportedRbb in duTypeRbbMap[duType]:
                    rbb = suppportedRbb[0]
                    rbbrelease = suppportedRbb[1]

                    if rbb in RBB1RUMap.keys() or rbb in RBB3RUMap.keys() or rbb in RBB4RUMap.keys():
                        if rbb in RBB1RUMap.keys():
                            className = RBB1RUMap[rbb][1]
                            ruTypeList = RBB1RUMap[rbb][0]
                        if rbb in RBB3RUMap.keys():
                            className = RBB3RUMap[rbb][1]
                            ruTypeList = RBB3RUMap[rbb][0]
                        if rbb in RBB4RUMap.keys():
                            className = RBB4RUMap[rbb][1]
                            ruTypeList = RBB4RUMap[rbb][0]

                        rbbClassInstance = getattr(thisModule, className)(rbb, rbbrelease, duType, ran, ruTypeList, RuDataList)
                        rbbClassInstance.generateRBBRuList()
                        rbbClassInstance.print(printDirectory)


                    if rbb in RBB2RUMap.keys():
                        className = RBB2RUMap[rbb][2]
                        ru1TypeList = RBB2RUMap[rbb][0]
                        ru2TypeList = RBB2RUMap[rbb][1]

                        rbbClassInstance = getattr(thisModule, className)(rbb, rbbrelease, duType, ran, ru1TypeList, ru2TypeList, RuDataList)
                        rbbClassInstance.generateRBBRuList()
                        rbbClassInstance.print(printDirectory)

#generate RBBMM1RUSharedRBBRuList based on RBB MM release info                        
def generateRBBMM1RUSharedRBBRuList():
    printDirectory = ".\\rbbresult_mixedmoderelease"

    for MNSBMMRListItem in MNSBMMR1RUSharedList:
        #step 1: generate single mode RBBRUList
        for (i, RBBInfo) in enumerate(MNSBMMRListItem):
            rbb = RBBInfo[0]
            ran = RBBInfo[2]
            duType = RBBInfo[1]
            ranmmrelease = RBBInfo[3]
            
            if rbb in RBB1RUMap.keys() or rbb in RBB3RUMap.keys() or rbb in RBB4RUMap.keys():
                if rbb in RBB1RUMap.keys():
                    className = RBB1RUMap[rbb][1]
                    ruTypeList = RBB1RUMap[rbb][0]
                if rbb in RBB3RUMap.keys():
                    className = RBB3RUMap[rbb][1]
                    ruTypeList = RBB3RUMap[rbb][0]
                if rbb in RBB4RUMap.keys():
                    className = RBB4RUMap[rbb][1]
                    ruTypeList = RBB4RUMap[rbb][0]

                for suppportedRbb in duTypeRbbMap[duType]:
                    #include RAN release info later    (if rbb have release info, like 15A, compare it with RuType release info) 
                    if (rbb == suppportedRbb[0]):
                        rbbrelease = suppportedRbb[1]
                        rbbClassInstance = getattr(thisModule, className)(rbb, rbbrelease, duType, ran, ruTypeList, RuDataList)
                        rbbClassInstance.generateRBBRuList()
                        MNSBMMRListItem[i].append(rbbClassInstance.RBBRuList)
                        break
            if rbb in RBB2RUMap.keys():
                className = RBB2RUMap[rbb][2]
                ru1TypeList = RBB2RUMap[rbb][0]
                ru2TypeList = RBB2RUMap[rbb][1]
                for suppportedRbb in duTypeRbbMap[duType]:
                    #include RAN release info later    (if rbb have release info, like 15A, compare it with RuType release info) 
                    if (rbb == suppportedRbb[0]):
                        rbbrelease = suppportedRbb[1]
                        rbbClassInstance = getattr(thisModule, className)(rbb, rbbrelease, duType, ran, ru1TypeList, ru2TypeList, RuDataList)
                        rbbClassInstance.generateRBBRuList()
                        MNSBMMRListItem[i].append(rbbClassInstance.RBBRuList)
                        break

        #step2: generate mixed mode RBBRUList (MNSBMMR 1RU shared)
        for i in range(2):

            rbbName = MNSBMMRListItem[i][0]
            duType = MNSBMMRListItem[i][1]
            ran = MNSBMMRListItem[i][2]
            ranmmrelease = MNSBMMRListItem[i][3]
            sharedRuNumber = MNSBMMRListItem[i][4]
            RBBRuList = MNSBMMRListItem[i][5]

            peerindex = (i+1) % 2
            peerrbbName = MNSBMMRListItem[peerindex][0]
            peerduType = MNSBMMRListItem[peerindex][1]
            peerran = MNSBMMRListItem[peerindex][2]
            peerranmmrelease = MNSBMMRListItem[peerindex][3]
            peersharedRuNumber = MNSBMMRListItem[peerindex][4]
            peerRBBRuList = MNSBMMRListItem[peerindex][5]


            mmrbbClassIntance = RBBMM1RUShared(rbbName, duType, ran, ranmmrelease, RBBRuList, sharedRuNumber, peerrbbName, peerduType, peerran, peerranmmrelease, peerRBBRuList, peersharedRuNumber)
            mmrbbClassIntance.generateRBBRuList()
            mmrbbClassIntance.print(printDirectory)

                
######################################## main program try to call function to generate result ###################################################################

#generateAllSingleModeRBBRuList()

generateRBBMM1RUSharedRBBRuList()