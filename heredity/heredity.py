import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        # print(f"{person}:")
        for field in probabilities[person]:
            # print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                # print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]
class Person():
    def __init__(self, name=None, mother=None, father=None, exhibits_trait=None):
        self.name = name
        self.mother = mother
        self.father = father
        self.exhibits_trait = exhibits_trait if exhibits_trait is not None else False

        # use the longer name consistently
        self.number_of_genes_to_calculate_probability_for = None
        self.compute_probability_for_trait = None

        self.joint_probability = 1

    # print person method
    def __str__(self):
        return f"Name: {self.name},\nMother: {self.mother},\nFather: {self.father},\nExhibits trait: {self.exhibits_trait}\nGenes to calculate probability for: {self.number_of_genes_to_calculate_probability_for}\nCompute probability for trait: {self.compute_probability_for_trait}\nJoint probability: {self.joint_probability}\n"

    def compute_joint_probability(self, mother=None, father=None):
        """
        Returns this person's probability factor for the current hypothesis:
        - If no parents: P(genes) * P(trait | genes)
        - Else:          P(genes | parents) * P(trait | genes)
        Uses:
        - self.number_of_genes_to_calculate_probability_for in {0,1,2}
        - self.compute_probability_for_trait in {True, False}
        """
        m = PROBS["mutation"]
        k = self.number_of_genes_to_calculate_probability_for
        t = self.compute_probability_for_trait

        # Helper: probability a parent passes the gene to child
        def pass_probability(parent):
            g = parent.number_of_genes_to_calculate_probability_for
            if g == 2:
                return 1 - m
            elif g == 1:
                return 0.5
            else:  # g == 0
                return m

        # Gene probability
        if self.mother is None and self.father is None:
            gene_p = PROBS["gene"][k]
        else:
            # if one parent is missing for some reason, fall back to priors
            if mother is None or father is None:
                gene_p = PROBS["gene"][k]
            else:
                p_m = pass_probability(mother)
                p_f = pass_probability(father)
                if k == 2:
                    gene_p = p_m * p_f
                elif k == 1:
                    gene_p = p_m * (1 - p_f) + (1 - p_m) * p_f
                elif k == 0:
                    gene_p = (1 - p_m) * (1 - p_f)
                else:
                    raise ValueError("Invalid gene count")

        # Trait probability
        trait_p = PROBS["trait"][k][t]

        factor = gene_p * trait_p
        self.joint_probability = factor  # keep for debugging if you like
        return factor

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return the joint probability that:
      - everyone in one_gene has 1 copy
      - everyone in two_genes has 2 copies
      - everyone else has 0 copies
      - everyone in have_trait has the trait
      - everyone else doesn't
    """
    # Build Person objects
    people_objects = {}
    for name, rec in people.items():
        mother = rec["mother"]
        father = rec["father"]
        exhibits_trait = rec["trait"]  # evidence (may be True/False/None)
        p = Person(name, mother, father, exhibits_trait)
        # assign the gene count for this hypothesis
        if name in two_genes:
            p.number_of_genes_to_calculate_probability_for = 2
        elif name in one_gene:
            p.number_of_genes_to_calculate_probability_for = 1
        else:
            p.number_of_genes_to_calculate_probability_for = 0
        # assign the trait status for this hypothesis
        p.compute_probability_for_trait = (name in have_trait)
        people_objects[name] = p

    # Multiply per-person factors
    total_probability = 1.0
    for person in people_objects.values():
        mom = people_objects.get(person.mother)
        dad = people_objects.get(person.father)
        total_probability *= person.compute_joint_probability(mom, dad)

    return total_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:

        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene_scaling_factor = 1.0 / sum(probabilities[person]['gene'].values())
        for key, _ in enumerate(probabilities[person]['gene'].values()):
            probabilities[person]['gene'][key] *= gene_scaling_factor
        traits_scaling_factor = 1.0 / sum(probabilities[person]['trait'].values())
        for key, _ in enumerate(probabilities[person]['trait'].values()):
            probabilities[person]['trait'][key] *= traits_scaling_factor

if __name__ == "__main__":
    main()
