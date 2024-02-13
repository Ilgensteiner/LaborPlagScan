from laborPlagScan.DataModels.plagiat import Plagiat
from laborPlagScan.DataModels.student import Student


class PlagiatPaare:
    def __init__(self, student1: Student, student2: Student):
        self.student1 = student1
        self.student2 = student2
        self.plagiate = []
        self.plagiatZeilenGes = 0

        self.countPlagiatZeilenGes()
        self.plagiatAnteil = (self.student1.zeilenGes / self.plagiatZeilenGes) * 100

    def addPlagiat(self, plagiat: Plagiat):
        self.plagiate.append(plagiat)

    def countPlagiatZeilenGes(self):
        for plagiat in self.plagiate:
            self.plagiatZeilenGes += plagiat.plagiatZeilenAnzahl