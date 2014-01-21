'''
Script to perform a SPARQL Query. Example from Programming the Semantic Web,
page 92-94
'''

import rdflib
from rdflib.graph import ConjunctiveGraph, Namespace
from rdflib import plugin

# Initialize the SPARQL plugins
plugin.register(
  "sparql", rdflib.query.Processor,
  "rdfextras.sparql.processor", "Processor")
plugin.register(
  "sparql", rdflib.query.Result,
  "rdfextras.sparql.query", "SPARQLQueryResult") 

# Initialize Namespace Objects
DBPEDIA = Namespace("http://dbpedia.org/")
INPHO = Namespace("http://inpho.cogs.indiana.edu/")
THINKER = Namespace("http://inpho.cogs.indiana.edu/thinker/")
g = ConjunctiveGraph()
g.parse("inpho_sample.n3.rdf", format="n3")

# this is the SPARQL Query
results = g.query("""
    SELECT ?teacher ?student
    WHERE { ?teacher inpho:teacher ?student }
    """, initNs={'inpho': INPHO, 'thinker': THINKER})

# print results, see p92-93 for XML serializing
for triple in results:
    print triple

