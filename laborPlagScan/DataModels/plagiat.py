
class Plagiat:
    def __init__(self, file1, file2, vonBis: list):
        self.file1 = file1
        self.file2 = file2
        self.vonBis = vonBis
        self.plagiatZeilenAnzahl = 0

        self.countlagiatZeilenAnzahl()

    def countlagiatZeilenAnzahl(self):
        for plagiat in self.vonBis:
            self.plagiatZeilenAnzahl += plagiat[1] - plagiat[0] + 1

