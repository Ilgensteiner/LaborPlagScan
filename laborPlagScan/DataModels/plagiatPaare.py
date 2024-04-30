from laborPlagScan.DataModels.plagiat import Plagiat
from laborPlagScan.DataModels.student import Student


class PlagiatPaare:
    def __init__(self, student1: Student, student2: Student):
        self.student1 = student1
        self.student2 = student2
        self.plagiate = []
        self.plagiatZeilenGes = 0
        self.plagiatAnteil_Absolut = 0
        self.plagiatAnteil_Relativ = 0
        self.plagiatStatus = ""

    def addPlagiat(self, plagiat: Plagiat):
        self.plagiate.append(plagiat)

    def countPlagiatZeilenGes(self):
        self.plagiatZeilenGes = 0
        for plagiat in self.plagiate:
            self.plagiatZeilenGes += plagiat.plagiatZeilenAnzahl

    def calcPlagiatAnteil(self):
        if self.plagiatZeilenGes == 0 or self.student1.zeilenGes_ungefiltert == 0:
            self.plagiatAnteil_Absolut = 0
            self.plagiatAnteil_Relativ = 0
        else:
            self.plagiatAnteil_Absolut = (100 / self.student1.zeilenGes_ungefiltert) * self.plagiatZeilenGes
            self.plagiatAnteil_Relativ = (100 / self.student1.zeilenGes_gefiltert) * self.plagiatZeilenGes

    def markPlagiatCodeinFiles(self):
        for stud1file in self.student1.files:
            stud1file.plagatierteZeilenMarktiert = []
            for plagiat in self.plagiate:
                if plagiat.file1 == stud1file:
                    for abschnitt in plagiat.vonBis:
                        stud1file.plagatierteZeilenMarktiert.append([abschnitt[0], abschnitt[1]])

        for stud2file in self.student2.files:
            stud2file.plagatierteZeilenMarktiert = []
            for plagiat in self.plagiate:
                if plagiat.file2 == stud2file:
                    for abschnitt in plagiat.vonBis:
                        stud2file.plagatierteZeilenMarktiert.append([abschnitt[2], abschnitt[3]])

