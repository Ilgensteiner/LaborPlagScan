# Klasse um Filter.txt auszulesen und zu verarbeiten
import ast
import re


def read_filters_from_file():
    with open('./filter.txt', 'r') as f:
        filter_list = ast.literal_eval(f.read())
    return filter_list


def save_filters_to_file(filters):
    with open('./filter.txt', 'w') as f:
        f.write(repr(filters))


class Filter:
    ignorePrintStatemants = False
    ignoreGetterSetter = False
    PlagiatAlert = 0
    ignore_files = []
    filter_strings = []
    regexpattern_list = []

    @staticmethod
    def readFilter():
        regexpattern_list_pre = []

        filter_list = read_filters_from_file()

        for filter_str in filter_list:
            if isinstance(filter_str, dict):
                settings_dict = filter_str
                Filter.ignorePrintStatemants = settings_dict["ignorePrintStatemants"]
                Filter.ignoreGetterSetter = settings_dict["ignoreGetterSetter"]
                Filter.PlagiatAlert = int(settings_dict["PlagiatAlert"])
                continue

            readed_filter = filter_str.split(":")
            if readed_filter[0] == "Regex":
                regexpattern_list_pre.append(readed_filter[1])
            elif readed_filter[0] == "File":
                Filter.ignore_files.append(readed_filter[1].strip().lower())
            else:
                Filter.filter_strings.append(filter_str)

        for regex_code in regexpattern_list_pre:
            Filter.regexpattern_list.append(re.compile(regex_code))

        if Filter.ignoreGetterSetter == 1:
            Filter.regexpattern_list.append(re.compile(r'(\s*public\s*\w+\s*x\s*\(\s*\w*\s*x?\s*\)\s*\{?\s*)'))
            Filter.regexpattern_list.append(re.compile(r'(\s*return this\.x;\s*)'))

    @staticmethod
    def getIgnorePrintStatemants():
        return Filter.ignorePrintStatemants

    @staticmethod
    def getPlagiatAlert():
        return Filter.PlagiatAlert

    @staticmethod
    def getIgnoreFiles():
        return Filter.ignore_files

    @staticmethod
    def getFilterStrings():
        return Filter.filter_strings

    @staticmethod
    def getRegexpatternList():
        return Filter.regexpattern_list
