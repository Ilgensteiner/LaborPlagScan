from laborPlagScan.DataModels.plagiat import Plagiat
from laborPlagScan.DataModels.student import Student


class PlagiatPaare:
    def __init__(self, student1: Student, student2: Student):
        self.student1 = student1
        self.student2 = student2
        self.plagiate = []
        self.plagiatZeilenGes = 0

    def addPlagiat(self, plagiat: Plagiat):
        self.plagiate.append(plagiat)

    def countPlagiatZeilenGes(self):
        for plagiat in self.plagiate:
            self.plagiatZeilenGes += plagiat.plagiatZeilenAnzahl

    def getPlagiatAnteil(self):
        self.countPlagiatZeilenGes()
        if self.plagiatZeilenGes == 0:
            return 0
        return (self.student1.zeilenGes / self.plagiatZeilenGes) * 100
