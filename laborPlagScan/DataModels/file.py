import re

from laborPlagScan import basicConfig
from laborPlagScan.filter import Filter

java_syntax_words = {"abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue",
                     "default", "double", "do", "else", "enum", "extends", "final", "finally", "float", "for", "goto",
                     "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package",
                     "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch",
                     "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while", "true",
                     "false", "null", "String", "System", "out", "println", "print", "Scanner", "nextInt", "nextLine",
                     "new", "File", "exists", "length", "length()", "charAt", "substring", "equals", "equalsIgnoreCase",
                     "next", "hasNext", "hasNextLine", "hasNextInt", "hasNextDouble", "hasNextBoolean", "hasNextByte",
                     "hasNextFloat", "hasNextLong", "hasNextShort", "hasNextBigDecimal", "hasNextBigInteger",
                     "hasNextBigInteger", "hasNextBigDecimal", "hasNextBigInteger", "Main", "main", "args", "array",
                     "temp", "printStackTrace", "getMessage", "abstrakt", "@override", "@Override",
                     "Override", "toString", "equals", "hashCode", "clone", "compareTo", "finalize", "getClass"}

java_syntax_chars = {"{", "}", "(", ")", "[", "]", ";", "=", ":", ",", "+", "-", "*", "%", "++", "--", "==", "!=", ">",
                     "<", ">=", "<=", "&&", "||", "!", "&", "|", "^", "~", "<<", ">>", ">>>", "+=", "-=", "*=", "/=",
                     "%=", "&=", "|=", "^=", "<<=", ">>=", ">>>=", "?"}


def replace_words_in_file(file_list: list, word_list: set, java_operator_set: set) -> list:
    """Replaces all variables in a file with a placeholder and deletes all comments, and blank lines"""
    new_lines = []
    commentblock = False
    for line in file_list:
        new_line = line[:]
        if '/**' in new_line[1]:
            commentblock = True
            continue
        elif '*/' in new_line[1]:
            commentblock = False
            continue
        elif commentblock:
            continue
        else:
            if '//' in new_line[1]:
                new_line[1] = new_line[1].split('//')[0] + '\n'

        # Entfernen von "{" und "}" in der Zeile da diese an verschiedenen Stellen gesetzt sein können
        new_line[1] = new_line[1].replace('{', '').replace('}', '')

        # Erntferenen von Leeren Zeilen
        if new_line[1].strip() == "":
            continue

        if re.search(r'System\.out\.println\("?\s*(?:\\n|\\t)*\s*"?\);', new_line[1]):
            continue

        words = re.findall(r'\b\w+\b', new_line[1])
        for word in words:
            if word not in word_list and word not in java_operator_set:
                new_line[1] = re.sub(r'\b' + re.escape(word) + r'\b', 'x', new_line[1])

        # leerzeichen um Java zeichen und Operatoren entfernen
        pattern = r'\s*(' + '|'.join([re.escape(ch) for ch in sorted(java_syntax_chars, key=len, reverse=True)]) + r')\s*'
        new_line[1] = re.sub(pattern, r'\1', new_line[1])

        # Java operatoren vereinfachen
        new_line[1] = new_line[1].replace('<=', '<').replace('>=', '>').replace('&&', '&')

        # alles innerhalb von Anführungszeichen ersetzen durch ein "x"
        new_line[1] = re.sub(r'(["\']).*(["\'])', 'x', new_line[1])
        new_lines.append(new_line)

    return new_lines


def search_for_aiVars(line):
    """Searches for AI variables in a line"""
    for var in Filter.aiDetactionVarsList:
        if var in line:
            return True
    return False


class File:
    def __init__(self, name, pfad):
        self.name = name
        self.pfad = pfad
        self.fileInLines = []
        self.linesAufbereitet = []
        self.plagatierteZeilen = []
        self.aiDetection = False

        self.file_to_list()
        self.lineCount = len(self.fileInLines)
        file_lines_prepared = replace_words_in_file(self.fileInLines, java_syntax_words, java_syntax_chars)
        self.filter_lines(file_lines_prepared)

    def file_to_list(self):
        """Converts a file to a list of lines, each line is a list with the line number and the line itself"""
        with open(self.pfad, 'r') as file:
            try:
                lines = file.readlines()
            except UnicodeDecodeError as e:
                basicConfig.handle_exception(type(e), e, None, "Mindestens eine Datei konnte nicht gelesen werden!",
                                             "File: " + self.pfad + " konnte nicht gelesen werden!")
                return []

        i = 0
        for line in lines:
            if line.count(";") > 1:
                lineSplits = line.count(";") - 1
                multi_line = line.replace(";", ";SplitHERE", lineSplits).split("SplitHERE")
                for j in multi_line:
                    line_list = [i, j]
                    self.fileInLines.append(line_list)
                    i += 1
                continue
            if search_for_aiVars(line):
                self.aiDetection = True

            line_list = [i, line]
            self.fileInLines.append(line_list)
            i += 1

    def filter_lines(self, file_lines) -> list:
        """Filters all lines from a file that contain a string from the filter.txt file"""
        regexpattern_list = Filter.getRegexpatternList()
        filter_strings = Filter.getFilterStrings()
        ignorePrintStatemants = Filter.getIgnorePrintStatemants()

        for line in file_lines:
            line[1] = line[1].strip()
            if not any(exclude_string in line for exclude_string in filter_strings) and not any(
                    regex_pattern.search(line[1]) for regex_pattern in regexpattern_list):
                if ignorePrintStatemants == 1:
                    if "System.out.print" in line[1]:
                        continue
                self.linesAufbereitet.append(line)

    def getFileString(self):
        """Returns the file as a string"""
        fileString = ""
        for line in self.fileInLines:
            fileString += line[1]
        return fileString
