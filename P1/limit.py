from SearchEnum import SearchEnum
class limit:
    count : int
    flag : False
    uniFlag : False
    heurFlag : False
    aStarF : False
    bflag : False
    hillPrint : False
    beamPrint : False
    def __init__(self):
        self.count = 2
        self.uniFlag = False
        self.flag = False
        self.heurFlag = False
        self.aStarF = False
        self.bflag = False
        self.heurPrint = False
        self.hillPrint = False
        self.beamPrint = False
    def increase(self):
        self.count+=1
    def check(self, status):
        if status is SearchEnum.ITERATIVE_DEEPENING_SEARCH:
            self.flag = True
        else:
            self.flag = False
        if status is SearchEnum.UNIFORM_COST_SEARCH:
            self.uniFlag = True
        else:
            self.uniFlag = False
        if status is SearchEnum.GREEDY_SEARCH or SearchEnum.HILL_CLIMBING or SearchEnum.BEAM_SEARCH:
            self.heurFlag = True
        else:
            self.heurFlag = False
        if status is SearchEnum.A_STAR:
            self.aStarF = True
        else:
            self.aStarF = False
        if status is SearchEnum.BEAM_SEARCH:
            self.bflag = True
        else:
            self.bflag = False
        if status is SearchEnum.GREEDY_SEARCH:
            self.heurPrint = True
        else:
            self.heurPrint = False
        if status is SearchEnum.HILL_CLIMBING:
            self.hillPrint = True
        else:
            self.hillPrint = False
        if status is SearchEnum.BEAM_SEARCH:
            self.beamPrint = True
        else:
            self.beamPrint = False


    def setcount(self, x):
        self.count = x
    def falseFlag(self):
        self.flag = False
        self.uniFlag = False
        self.heurFlag = False
        self.aStarF = False
        self.bflag = False
        self.heurPrint = False
        self.hillPrint = False
        self.beamPrint = False


    def skip(self):
        self.skipper = True
