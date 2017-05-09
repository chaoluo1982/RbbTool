import csv
import re
import sys
import os
from RadioCapabilityCSVhandling import *
from RbbRules import *
from RbbClass import *
from RbbInfoDataBase import *



thisModule = sys.modules[__name__]
RuDataList = parseAllRUInfo("RadioCapability.csv")

"""
fileName = "AllRuDataFromRUCapabilities.txt"
with open(fileName, "w") as rbbInfofile:
    for info in RuDataList:
        rbbInfofile.write("%s\n" % info)
"""


               
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
def generateRBBMNSBMMRRBBRuList():
    printDirectory = ".\\rbbresult_mnsbmixedmoderelease"

    for MNSBMMRListItem in MNSBMMRRbbInfoList:
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

                    #here we do not care whether the RBB is released or not in the SNSMR case

                    

                rbbrelease = ""
                rbbClassInstance = getattr(thisModule, className)(rbb, rbbrelease, duType, ran, ruTypeList, RuDataList)
                rbbClassInstance.generateRBBRuListWithoutRanCheck()
                MNSBMMRListItem[i].append(rbbClassInstance.RBBRuList)

            if rbb in RBB2RUMap.keys():
                className = RBB2RUMap[rbb][2]
                ru1TypeList = RBB2RUMap[rbb][0]
                ru2TypeList = RBB2RUMap[rbb][1]
                #here we do not care whether the RBB is released or not in the SNSMR case

                rbbrelease = ""
                rbbClassInstance = getattr(thisModule, className)(rbb, rbbrelease, duType, ran, ru1TypeList, ru2TypeList, RuDataList)
                rbbClassInstance.generateRBBRuListWithoutRanCheck()
                MNSBMMRListItem[i].append(rbbClassInstance.RBBRuList)


        #step2: generate mixed mode RBBRUList (MNSBMMR 1RU shared) for both RBB involved inthis mixed mode case
        for i in range(2):

            rbbName = MNSBMMRListItem[i][0]
            duType = MNSBMMRListItem[i][1]
            ran = MNSBMMRListItem[i][2]
            ranmmrelease = MNSBMMRListItem[i][3]
            sharedRuNumberList = MNSBMMRListItem[i][4]
            RBBRuList = MNSBMMRListItem[i][5]

            peerindex = (i+1) % 2
            peerrbbName = MNSBMMRListItem[peerindex][0]
            peerduType = MNSBMMRListItem[peerindex][1]
            peerran = MNSBMMRListItem[peerindex][2]
            peerranmmrelease = MNSBMMRListItem[peerindex][3]
            peersharedRuNumberList = MNSBMMRListItem[peerindex][4]
            peerRBBRuList = MNSBMMRListItem[peerindex][5]



            mmrbbClassIntance = RBBMNSBMMR(rbbName, duType, ran, ranmmrelease, RBBRuList, sharedRuNumberList, peerrbbName, peerduType, peerran, peerranmmrelease, peerRBBRuList, peersharedRuNumberList)
            mmrbbClassIntance.generateRBBRuList()
            mmrbbClassIntance.print(printDirectory)

