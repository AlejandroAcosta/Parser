#!/usr/bin/python

import sys, os, re, nltk

# import grammar

from nltk.corpus import treebank
from nltk.grammar import ContextFreeGrammar, Nonterminal
from nltk.treetransforms import chomsky_normal_form


'''
tbank_productions = set(production for sent in treebank.parsed_sents()
                        for production in sent.productions())

'''

treebank_prods = []
for i in range(199): # for all found sets of fileids
    tbstuff = treebank._fileids[i] # get a bunch of 'em
    for tree in treebank.parsed_sents(tbstuff):
        tree.chomsky_normal_form()

        treebank_prods += tree.productions()



tTCpcfg = nltk.induce_pcfg(Nonterminal('S'), list(treebank_prods))

# induce pcfg

# PTCpcfg = nltk.induce_pcfg(tbank_grammar)

# treetransforms: chomsky_normal_form

print("done! You have your WeightedGrammar")


