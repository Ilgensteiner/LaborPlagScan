import unittest

from laborPlagScan.Gui.tableGui import delete_stud_from_dict

class TestDeleteStudFromDict(unittest.TestCase):

    def setUp(self):
        # Initial data setups for different tests
        self.data_4_students = {
            "plagiat1": [["Stud1", "details1"], ["Stud2", "details2"], ["Stud3", "details3"], ["Stud4", "details4"]],
            "plagiat2": [["Stud5", "details5"], ["Stud6", "details6"]]
        }

        self.data_3_students = {
            "plagiat3": [["Stud7", "details7"], ["Stud8", "details8"], ["Stud9", "details9"]]
        }

        self.data_6_students = {
            "plagiat4": [["Stud10", "details10"], ["Stud11", "details11"], ["Stud12", "details12"],
                         ["Stud13", "details13"], ["Stud14", "details14"], ["Stud15", "details15"]]
        }

    def test_4_students(self):
        result = delete_stud_from_dict(self.data_4_students, ["Stud1", "Stud2"])
        expected = {
            'plagiat1': [['Stud3', 'details3'], ['Stud4', 'details4']],
            'plagiat2': [['Stud5', 'details5'], ['Stud6', 'details6']],
            'plagiat1_Stud1_Stud3': [['Stud1', 'details1'], ['Stud3', 'details3']],
            'plagiat1_Stud1_Stud4': [['Stud1', 'details1'], ['Stud4', 'details4']],
            'plagiat1_Stud2_Stud3': [['Stud2', 'details2'], ['Stud3', 'details3']],
            'plagiat1_Stud2_Stud4': [['Stud2', 'details2'], ['Stud4', 'details4']]
        }
        self.assertEqual(result, expected)

    def test_3_students(self):
        result = delete_stud_from_dict(self.data_3_students, ["Stud7", "Stud8"])
        expected = {
            'plagiat3_Stud7_Stud9': [['Stud7', 'details7'], ['Stud9', 'details9']],
            'plagiat3_Stud8_Stud9': [['Stud8', 'details8'], ['Stud9', 'details9']]
        }
        self.assertEqual(result, expected)

    def test_6_students(self):
        result = delete_stud_from_dict(self.data_6_students, ["Stud10", "Stud11"])
        expected = {
            'plagiat4': [['Stud12', 'details12'], ['Stud13', 'details13'], ['Stud14', 'details14'], ['Stud15', 'details15']]
        }
        self.assertEqual(result, expected)