#generate RBBSNMBMMRRBBRuList based on RBB MM release info                        
def generateRBBSNMBMMRRBBRuList():
    printDirectory = ".\\rbbresult_snmbmixedmoderelease"

    for RBBInfo in SNMBMMRRbbInfoList:
        #make sure all input is capital case
        rbb = RBBInfo[0].upper()
        duTypeInfo = RBBInfo[1]
        ran = RBBInfo[2]
        peerran = RBBInfo[3]
        mmrelease = RBBInfo[4]
        ranList = [ran, peerran]
        
        for ranItem in ranList:
            RBBRuList = []
            duType = duTypeInfo + ranItem

        #step 1: generate single mode RBBRUList


            
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


                #here we do not care whether the RBB is released or not in the SNSMR case
                rbbrelease = ""
                rbbClassInstance = getattr(thisModule, className)(rbb, rbbrelease, duType, ranItem, ruTypeList, RuDataList)
                rbbClassInstance.generateRBBRuListWithoutRanCheck()
                RBBRuList = rbbClassInstance.RBBRuList
                    
            if rbb in RBB2RUMap.keys():
                className = RBB2RUMap[rbb][2]
                ru1TypeList = RBB2RUMap[rbb][0]
                ru2TypeList = RBB2RUMap[rbb][1]

                #here we do not care whether the RBB is released or not in the SNSMR case
                rbbrelease = ""
                rbbClassInstance = getattr(thisModule, className)(rbb, rbbrelease, duType, ranItem, ru1TypeList, ru2TypeList, RuDataList)
                rbbClassInstance.generateRBBRuListWithoutRanCheck()
                RBBRuList = rbbClassInstance.RBBRuList
                
            RBBInfo.append(RBBRuList)

        #step2: generate mixed mode RBBRUList (MNSBMMR 1RU shared) for both RBB involved in this mixed mode case

        RBBRuList = RBBInfo[-2]
        peerRBBRuList = RBBInfo[-1]
        mmrbbClassIntance = RBBSNMBMMR(rbb, duTypeInfo, ran, mmrelease, RBBRuList,  peerran, peerRBBRuList)
        mmrbbClassIntance.generateRBBRuList()
        mmrbbClassIntance.print(printDirectory)
                
