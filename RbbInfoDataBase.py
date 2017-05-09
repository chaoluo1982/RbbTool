import sys
import os

thisModule = sys.modules[__name__]

##########################################################Data base input section############################################################################
# RAN-->DUType-->RBBSNSMR     
standardList = ["W", "G", "L"]
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

"""
map
based on RBB, RuTypelist, we find its function,
we go through all possible duType and standard,

RBBSNSMR:
{RBB2RU: (RuTypeList1, RuTypeList2, ClassName)}
duTypelist
"""

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

#Typical RBB with 2RU analogue Cross connect, but without cpri cascading
# RBB20_2A
# RBB22_2B, RBB22_2J
# RBB42_2D
RU1TypeRBB202A = ["RRUS01", "RRUS02", "RRUW02", "RUL01", "RUS01", "RUS02", "RUS03", "RUW02"]
RU2TypeRBB202A = ["RRUS01", "RRUS02", "RRUW02", "RUL01", "RUS01", "RUS02", "RUS03", "RUW02"]
RBB202ARBBClass = "RBBSNSMRWith2RUCC"

RU1TypeRBB222B = ["RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW01", "RUW02"]
RU2TypeRBB222B = ["RRUS01", "RRUS02", "RRUW01", "RRUW02", "RRUW03", "RUL01", "RUS01", "RUS02", "RUS03", "RUW01", "RUW02"]
RBB222BRBBClass = "RBBSNSMRWith2RUCC"

RU1TypeRBB222J = ["RUS01", "RUS02"]
RU2TypeRBB222J = ["RUS01", "RUS02"]
RBB222JRBBClass = "RBBSNSMRWith2RUCC"

RU1TypeRBB422D = ["RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RU2TypeRBB422D = ["RRUS11", "RRUS12", "RRUS13", "RRUS14", "RRUS14s"]
RBB422DRBBClass = "RBBSNSMRWith2RUCC"

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
                 "RBB122C", "RBB142A", "RBB242B", "RBB222A", "RBB222E", "RBB242A", "RBB442C", "RBB202A", "RBB222B", "RBB222J", "RBB422D"]

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
MNSBMMRRbbInfoList = []

