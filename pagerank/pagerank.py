import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    pages_to_choose_from_current = corpus[page]
    pages_to_choose_from_all = set(corpus.keys())

    # If no outgoing links, treat as linking to all pages
    if not pages_to_choose_from_current:
        return {page: 1 / len(pages_to_choose_from_all) for page in pages_to_choose_from_all}

    probability_from_current = damping_factor / len(pages_to_choose_from_current)
    probability_from_all = (1 - damping_factor) / len(pages_to_choose_from_all)

    # combine both probabilities
    probabilities = {}
    for page in pages_to_choose_from_all:
        probabilities[page] = probability_from_all
        if page in pages_to_choose_from_current:
            probabilities[page] += probability_from_current
    
    return probabilities



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Start with a random page
    current_page = random.choice(list(corpus.keys()))
    page_counts = {page: 0 for page in corpus.keys()}
    page_counts[current_page] += 1

    for _ in range(1, n):
        probabilities = transition_model(corpus, current_page, damping_factor)
        pages = list(probabilities.keys())
        weights = list(probabilities.values())
        current_page = random.choices(pages, weights=weights, k=1)[0]
        page_counts[current_page] += 1

    return {page: count / n for page, count in page_counts.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialization
    N = len(corpus)
    page_ranks = {page: 1 / N for page in corpus.keys()}

    converged = False

    while not converged:
        # calculate new ranks
        new_ranks = {}
        for page in corpus.keys():
            # use formula: pagerank(p) = (1 - d) / N + d * sum(pagerank(i) / NumLinks(i) for all i linking to p)
            new_rank = (1 - damping_factor) / N
            for possible_linking_page in corpus.keys():
                if page in corpus[possible_linking_page]:
                    num_links = len(corpus[possible_linking_page])
                    new_rank += damping_factor * (page_ranks[possible_linking_page] / num_links)
                # if a page has no outgoing links, treat it as having links to all pages (including itself)
                if not corpus[possible_linking_page]:
                    new_rank += damping_factor * (page_ranks[possible_linking_page] / N)
            new_ranks[page] = new_rank

        # store the page ranks to check for convergence later
        old_ranks = page_ranks
        page_ranks = new_ranks

        # check for convergence
        converged = True
        for page in corpus.keys():
            if abs(page_ranks[page] - old_ranks[page]) > 0.001:
                converged = False
                break
    
    return page_ranks


if __name__ == "__main__":
    main()
