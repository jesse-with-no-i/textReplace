from replacer import Replacer

# this will be the console application runner for this program
def run():
    # introduce the application
    print("Hello user! This is a simple application that allows you to enter a set of \nstrings and find and replace "
          "those string in the text file that you also select. \nPlease make sure that your input is accurate and "
          "correctly formatted.\n")

    # prompt user for a text file
    textfile = input("Enter the name of a text file for the input: ")
    outputTextfile = input("What would you like to name the new file?: ")

    # create a Replacer object with the given input
    userReplacer = Replacer(textfile, outputTextfile)

    # get user input for the replacements
    try:
        numInput = int(input("How many replacements will you be making to your file?: "))
    except ValueError:
        print("Error: the value entered was not an integer.")

    print("\nIn the next", numInput, 'lines, please enter the string you want to find, and the string you\n'
                                   'want to replace it with. For each entry, please follow the format: \n\n"find" "replace"\n\n')

    for _ in range(numInput):
        f, r = input().split('" "')
        findInput = f.strip('"')
        replaceInput = r.strip('"')

        userReplacer.add_replacement(findInput, replaceInput)

    # perform the replacement operation
    userReplacer.replace_text()

    print("Process Complete")