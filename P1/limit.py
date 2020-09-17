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
    alpha : False
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
        self.alpha = False

    def increase(self):
        self.count+=1
    def check(self, status):
        if status is SearchEnum.DEPTH_FIRST_SEARCH:
            self.alpha = True
        if status is SearchEnum.BREADTH_FIRST_SEARCH:
            self.alpha = True
        if status is SearchEnum.ITERATIVE_DEEPENING_SEARCH:
            self.alpha = True
        if status is SearchEnum.DEPTH_LIMITED_SEARCH:
            self.alpha = True
        if status is SearchEnum.ITERATIVE_DEEPENING_SEARCH:
            self.flag = True
        if status is SearchEnum.UNIFORM_COST_SEARCH:
            self.uniFlag = True
        if status is SearchEnum.GREEDY_SEARCH or SearchEnum.HILL_CLIMBING:
            self.heurFlag = True
        if status is SearchEnum.A_STAR:
            self.aStarF = True
        if status is SearchEnum.BEAM_SEARCH:
            self.bflag = True
        if status is SearchEnum.GREEDY_SEARCH:
            self.heurPrint = True
        if status is SearchEnum.HILL_CLIMBING:
            self.hillPrint = True
        if status is SearchEnum.BEAM_SEARCH:
            self.beamPrint = True

    def falseFlag(self):
        self.flag = False
        self.uniFlag = False
        self.heurFlag = False
        self.aStarF = False
        self.bflag = False
        self.heurPrint = False
        self.hillPrint = False
        self.beamPrint = False
        self.alpha = False
