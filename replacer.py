# this file will contain the class Reader and the "struct" Replacement (class with public functions)

# custom error for when the read string is a substring of the write string
class SubstringError(Exception):
    pass

# this class has two attributes, readString and writeString. readString contains the string that will be the input
# of our find() function when looking at the text. writeString will be what we replace the readString with in our
# output text
class Replacement:

    def __init__(self, readString='', writeString=''):
        self.readString = readString
        self.writeString = writeString
        self.length = len(readString)

        # verify that readString is not a substring of writeString
        if writeString.find(readString) != -1:
            raise SubstringError("Error: String you want to replace cannot be a substring of the replacement string.")


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

    # adds a new Replacement object to the replacements list
    def add_replacement(self, rString, wString):

        self.replacements.append(Replacement(rString, wString))

    # performs the replacement operation
    def replace_text(self):

        # saves the text from the input file to the outputString initially
        with open(self.infile, "r") as infile:
            self.outputString = infile.read()

        # begin iterating through the string for each replacement
        for r in self.replacements:

            # replace every string until there is none found (find function returns -1)
            foundIndex = self.outputString.find(r.readString)
            while foundIndex != -1:

                # modify output string so that the found instance of the string is replaced
                self.outputString = self.outputString[0:foundIndex] + r.writeString + \
                                    self.outputString[foundIndex + r.length:]

                foundIndex = self.outputString.find(r.readString)

        # write the output of the operation to the output file
        with open(self.outfile, "w", encoding="utf-8") as outfile:
            outfile.write(self.outputString)

