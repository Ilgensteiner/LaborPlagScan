# Create a List with all Parameters of the Java-Syntax
import re

java_syntax = {"abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue",
               "default", "double", "do", "else", "enum", "extends", "final", "finally", "float", "for", "goto",
               "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package",
               "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch",
               "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while", "true",
               "false", "null", "String", "System", "out", "println", "print", "Scanner", "nextInt", "nextLine",
               "new", "File", "exists", "length", "length()", "charAt", "substring", "equals", "equalsIgnoreCase",
               "next", "hasNext", "hasNextLine", "hasNextInt", "hasNextDouble", "hasNextBoolean", "hasNextByte",
               "hasNextFloat", "hasNextLong", "hasNextShort", "hasNextBigDecimal", "hasNextBigInteger",
               "hasNextBigInteger", "hasNextBigDecimal", "hasNextBigInteger", "{", "}", "(", ")", "[", "]", ";", "=",
               ":", ",", "+", "-", "*", "%", "++", "--", "==", "!=", ">", "<", ">=", "<=", "&&", "||", "!", "&",
               "|", "^", "~", "<<", ">>", ">>>", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", ">>>=",
               "?", "Main", "main", "args", "array", "temp", "Exception", "printStackTrace", "getMessage", "abstrakt",
               "@override", "@Override", "Override", "toString", "equals", "hashCode", "clone", "compareTo", "finalize", "getClass",
               "IllegalArgumentException"}


def replace_syntax_in_file(filepath, word_list):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines:
        if '//' in line:
            line = line.split('//')[0] + '\n'
        for word in word_list:
            line = re.sub(r'\b' + re.escape(word) + r'\b', '.', line)
        new_lines.append(line)
    new_text = ''.join(new_lines)
    new_filepath = filepath.rsplit('.', 1)[0] + '_checked.' + filepath.rsplit('.', 1)[1]
    with open(new_filepath, 'w') as file:
        file.write(new_text)


def replace_words_in_file(filepath, word_list):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines:
        if '//' in line:
            line = line.split('//')[0] + '\n'
        words = re.findall(r'\b\w+\b', line)
        for word in words:
            if word not in word_list:
                line = re.sub(r'\b' + re.escape(word) + r'\b', 'x', line)
        new_lines.append(line)
    new_text = ''.join(new_lines)
    new_filepath = filepath.rsplit('.', 1)[0] + '_checked.' + filepath.rsplit('.', 1)[1]
    with open(new_filepath, 'w') as file:
        file.write(new_text)


def test_filter_java_syntax():
    replace_syntax_in_file('C:\\Users\\eriki\\Downloads\\Ticket.java', java_syntax)
    replace_syntax_in_file('C:\\Users\\eriki\\Downloads\\CinemaTicket.java', java_syntax)
    replace_syntax_in_file('C:\\Users\\eriki\\Downloads\\ConcertTicket.java', java_syntax)
    replace_syntax_in_file('C:\\Users\\eriki\\Downloads\\Shop.java', java_syntax)


def test_filter_not_java_syntax():
    replace_words_in_file('C:\\Users\\eriki\\Downloads\\Ticket.java', java_syntax)
    replace_words_in_file('C:\\Users\\eriki\\Downloads\\CinemaTicket.java', java_syntax)
    replace_words_in_file('C:\\Users\\eriki\\Downloads\\ConcertTicket.java', java_syntax)
    replace_words_in_file('C:\\Users\\eriki\\Downloads\\Shop.java', java_syntax)


if __name__ == '__main__':
    test_filter_not_java_syntax()
