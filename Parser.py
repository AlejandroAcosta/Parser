import nltk, numpy, re
from nltk import grammar 
from numpy import *

class Parser:
    """
    Contains methods to parse a probabilistic context free grammar.
    
    Organizes all the functions related to parsing a sentence using a PCFG
    in NLTK format.

    grammar: the PCFG used by the parser
    MAX_PARSES: maximum number of parses that the parser will output.
    """

    # this is the PCFG, initializing to 0
    #grammar = 0
    
    def __init__(self, probCFG, maximum_number_of_parses):
        """ Initializes the PCFG.

        Takes as parameter a PCFG and constructs it. The rest of the methods
        will use this grammar.
        """
        self.grammar = probCFG
        self.MAX_PARSES = maximum_number_of_parses

    def __str__(self):
        """ Returns a representation of the class. """
        rep = str(self.grammar)
        rep += str(self.MAX_PARSES)
        return rep
        
    def CKY(self, sentence):
        """ Calculates the parses and associated parse probabilities.

        Performs the CKY algorithm on the input sentence and saves each of the
        possible parses for later processing.

        sentence: tokenized sentence. 
        """
        # length of the sentence. Used for size of table
        n = len(sentence)

        # initializing tables. each element is dictionary
        # CKY_Table: maps production to probability of production
        # back_table: contains back trace for the given production
        CKY_table = [[dict() for x in range(n)] for x in range(n)]
        back_table = [[dict() for x in range(n)] for x in range(n)]
        

        # the algorithm itself
        for j in range(1, len(sentence)+1):
            # for all productions of form A -> s where s is non-terminal
            # assumes that all rhs with NT contain exactly 1 NT
            for production in toy_pcfg2.productions():
                # this production's rhs is the word we're looking at
                if production.rhs()[0] == sentence[j-1]:
                    CKY_table[j-1][j][production.lhs()] = production.prob()

            # loop through rows
            for i in range(j-2,-1,-1):
                # loop through values that can join together for parsing
                for k in range(i+1,j):
                    for production in toy_pcfg2.productions():
                        # may deal with unit productions here
                        # get productions with given word as rhs and see if they
                        # are unit productions. Treat the whole chain up to
                        # something valid as one production.
                        #
                        # Get the parent of the production producing the word
                        # then get the possible parents of that non-terminal
                        # and see its children                        
                        if len(production) == 2 \
                           and CKY_table[i][k].get(production.rhs()[0]) > 0 \
                           and CKY_table[k][j].get(production.rhs()[1]) > 0:
                            A = production.lhs()
                            B = production.rhs()[0]
                            C = production.rhs()[1]
                            prob_thresh = production.prob()*\
                                CKY_table[i][k][B] * CKY_table[k][j][C]

                            if CKY_table[i][j].get(A) < prob_thresh:
                                CKY_table[i][j][A] = prob_thresh
                                back_table[i][j][A] = (k,B,C)
      
                    

    def __unit_productions(self, cur_prod, prod = [], prob = 0):
        """ Goes up the grammar's hierarchy and deals with unit productions.

        Give it a terminal rhs and it will recursively call itself and
        construct an enhanced rule so that the CKY table can treat it as
        one big production in CNF.
        """
##        # if first call
##        if is_terminal(cur_prod.rhs()[0]):
##            # stripping probability out
##            prod_list = re.split('\[|\]', str(cur_prod))
##            new_production = prod_list[0]
##            new_prob = prod_list[1]
##
##            # call itself here
##            self.__unit_productions(new_production, 
##            # bottom of recursion return
##            return (new_production, new_prob)
##
##        # if unit production
##        elif len(cur_prod.rhs()) == 1 and is_nonterminal(cur_prod.rhs()[0]):
##            prod_list = re.split('\[|\]', str(cur_prod))
##            new_production =
##            new_prob *= prod_list[1]
                    
    # may need a paramater
    def __decide_parse(self):
        """ Decides the most probable parse from CKY algorithm. """

    def __build_trees(self, back_table, table):
        """ Builds trees based on the parse table and traceback table.

        :return: list of parse trees in order from most to least likely
        :rtype: list of trees
        
        :param back_table: back trace table
        :type back_table: list of lists of dicts
        
        :param table: CKY parse table
        :type table: list of lists of dicts
        """
        trees_list = []
        # length of the table
        n = len(table)-1
        # for every valid parse of entire sentence
        for S in back_table[0][n]:
            # construct a tree and then append it to tree_list
            # start with start_symbol + parse probability
            ## this may be an issue because of Tree constructor,
            ## consider dropping space
            start_symbol = str(S) + ' ' + str(table[0][n][S])
            tree_string = '(' + str(S)
            i = 0
            j = n
            k = back_table[0][n][S][0]

            # increases everytime sees right. Decreases if sees T after an R
            depth = 0
            # indicates if last element seen was right
            last_was_right = False
            
            # first element is element. second element indicates type of node
            # right child, left child, or terminal
            # third element is i, j, k indices
            stack = [(back_table[0][n][S][2], 'r', (i, j, k)), \
                     (back_table[0][n][S][1], 'l', (i, j, k)) ] # [C, B]
            # iterate through everything until tree constructed
            # (ie. stack is empty at end of iteration)
            while len(stack) > 0:
                A = stack.pop()
                # if looking at right child
                if A[1] == 'l': # is left child
                    # indices for element that just got popped
                    old_i = A[2][0]
                    old_j = A[2][1]
                    old_k = A[2][2]

                    last_was_right = False
                    # this left side leads to terminal
                    if isinstance(back_table[old_i][old_k].get(A[0]), str):
                        stack.append((back_table[old_i][old_k][A[0]], 't'))

                    # this right side leads to non-terminals
                    else:
                        # updating indices
                        i = old_i
                        j = old_k
                        key = back_table[i][j].get(A[0])
                        k = key[0]
                        # appending next set of non-terminals
                        stack.append((key[2],'r',(i,j,k)))
                        stack.append((key[1],'l',(i,j,k)))
                    tree_string += ' (' + str(A[0])
                elif A[1] == 'r':
                    print 'Looking at right'
                    # indices for element that just got popped
                    old_i = A[2][0]
                    old_j = A[2][1]
                    old_k = A[2][2]
                    
                    last_was_right = True
                    # incrementing depth
                    depth += 1
                    
                    if isinstance(back_table[k][j].get(A[0]), str):
                        stack.append((back_table[k][j][A[0]], 't'))
                    else:
                        #updating indices
                        i = old_k
                        j = old_j
                        key = back_table[i][j].get(A[0])
                        k = key[0]
                        # appending next set of non-terminals
                        stack.append((key[2], 'r', (i,j,k)))
                        stack.append((key[1], 'l', (i,j,k)))
                    
                    # updating indices j remains the same
                    tree_string += ' (' + str(A[0])            
                    
                elif A[1] == 't': # is terminal
                    tree_string += ' ' + A[0]
                    # decrement depth if terminal closes a right
                    if last_was_right and len(stack) > 0 and stack[0][1] == 'r':
                        depth -= 1
                        tree_string += ')'*(len(stack)+1)
                    else:
                        tree_string += ')'
                    
                else: # error
                    print 'Error: something went wrong with tree constructing'

            # finishing string representation
            tree_string += ')'*depth
            
            return tree_string

    def output_parses(self):
        """ Output the results of the parse for use by other programs. """

    
if __name__ == "__main__":
    print "You ran this module directly. That's no good.\n"
    raw_input("Press the enter key to exit.\n\n")

    
