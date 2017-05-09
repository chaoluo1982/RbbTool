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
    #in case table info is wrong, that RU is not released for this (DUType, RAN), in cases like AIR32 which only exist in mixed mode cases?
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
    if ("+" not in ran1) and ("+" not in ran2):
        ranCombination1 = ran1 + "+" + ran2
        ranCombination2 = ran2 + "+" + ran1
        if ranCombination1 in ruExample.keys():
            ranCombination = ranCombination1
            return ranCombination
        elif ranCombination2 in ruExample.keys():
            ranCombination = ranCombination2
            return ranCombination
        else:
            raise Exception("this is an error!")
        
    if ("+" in ran1) and ("+" not in ran2):
        [ranStandard1, ranStandard2] = ran1.split("+")
        ranStandard3 = ran2
        for rans1 in [ranStandard1, ranStandard2, ranStandard3]:
            for rans2 in [ranStandard1, ranStandard2, ranStandard3]:
                for rans3 in [ranStandard1, ranStandard2, ranStandard3]:
                    if (rans1 != rans2) and (rans2 != rans3) and (rans1 != rans3):
                        ranCombination = rans1 + "+" + rans2 + "+" + rans3
                        if ranCombination in ruExample.keys():
                            return ranCombination                        
    if ("+" in ran2) and ("+" not in ran1):
        [ranStandard1, ranStandard2] = ran2.split("+")
        ranStandard3 = ran1
        for rans1 in [ranStandard1, ranStandard2, ranStandard3]:
            for rans2 in [ranStandard1, ranStandard2, ranStandard3]:
                for rans3 in [ranStandard1, ranStandard2, ranStandard3]:
                    if (rans1 != rans2) and (rans2 != rans3) and (rans1 != rans3):
                        ranCombination = rans1 + "+" + rans2 + "+" + rans3
                        if ranCombination in ruExample.keys():
                            return ranCombination   


    raise Exception("this is an error!")
    
    
    

            
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

