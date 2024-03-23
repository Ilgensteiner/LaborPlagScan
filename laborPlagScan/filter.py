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
    filterLoaded = False
    ignorePrintStatemants = False
    ignoreGetterSetter = False
    PlagiatAlert = 0
    ignore_files = []
    filter_strings = []
    regexpattern_list = []
    aiDetactionVarsList = []

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
            elif readed_filter[0] == "AI-Var":
                Filter.aiDetactionVarsList.append(readed_filter[1])
            else:
                Filter.filter_strings.append(filter_str)

        for regex_code in regexpattern_list_pre:
            Filter.regexpattern_list.append(re.compile(regex_code))

        if Filter.ignoreGetterSetter == 1:
            Filter.regexpattern_list.append(re.compile(r'(\s*public\s*\w+\s*x\s*\(\s*\w*\s*x?\s*\)\s*\{?\s*)'))
            Filter.regexpattern_list.append(re.compile(r'(\s*return this\.x;\s*)'))

        Filter.filterLoaded = True

    @staticmethod
    def getIgnorePrintStatemants():
        if not Filter.filterLoaded:
            Filter.readFilter()
        return Filter.ignorePrintStatemants

    @staticmethod
    def getPlagiatAlert():
        if not Filter.filterLoaded:
            Filter.readFilter()
        return Filter.PlagiatAlert

    @staticmethod
    def getIgnoreFiles():
        if not Filter.filterLoaded:
            Filter.readFilter()
        return Filter.ignore_files

    @staticmethod
    def getFilterStrings():
        if not Filter.filterLoaded:
            Filter.readFilter()
        return Filter.filter_strings

    @staticmethod
    def getRegexpatternList():
        if not Filter.filterLoaded:
            Filter.readFilter()
        return Filter.regexpattern_list

    @staticmethod
    def getAiDetactionVarsList():
        if not Filter.filterLoaded:
            Filter.readFilter()
        return Filter.aiDetactionVarsList
