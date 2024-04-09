from replacer import Replacer


def main():
    newReplacer = Replacer(infile="my_text.txt")

    newReplacer.add_replacement("SIGMA", "Σ")
    newReplacer.add_replacement("DELTA", "δ")
    newReplacer.add_replacement("GAMMA", "Ⲅ")
    newReplacer.add_replacement("ELEMENT_OF", "∊")
    newReplacer.add_replacement("SUBSET_OF", "⊆")

    newReplacer.replace_text()


if __name__ == '__main__':
    main()

