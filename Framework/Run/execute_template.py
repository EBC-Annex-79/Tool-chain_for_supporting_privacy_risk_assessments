import os, sys
import pdb
current_path = os.path.abspath('.')
sys.path.append(current_path)

from rdflib import Graph, Namespace, URIRef, Literal, namespace
import rdflib
from Framework.driver import Driver
import Framework.namespace_util as NSUtil


def run_analyses(json):
    g1 = Graph()

    # source namespaces
    RDF  = NSUtil.get_namespase_rdf()
    RDFS = NSUtil.get_namespase_rdfs()
    OWL  = NSUtil.get_namespase_owl()
    XSD  = NSUtil.get_namespase_xsd()
    PRIVVULN = NSUtil.get_namespase_base_ontology()
    PRIVVULNV2 = NSUtil.get_namespase_extrantion_ontology()
    SBUILDING = NSUtil.get_namespase_domain_smart_building()

    g1.bind('rdf' , RDF)
    g1.bind('rdfs', RDFS)
    g1.bind('owl' , OWL)
    g1.bind('xsd' , XSD)

    # custom namespace
    g1.bind('privvuln',PRIVVULN)

    g1.bind('privvulnv2',PRIVVULNV2)

    g1.bind('sbuilding',SBUILDING)

    nodes = json["nodes"]
    
    links = json["links"]

    namespace = json["namespace"]
    M = Namespace(namespace)
    g1.bind('m', M)
    
    for node in nodes:
        if "name" not in node and "type" not in node:
            continue
        subject = M[node["name"]]
        g1.add((subject, RDF.type, rdflib.term.URIRef(node["type"])))

        if "attributes" in node:
            for attribute in node["attributes"]:
                if "name" not in attribute and "value" not in attribute and "dataType" not in attribute:
                    continue
                if attribute["dataType"] == "int" or attribute["dataType"] == "double" or attribute["dataType"] == "string":
                    # "xsd" and "sbuilding" might not work
                    g1.add((subject, rdflib.term.URIRef(str(SBUILDING) + attribute["name"]), Literal(attribute["value"], datatype=rdflib.term.URIRef(str(XSD)+ attribute["dataType"]))))

    for link  in links:
        if "subject" not in link and "predicate" not in link and "object" not in link:
            continue
        g1.add((rdflib.term.URIRef(link["subject"]), rdflib.term.URIRef(link["predicate"]), rdflib.term.URIRef(link["object"])))

    driver = Driver(debug_mode=True)
    print("graph has %s statements." % len(g1))

    folder = "output/"
    outputName = "test"

    g1 = driver.run(g1, folder + outputName)

    # print("graph has %s statements." % len(g1))

    # g1.serialize(folder+outputName+".rdf")