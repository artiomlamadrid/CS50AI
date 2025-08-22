import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        
        # Remove any sentences that are now empty
        self.knowledge = [sentence for sentence in self.knowledge if len(sentence.cells) > 0]

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        
        # Remove any sentences that are now empty
        self.knowledge = [sentence for sentence in self.knowledge if len(sentence.cells) > 0]

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # STEP 3: Add a new sentence to the AI's knowledge base based on the
        # value of 'cell' and 'count'
        
        # Find all neighbors of the revealed cell (including diagonals)
        neighbors = set()
        for row in range(cell[0] - 1, cell[0] + 2): # check rows above, current, below
            for col in range(cell[1] - 1, cell[1] + 2): # check columns left, current, right
                # Add neighbor if it's not the cell itself and is within board bounds
                if (row, col) != cell and 0 <= row < self.height and 0 <= col < self.width:
                    neighbors.add((row, col))
        
        # Remove neighbors that are already known to be safe
        neighbors -= self.safes
        
        # Count how many known mines are among the neighbors (before removing them)
        mines_in_neighbors = len(self.mines.intersection(neighbors))
        
        # Remove neighbors that are already known to be mines
        neighbors -= self.mines
        
        # Adjust the count: subtract known mines from the total mine count
        count -= mines_in_neighbors
        
        # Only add the sentence if there are unknown neighbors to reason about
        if len(neighbors) > 0:
            self.knowledge.append(Sentence(neighbors, count))

        # STEP 4 & 5: Iterative inference - keep inferring until no new knowledge
        # This loop continues until we can't deduce any new information
        knowledge_added = True
        while knowledge_added:
            knowledge_added = False  # Assume no new knowledge will be found
            
            # Check all sentences for immediate conclusions (mines/safes)
            for sentence in self.knowledge.copy():
                # If sentence concludes certain cells are mines, mark them
                for mine in sentence.known_mines().copy():
                    if mine not in self.mines:  # Only mark if not already known
                        self.mark_mine(mine)
                        knowledge_added = True  # We found new information
                
                # If sentence concludes certain cells are safe, mark them
                for safe in sentence.known_safes().copy():
                    if safe not in self.safes:  # Only mark if not already known
                        self.mark_safe(safe)
                        knowledge_added = True  # We found new information
            
            # Check for subset relationships to infer new sentences
            # If sentence1 is a subset of sentence2, we can deduce a new sentence
            for i, sentence1 in enumerate(self.knowledge):
                for j, sentence2 in enumerate(self.knowledge):
                    if i != j and sentence1.cells.issubset(sentence2.cells):
                        # New sentence: cells in sentence2 but not in sentence1
                        new_cells = sentence2.cells - sentence1.cells
                        # New count: mines in sentence2 minus mines in sentence1
                        new_count = sentence2.count - sentence1.count
                        
                        # Only add if it's a valid sentence with unknown cells
                        if len(new_cells) > 0 and new_count >= 0:
                            new_sentence = Sentence(new_cells, new_count)
                            if new_sentence not in self.knowledge:
                                self.knowledge.append(new_sentence)
                                knowledge_added = True  # We added new knowledge



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        available_safe_cells = self.safes - self.moves_made

        if available_safe_cells:
            return random.choice(list(available_safe_cells))
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cells = {(i, j) for i in range(self.height) for j in range(self.width)}
        available_cells = all_cells - self.moves_made - self.mines

        if available_cells:
            return random.choice(list(available_cells))
        return None
