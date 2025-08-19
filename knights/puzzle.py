from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

knowledge0 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),  # A cannot be both a knight and a knave 
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(BKnight, BKnave)),  # B cannot be both a knight
    Or(CKnight, CKnave),  # C is either a knight or a knave
    Not(And(CKnight, CKnave)),  # C cannot be both a knight

    Implication(AKnight, And(AKnight, AKnave)), # A says "I am both a knight and a knave."
    
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

both_knaves = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),  # A cannot be both a knight and a knave 
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(BKnight, BKnave)),  # B cannot be both a knight
    Or(CKnight, CKnave),  # C is either a knight or a knave
    Not(And(CKnight, CKnave)),  # C cannot be both a knight

    Implication(AKnight, both_knaves), # If A is a Knight it must be true that both are Knaves
    Implication(AKnave, Not(both_knaves)),  # If A is a Knave, then it cannot be true that both are Knaves
    
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

same_kind = Or(
    And(AKnight, BKnight),
    And(AKnave, BKnave),
)

different_kind = Or(
    And(AKnight, BKnave),
    And(AKnave, BKnight),
)

knowledge2 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),  # A cannot be both a knight and a knave 
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(BKnight, BKnave)),  # B cannot be both a knight
    Or(CKnight, CKnave),  # C is either a knight or a knave
    Not(And(CKnight, CKnave)),  # C cannot be both a knight

    Implication(AKnight, same_kind), # If A is a Knight, then A and B must be the same kind
    Implication(AKnave, Not(same_kind)), # If A is a Knave, then A and B cannot be the same kind

    Implication(BKnight, different_kind), # If B is a Knight, then A and B must be different kinds
    Implication(BKnave, Not(different_kind)),  # If B is a Knave, then A and B cannot be different kinds
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.

# B says "A said 'I am a knave'."

# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),  # A cannot be both a knight and a knave 
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(BKnight, BKnave)),  # B cannot be both a knight
    Or(CKnight, CKnave),  # C is either a knight or a knave
    Not(And(CKnight, CKnave)),  # C cannot be both a knight
    
    Implication(BKnight, And(AKnight, AKnave)),  # If B is a Knight and telling the truth, then A said he is a Knave, which is a contradiction
    Implication(BKnave, Implication(AKnight, AKnight)),  # If B is a Knave, then A did not say he is a Knave
    Implication(BKnight, CKnave),  # If B is a Knight, C is a Knave
    Implication(BKnave, Not(CKnave)),  # If B is a Knave, then C cannot be a Knave
    Implication(CKnight, AKnight),  # C says A is a Knight
    Implication(CKnave, Not(AKnight)),  # If C is a Knave, then A cannot be a Knight
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
