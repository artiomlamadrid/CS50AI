import string
import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""
# examples:
# I had a little moist red paint in the palm of my hand.
# N V.  Det Adj. Adj.  Adj N.    P  Det N.   P  Det N

# I had a country walk on Thursday and came home in a dreadful mess.
# N V.  Det Adj   N.   P. N.       Conj V.  N.   P. Det Adj.   N

NONTERMINALS = """
S  -> NP VP | S Conj S

NP -> Det Adj N | Det N | N

VP -> V | V NP | V PP | V NP PP | V Adv
VP -> VP PP
VP -> VP Conj VP
VP -> V Adv PP

PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.strip().translate(str.maketrans("", "", string.punctuation)).lower().split()
    return [word for word in sentence if any(character.isalpha() for character in word)]



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    if isinstance(tree, nltk.Tree) and tree.label() == "NP":
        
        has_np_descendant = False
        for sub in tree.subtrees():
            if sub is not tree and isinstance(sub, nltk.Tree) and sub.label() == "NP":
                has_np_descendant = True
                break

        if not has_np_descendant:
            return [tree]

    for child in tree:
        if isinstance(child, nltk.Tree):
            chunks.extend(np_chunk(child))

    return chunks


if __name__ == "__main__":
    main()
