import os, sys
current_path = os.path.abspath('.')
sys.path.append(current_path)

from rdflib import Graph, Namespace, URIRef, Literal
import rdflib
from Framework.driver import Driver
import Framework.namespace_util as NSUtil


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

# model namespace
M = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
g1.bind('m', M)

room = M['room']
g1.add((room, RDF.type, SBUILDING.Office_Room))

temperature = M['Temperature']
g1.add((temperature, RDF.type, SBUILDING.Temperature))
g1.add((temperature, RDF.type, PRIVVULN.TimeSeries))
g1.add((temperature, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, temperature))

occupantCount = M['OccupantCount']
g1.add((occupantCount, RDF.type, SBUILDING.OccupantCount))
g1.add((occupantCount, RDF.type, PRIVVULN.TimeSeries))
g1.add((occupantCount, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, occupantCount))

time = M['Time']
g1.add((time, RDF.type, SBUILDING.Timestamp))
g1.add((time, RDF.type, PRIVVULN.Metadata))
g1.add((room, PRIVVULNV2.has, time))

driver = Driver(debug_mode=True)
print("graph has %s statements." % len(g1))

folder = "output/paper/TORS/"
outputName = "10.1145-2993422.2993427"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")