# this file will contain the class Reader and the "struct" Replacement (class with public functions)

# this class has two attributes, readString and writeString. readString contains the string that will be the input
# of our find() function when looking at the text. writeString will be what we replace the readString with in our
# output text
class Replacement:

    def __init__(self, readString='', writeString=''):
        self.readString = readString
        self.writeString = writeString


# Attributes:
# - Replacement [] replacements
# - string infile
# - string outfile
# - string outputString
# Methods:
# - void add_replacement(string text, string replace)
#   - takes 2 strings and creates a Replacement object with those strings and adds the Replacement object into the
#     Reader’s replacements
# - void replace_text()
#   - Begins the replacement operation

class Replacer:

    def __init__(self, infile, outfile="replaced_text.txt"):
        self.replacements = []
        self.infile = infile
        self.outfile = outfile
        self.outputString = ""