## MNSBMMR RBB release tables with 1 RU shared
#get this info from RS doc 2.6.1.1.5	MSMM WCDMA with DUW 10, DUW 11, DUW 20, DUW 30, DUW 31, DUW 41 + GSM with DUG 20 in star configuration
" W+G MNSBMMR cases: DUWV1102030 + DUG20 "
RBBInfo1 = ["RBB221A", "DUWV1102030", "W","15A", (2,)]
RBBInfo2 = ["RBB111A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB101A", "DUWV1102030", "W","16B", (1,)]
RBBInfo2 = ["RBB323A", "DUG20", "G","16B", (3,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB101A", "DUWV1102030", "W","16B", (1,)]
RBBInfo2 = ["RBB323B", "DUG20", "G","16B", (3,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB101A", "DUWV1102030", "W","16B", (1,)]
RBBInfo2 = ["RBB434A", "DUG20", "G","16B", (3,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB111A", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB111A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

#W G1 should use data port 1
RBBInfo1 = ["RBB111A", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB221A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))


#in this case, shared RU could be 1 or 2
RBBInfo1 = ["RBB111A", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB222B", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))


RBBInfo1 = ["RBB111A", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB222B", "DUG20", "G","14B", (2,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))


RBBInfo1 = ["RBB111A", "DUWV1102030", "W","16B", (1,)]
RBBInfo2 = ["RBB323A", "DUG20", "G","16B", (3,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB111A", "DUWV1102030", "W","16B", (1,)]
RBBInfo2 = ["RBB323B", "DUG20", "G","16B", (3,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))


RBBInfo1 = ["RBB111A", "DUWV1102030", "W","16B", (1,)]
RBBInfo2 = ["RBB434A", "DUG20", "G","16B", (4,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))


RBBInfo1 = ["RBB121A", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB121A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

#W G1 can only use RU1 because it need be connected with data port 1
RBBInfo1 = ["RBB121A", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB241A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))


RBBInfo1 = ["RBB121A", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB242A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))
RBBInfo1 = ["RBB121A", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB242A", "DUG20", "G","14B", (2,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB142A", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB121A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB221A", "DUWV1102030", "W","15A", (2,)]
RBBInfo2 = ["RBB111A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB221B", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB221B", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB221B", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB442C", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))
RBBInfo1 = ["RBB221B", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB442C", "DUG20", "G","14B", (2,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB221C", "DUWV1102030", "W","15A", (2,)]
RBBInfo2 = ["RBB121A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))


#question to RS, why RBB221F/RBB221G/RBB441D is mentioned in the MSMM case for W+G (DUWV1V2 + DUG20), but not in DUG20 single mode case???
RBBInfo1 = ["RBB221F", "DUWV1102030", "W","17A", (1,)]
RBBInfo2 = ["RBB221F", "DUG20", "G","17A", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB221G", "DUWV1102030", "W","17A", (1,)]
RBBInfo2 = ["RBB221G", "DUG20", "G","17A", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB441D", "DUWV1102030", "W","16A", (1,)]
RBBInfo2 = ["RBB441D", "DUG20", "G","16A", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))




RBBInfo1 = ["RBB222B", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB111A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))
RBBInfo1 = ["RBB222B", "DUWV1102030", "W","15A", (2,)]
RBBInfo2 = ["RBB111A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB241A", "DUWV1102030", "W","15A", (2,)]
RBBInfo2 = ["RBB121A", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB242B", "DUWV1102030", "W","15A", (1,)]
RBBInfo2 = ["RBB221B", "DUG20", "G","14B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB441B", "DUWV1102030", "W","16B", (2,)]
RBBInfo2 = ["RBB221B", "DUG20", "G","16B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))



RBBInfo1 = ["RBB442C", "DUWV1102030", "W","16B", (2,)]
RBBInfo2 = ["RBB221B", "DUG20", "G","16B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))
RBBInfo1 = ["RBB442C", "DUWV1102030", "W","16B", (1,)]
RBBInfo2 = ["RBB221B", "DUG20", "G","16B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))


RBBInfo1 = ["RBB422D", "DUWV1102030", "W","15A", (1,2)]
RBBInfo2 = ["RBB422D", "DUG20", "G","14B", (1,2)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB442C", "DUWV1102030", "W","16B", (1,2)]
RBBInfo2 = ["RBB442C", "DUG20", "G","16B", (1,2)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB222B", "DUWV1102030", "W","15A", (1,2)]
RBBInfo2 = ["RBB222B", "DUG20", "G","14B", (1,2)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB222B", "DUWV1102030", "W","16B", (1,2)]
RBBInfo2 = ["RBB323A", "DUG20", "G","16B", (2,3)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))

RBBInfo1 = ["RBB222B", "DUWV1102030", "W","16B", (1,2)]
RBBInfo2 = ["RBB323B", "DUG20", "G","16B", (2,3)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))


RBBInfo1 = ["RBB222B", "DUWV1102030", "W","16B", (1,2)]
RBBInfo2 = ["RBB434A", "DUG20", "G","16B", (3,4)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))



"""
#2RU shared DMMA, AIR21, special handling
RBBInfo1 = ["RBB241A", "DUWV1102030", "W","15B", (1,)]
RBBInfo2 = ["RBB241A", "DUG20", "G","15B", (1,)]
MNSBMMRRbbInfoList.append((RBBInfo1, RBBInfo2))
"""
SNMBMMRRbbInfoList = []
SNMBMMRRbbInfoListFor5216GW = [ ["RBB101a", "5216", "W", "G",	"16B" ],
                                ["RBB111a", "5216",	"W", "G",	"16B" ],
                                ["RBB111c", "5216",	"W", "G",	"17Q1"],
                                ["RBB111d", "5216",	"W", "G",	"17Q1"],
                                ["RBB121a", "5216",	"W", "G",	"16B" ],
                                ["RBB121c", "5216",	"W", "G",	"17Q1"],
                                ["RBB121d", "5216",	"W", "G",	"17Q1"],
                                ["RBB122b", "5216",	"W", "G",	"17Q1"],
                                ["RBB122c", "5216",	"W", "G",	"17Q1"],
                                ["RBB141a", "5216",	"W", "G",	"17A" ],
                                ["RBB142a", "5216",	"W", "G",	"17A" ],
                                ["RBB201a", "5216",	"W", "G",	"16B" ],
                                ["RBB202a", "5216",	"W", "G",	"17A" ],
                                ["RBB221a", "5216",	"W", "G",	"16B" ],
                                ["RBB221b", "5216",	"W", "G",	"16B" ],
                                ["RBB221f", "5216",	"W", "G",	"17A" ],
                                ["RBB221g", "5216",	"W", "G",	"17A" ],
                                ["RBB222b", "5216",	"W", "G",	"16B" ],
                                ["RBB222k", "5216",	"W", "G",	"17A" ],
                                ["RBB222l", "5216",	"W", "G",	"17A" ],
                                ["RBB241a", "5216",	"W", "G",	"16B" ],
                                ["RBB241b", "5216",	"W", "G",	"17A" ],
                                ["RBB242a", "5216",	"W", "G",	"16B" ],
                                ["RBB242b", "5216",	"W", "G",	"17A" ],
                                ["RBB321a", "5216",	"W", "G",	"16B" ],
                                ["RBB321b", "5216",	"W", "G",	"16B" ],
                                ["RBB323a", "5216",	"W", "G",	"16B" ],
                                ["RBB323b", "5216",	"W", "G",	"16B" ],
                                ["RBB421b", "5216",	"W", "G",	"16B" ],
                                ["RBB422d", "5216",	"W", "G",	"16B" ],
                                ["RBB431a", "5216",	"W", "G",	"16B" ],
                                ["RBB434a", "5216",	"W", "G",	"16B" ],
                                ["RBB441b", "5216",	"W", "G",	"16B" ],
                                ["RBB441d", "5216",	"W", "G",	"16B" ],
                                ["RBB442c", "5216",	"W", "G",	"16B" ],
                                ["RBB442f", "5216",	"W", "G",	"16B" ]]

SNMBMMRRbbInfoList += SNMBMMRRbbInfoListFor5216GW


#Triple mixed mode
MNMBMMRRbbInfoList = []

#Baseband 5216 for GSM + LTE and DUW 10 / DUW 11 / DUW 20 / DUW 20 / DUW 30 / DUW 31 / DUW 41 for WCDMA


MNMBMMRRbbInfoListForBB5216GLAndDUWV1V2W = [(["RBB221b", "5216", "G", "L", (1,), "17A"],	["RBB221b", "DUWV1102030", "W", (1,), "17A"]),  
                                            (["RBB221b", "5216", "G", "L", (1,), "17A"],	["RBB221b", "DUWV1102030", "W", (1,), "17A"]),   
                                            (["RBB221b", "5216", "G", "L", (1,), "17A"],	["RBB242b", "DUWV1102030", "W", (1,), "17A"]),   
                                            (["RBB221b", "5216", "G", "L", (1,), "17A"],	["RBB441b", "DUWV1102030", "W", (2,), "17A"]),   
                                            (["RBB221b", "5216", "G", "L", (1,), "17A"],	["RBB442c", "DUWV1102030", "W", (1,), "17A"]),   
                                            (["RBB221f", "5216", "G", "L", (1,), "17A"],	["RBB221f", "DUWV1102030", "W", (1,), "17A"]),   
                                            (["RBB221g", "5216", "G", "L", (1,), "17A"],	["RBB221g", "DUWV1102030", "W", (1,), "17A"]),   
                                            (["RBB241b", "5216", "G", "L", (1,), "17A"],	["RBB221b", "DUWV1102030", "W", (1,), "17A"]),   
                                            (["RBB242b", "5216", "G", "L", (1,), "17A"],	["RBB221b", "DUWV1102030", "W", (1,), "17A"]),   
                                            (["RBB242b", "5216", "G", "L", (1,2), "17A"],	["RBB242b", "DUWV1102030", "W", (1,2), "17A"]),
                                            (["RBB422d", "5216", "G", "L", (1,2), "17A"],	["RBB422d", "DUWV1102030", "W", (1,2), "17A"]),
                                            (["RBB441b", "5216", "G", "L", (1,), "17A"],	["RBB221b", "DUWV1102030", "W", (1,), "17A"]),   
                                            (["RBB441d", "5216", "G", "L", (1,), "17A"],	["RBB441d", "DUWV1102030", "W", (1,), "17A"]),  
                                            (["RBB442c", "5216", "G", "L", (1,), "17A"],	["RBB221b", "DUWV1102030", "W", (1,), "17A"]),   
                                            (["RBB442c", "5216", "G", "L", (1,2), "17A"],	["RBB442c", "DUWV1102030", "W", (1,2), "17A"])]
                                 

MNMBMMRRbbInfoList += MNMBMMRRbbInfoListForBB5216GLAndDUWV1V2W

