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


desk1 = M['desk1']
g1.add((desk1, RDF.type, SBUILDING.Desk))

plugLoadStream = M['PlugLoadStream']
g1.add((plugLoadStream, RDF.type, SBUILDING.PowerMeter))
g1.add((plugLoadStream, RDF.type, PRIVVULN.TimeSeries))
g1.add((plugLoadStream, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((desk1, PRIVVULNV2.has, plugLoadStream))

desk2 = M['desk2']
g1.add((desk2, RDF.type, SBUILDING.Desk))

plugLoadStream2 = M['PlugLoadStream2']
g1.add((plugLoadStream2, RDF.type, SBUILDING.PowerMeter))
g1.add((plugLoadStream2, RDF.type, PRIVVULN.TimeSeries))
g1.add((plugLoadStream2, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((desk2, PRIVVULNV2.has, plugLoadStream2))

room = M['Room']
g1.add((room, RDF.type, SBUILDING.Room))
g1.add((room, PRIVVULN.star, desk1))
g1.add((room, PRIVVULN.star, desk2))

single_Office_Room = M['Single_Office_Room']
g1.add((single_Office_Room, RDF.type, SBUILDING.Single_Office_Room))

plugLoadStream3 = M['PlugLoadStream3']
g1.add((plugLoadStream3, RDF.type, SBUILDING.PowerMeter))
g1.add((plugLoadStream3, RDF.type, PRIVVULN.TimeSeries))
g1.add((plugLoadStream3, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((single_Office_Room, PRIVVULNV2.has, plugLoadStream3))

floor = M['Floor']
g1.add((floor, RDF.type, SBUILDING.Floor))
g1.add((floor, PRIVVULN.star, room))
g1.add((floor, PRIVVULN.star, single_Office_Room))

driver = Driver(debug_mode=True)
print("graph has %s statements." % len(g1))

folder = "output/papers/"
outputName = "Sonta et al 2019"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")