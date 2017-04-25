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
    printDirectory = ".\\rbbresult_mixedmoderelease"

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

                
######################################## main program try to call function to generate result ###################################################################

#generateAllSingleModeRBBRuList()

generateRBBMNSBMMRRBBRuList()