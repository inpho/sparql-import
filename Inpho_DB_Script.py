'''
@author: Rohit Zawar
@contact: zawar.rohit@gmail.com
@organization: Cognitive Science Department, Indiana university of bloomington.
@summary: This is script to query dbpedia for all the properties for the data present in LODE. The script outputs two files.One which has equivalent data from LODE and DBpedia and mapped against the inpho property.Other file has the data which is not present in the LODE.
@version: 1.0
'''
from rdflib.graph import ConjunctiveGraph
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
if __name__ == '__main__':
    dbPropResults = {}#dictionary to store the mapping properties DBprop:Inphoprop
    inpho_DB = {}#dictionary to store the DBpedia results against Inpho . Inphoresult:DBresult
    DB_inpho = {}#dictionary to store the Inpho results against DBpedia . DBresult:Inphoresult
    triples={}#storing the triples in the nested dictionary. Subject[predicate[object...]...]
    
    #query Inpho for data related to DBpedia for owl:sameAs property
    gLODE = ConjunctiveGraph()
    gLODE.parse("http://inphodev.cogs.indiana.edu/~jammurdo/out_n3.20140207.rdf", format="n3")
    resultsLODE = gLODE.query("""
        SELECT ?thinker_LODE ?thinkerDB
        WHERE { ?thinker_LODE owl:sameAs ?thinkerDB 
                FILTER (regex(str(?thinker_LODE),"http://inpho.cogs.indiana.edu","i")
                && regex(str(?thinkerDB),"http://dbpedia.org/resource/","i")).
               }limit 10
        """)
    
    #reading the cvsv file for the dbprop against the inpho property
    with open('inpho_db prop mapping.txt','r') as f:
        dbprops=csv.reader(f,delimiter='\t')
        for dbprop in dbprops:
            dbPropResults[dbprop[1]] = dbprop[0]
            
    #String the results in two different dictionaries to create bi-directional mapping between the results.
    for triple in resultsLODE:
        inpho_DB[triple[0]] = triple[1]#store the results in key as inpho url and value as dbpedia url
        DB_inpho[triple[1]] = triple[0]#store the results in key as dbpedia url and value as inpho url
        
    #Set Dbpedia sparql endpoint for querying   
    sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")
    #return format set to JSON
    sparqlDB.setReturnFormat(JSON)
    
    #Query the DBpedia for every item in the LODE and for every Item in the dbprop mapping file
    for inpho,DB in inpho_DB.iteritems():
        predicate = {}
        for dbprop in dbPropResults:
            sparqlDB.setQuery(""" PREFIX dbpprop: <http://dbpedia.org/ontology/>
                                  SELECT ?b  WHERE { <"""+DB+"""> """+dbprop+""" ?b.
                                                    FILTER (regex(str(?b),"dbpedia.org/resource/","i")).
                                                    }""")
            resultsDB = sparqlDB.query().convert()
            predicate[dbprop] = resultsDB["results"]["bindings"]
        triples[DB] = predicate
    
    #open files to store the contents, create if doesnt exists.    
    dataAbsentLODE = open('AbsentDataLODE.txt','w+')
    dataPresentLODE = open('PresentDataLODE.txt','w+')
    
    #iterate over the triples stored to get the subject predicate object
    for subject,predicate in triples.iteritems():
        for predicate1, objectn in predicate.iteritems():
            for object1 in objectn:
                DB_Entry = DB_inpho.get(object1['b']['value'])#reverse lookup for the inpho data check
                if(DB_Entry == None):#if not present put it to absent file
                    dataAbsentLODE.write(object1['b']['value']+'\n')
                else:#if present, make the entry of triple with inpho property and the object.
                    dataPresentLODE.write( DB_Entry + "  " +dbPropResults.get(predicate1)+"  "+ object1['b']['value']+'\n')
    
    #close the open files
    dataAbsentLODE.close();
    dataPresentLODE.close();
        