import nltk
from nltk import grammar

class Parser:
    """
    Contains methods to parse a probabilistic context free grammar.
    
    Organizes all the functions related to parsing a sentence using a PCFG
    in NLTK format.
    """

    # this is the PCFG, initializing to 0
    grammar = 0

    def __init__(self, probCFG):
        """ Initializes the PCFG.

        Takes as parameter a PCFG and constructs it. The rest of the methods
        will use this grammar.
        """
        self.grammar = probCFG

    def CKY(self, sentence):
        """ Calculates the parses and associated parse probabilities.

        Performs the CKY algorithm on the input sentence and saves each of the
        possible parses for later processing.
        """

    # may need a paramater
    def __decide_parse(self):
        """ Decides the most probable parse from CKY algorithm. """

    def output_parses(self):
        """ Output the results of the parse for use by other programs. """

    

    
