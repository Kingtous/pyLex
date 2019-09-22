import constDef
class IclosureStruct:
    def __init__(self,id,selectedSet):
        self.id = id
        self.ms = selectedSet
        self.sDict = dict()
        self.node = constDef.nodeLabel