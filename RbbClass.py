
import csv
import re
import sys
import os

from RbbRules import *


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
class RBBMNSBMMR(RBB):
    
    def __init__(self, rbbName, duType, ran, ranmmrelease, RBBRuList, sharedRuNumberList, peerrbbName, peerduType, peerran, peerranmmrelease, peerRBBRuList, peersharedRuNumberList):
        self.rbbName = rbbName 
        self.duType = duType
        self.ran = ran
        self.ranmmrelease = ranmmrelease
        self.RBBRuList = RBBRuList
        self.sharedRuNumberList = sharedRuNumberList
        self.peerrbbName = peerrbbName 
        self.peerduType = peerduType
        self.peerran = peerran
        self.peerranmmrelease = peerranmmrelease
        self.peerRBBRuList = peerRBBRuList
        self.peersharedRuNumberList = peersharedRuNumberList
        
        if len(sharedRuNumberList) != len(peersharedRuNumberList):
            raise Exception("this is an error for shared RU number list!")
        self.rbbName += "_"
        for sharedRuNumber in self.sharedRuNumberList:
            self.rbbName += "RU" + str(sharedRuNumber)
        self.rbbName += "_MixedModeWith_"
        for sharedRuNumber in self.peersharedRuNumberList:
            self.rbbName += "RU" + str(sharedRuNumber)
        self.rbbName += "_In_" + self.peerduType + "_" + self.peerran + "_" + self.peerrbbName

        
        
    def generateRBBRuList(self):
        
        RBBRuListItem = []
        peerRBBRuListItem = []
        newRBBRuList = []
        release = self.ran + self.ranmmrelease


        ranCombination = getRanCombination(self.ran, self.peerran, self.RBBRuList[0][0])
                
        
        #shared RU should support RAN combination and supported by peer(DU,RAN)
        for RBBRuListItem in self.RBBRuList:
            isValidRBBRuListItem = 0
            for (i, sharedRuNumber) in enumerate(self.sharedRuNumberList):
                if (not hasRanSupport(RBBRuListItem[sharedRuNumber - 1][ranCombination])):
                    #get out this for loop for self.sharedRuNumberList because RAN combination does not support it
                    break
                
                for peerRBBRuListItem in self.peerRBBRuList:
                    #for shared RU number list like (2,3) will be compared with peer (1,2), and RU2 will be mapping to peer RBB RU1 just as the list sequence
                    if (RBBRuListItem[sharedRuNumber - 1] == peerRBBRuListItem[self.peersharedRuNumberList[i] - 1]):
                        #break out from this inner loop for peer RBB RU, and continue outer for loop
                        break
                else:
                    #get out this for loop for self.sharedRuNumberList because RU is not supported by peer RBB
                    break
            else:
                #go through all self.sharedRuNumberList checking, all conditions are OK
                if release > RBBRuListItem[-1]:
                    RBBRuListItem[-1] = release
                newRBBRuList.append(RBBRuListItem)

                
        self.RBBRuList = newRBBRuList        

######################################################################################################################################
#RBBSNMBMMR
class RBBSNMBMMR(RBB):
    
    def __init__(self, rbbName, duType, ran, mmrelease, RBBRuList, peerran, peerRBBRuList):
        self.rbbName = rbbName 
        self.duType = duType
        self.ran = ran
        self.mmrelease = mmrelease
        self.RBBRuList = RBBRuList
        self.peerran = peerran
        self.peerRBBRuList = peerRBBRuList
        self.RBBRuList += self.peerRBBRuList 


        self.rbbName += "_mixedmodebasband_" + self.peerran 

        
        
    def generateRBBRuList(self):
        
        RBBRuListItem = []
        peerRBBRuListItem = []
        newRBBRuList = []


        ranCombination = getRanCombination(self.ran, self.peerran, self.RBBRuList[0][0])
                
        
        #shared RU should support RAN combination and supported by peer(DU,RAN)
        for RBBRuListItem in self.RBBRuList:
            #here we only check whether any of the item support RAN combination
            for ru in RBBRuListItem[0:-1]:
                if hasRanSupport(ru[ranCombination]):
                    mmrelease = RBBRuListItem[-1][1:]
                    if self.mmrelease > mmrelease:
                        RBBRuListItem[-1] = self.mmrelease
                    else:
                        RBBRuListItem[-1] = mmrelease
                    newRBBRuList.append(RBBRuListItem)
                    break
                
        self.RBBRuList = newRBBRuList        
            