#generate RBBMNMBMMRRBBRuList based on RBB MM release info
#Triple Mixed Mode
#for simplification, assume there is no case, that RU can only support triple mixed mode, but cannnot support 2 standard mixed mode, 
def generateRBBMNMBMMRRBBRuList():
    printDirectory = ".\\rbbresult_mnmbmixedmoderelease"

    for MNMBMMRListItem in MNMBMMRRbbInfoList:
        
        #step 1: generate mixed mode baseband RBBRUList
        mbRBBRuList = []
        mbrbbInfo = MNMBMMRListItem[0]

        mbrbb = mbrbbInfo[0].upper()
        mbduTypeInfo = mbrbbInfo[1]
        mbran = mbrbbInfo[2]
        mbpeerran = mbrbbInfo[3]
        mbrelease = mbrbbInfo[5]
        mbsharedRuNumberList = mbrbbInfo[4]
        mbranList = [mbran, mbpeerran]
        
        for ranItem in mbranList:
            RBBRuList = []
            #mixed mode baseband dutype info need add ran
            duType = mbduTypeInfo + ranItem

        #step 1: generate single mode RBBRUList with RAN checking        
            if mbrbb in RBB1RUMap.keys() or mbrbb in RBB3RUMap.keys() or mbrbb in RBB4RUMap.keys():
                if mbrbb in RBB1RUMap.keys():
                    className = RBB1RUMap[mbrbb][1]
                    ruTypeList = RBB1RUMap[mbrbb][0]
                if mbrbb in RBB3RUMap.keys():
                    className = RBB3RUMap[mbrbb][1]
                    ruTypeList = RBB3RUMap[mbrbb][0]
                if mbrbb in RBB4RUMap.keys():
                    className = RBB4RUMap[mbrbb][1]
                    ruTypeList = RBB4RUMap[mbrbb][0]


                #here we do not care whether the RBB is released or not in the SNSMR case
                rbbrelease = ""
                rbbClassInstance = getattr(thisModule, className)(mbrbb, rbbrelease, duType, ranItem, ruTypeList, RuDataList)
                rbbClassInstance.generateRBBRuListWithoutRanCheck()
                RBBRuList = rbbClassInstance.RBBRuList
                
            if mbrbb in RBB2RUMap.keys():
                className = RBB2RUMap[mbrbb][2]
                ru1TypeList = RBB2RUMap[mbrbb][0]
                ru2TypeList = RBB2RUMap[mbrbb][1]

                #here we do not care whether the RBB is released or not in the SNSMR case
                rbbrelease = ""
                rbbClassInstance = getattr(thisModule, className)(mbrbb, rbbrelease, duType, ranItem, ru1TypeList, ru2TypeList, RuDataList)
                rbbClassInstance.generateRBBRuListWithoutRanCheck()
                RBBRuList = rbbClassInstance.RBBRuList
                
            mbrbbInfo.append(RBBRuList)

            

        #step2: generate mixed mode baseband RBBRUList 
        mbRBBRuList = mbrbbInfo[-2]
        mbpeerRBBRuList = mbrbbInfo[-1]
        mmrbbClassIntance = RBBSNMBMMR(mbrbb, mbduTypeInfo, mbran, "", mbRBBRuList,  mbpeerran, mbpeerRBBRuList)
        mmrbbClassIntance.generateRBBRuList()
        
        mbRBBRuList = mmrbbClassIntance.RBBRuList
        mbran = getRanCombination(mbran, mbpeerran, mbRBBRuList[0][0])


        #step3: handle the single baseband RBB
        sbRBBRuList =[]
        sbrbbInfo = MNMBMMRListItem[1]
        sbrbb = sbrbbInfo[0].upper()
        sbran = sbrbbInfo[2]
        sbduType = sbrbbInfo[1]
        sbrelease = sbrbbInfo[4]
        sbsharedRuNumberList = sbrbbInfo[3]
            
        if sbrbb in RBB1RUMap.keys() or sbrbb in RBB3RUMap.keys() or sbrbb in RBB4RUMap.keys():
            if sbrbb in RBB1RUMap.keys():
                className = RBB1RUMap[sbrbb][1]
                ruTypeList = RBB1RUMap[sbrbb][0]
            if sbrbb in RBB3RUMap.keys():
                className = RBB3RUMap[sbrbb][1]
                ruTypeList = RBB3RUMap[sbrbb][0]
            if sbrbb in RBB4RUMap.keys():
                className = RBB4RUMap[sbrbb][1]
                ruTypeList = RBB4RUMap[sbrbb][0]

                    #here we do not care whether the RBB is released or not in the SNSMR case

                    

            rbbrelease = ""
            rbbClassInstance = getattr(thisModule, className)(sbrbb, rbbrelease, sbduType, sbran, ruTypeList, RuDataList)
            rbbClassInstance.generateRBBRuListWithoutRanCheck()
            sbRBBRuList = rbbClassInstance.RBBRuList

        if sbrbb in RBB2RUMap.keys():
            className = RBB2RUMap[sbrbb][2]
            ru1TypeList = RBB2RUMap[sbrbb][0]
            ru2TypeList = RBB2RUMap[sbrbb][1]
                #here we do not care whether the RBB is released or not in the SNSMR case

            rbbrelease = ""
            rbbClassInstance = getattr(thisModule, className)(sbrbb, rbbrelease, sbduType, sbran, ru1TypeList, ru2TypeList, RuDataList)
            rbbClassInstance.generateRBBRuListWithoutRanCheck()
            sbRBBRuList = rbbClassInstance.RBBRuList


        #step4: generate triple mixed mode RBBRUList
                
                
      
        mmrbbClassIntance = RBBMNMBMMR(mbrbb, mbduTypeInfo, mbran, mbrelease, mbRBBRuList, mbsharedRuNumberList, sbrbb, sbduType, sbran, sbrelease, sbRBBRuList, sbsharedRuNumberList)
        mmrbbClassIntance.generateRBBRuList()
        mmrbbClassIntance.print(printDirectory)

        mmrbbClassIntance = RBBMNMBMMR(sbrbb, sbduType, sbran, sbrelease, sbRBBRuList, sbsharedRuNumberList, mbrbb, mbduTypeInfo, mbran, mbrelease, mbRBBRuList, mbsharedRuNumberList)
        mmrbbClassIntance.generateRBBRuList()
        mmrbbClassIntance.print(printDirectory)

######################################## main program try to call function to generate result ###################################################################

#generateAllSingleModeRBBRuList()

generateRBBMNSBMMRRBBRuList()

#generateRBBSNMBMMRRBBRuList()

#generateRBBMNMBMMRRBBRuList()