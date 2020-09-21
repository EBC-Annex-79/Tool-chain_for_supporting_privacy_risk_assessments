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

globalSpace = M['Global']
# g1.add((globalSpace, RDF.type, PRIVVULNV2.Context))
g1.add((globalSpace, RDF.type, SBUILDING.Building))

skeletonModel = M['SkeletonModel_sub']
g1.add((skeletonModel, RDF.type, SBUILDING.SkeletonModel))
g1.add((skeletonModel, RDF.type, PRIVVULN.External))
g1.add((globalSpace, PRIVVULNV2.has, skeletonModel))

averageBMI = M['AverageBMI_sub']
g1.add((averageBMI, RDF.type, SBUILDING.AverageBMI))
g1.add((averageBMI, RDF.type, PRIVVULN.External))
g1.add((globalSpace, PRIVVULNV2.has, averageBMI))

typicalBodyShape = M['TypicalBodyShape_sub']
g1.add((typicalBodyShape, RDF.type, SBUILDING.TypicalBodyShape))
g1.add((typicalBodyShape, RDF.type, PRIVVULN.External))
g1.add((globalSpace, PRIVVULNV2.has, typicalBodyShape))

building = M['LivingLab']
g1.add((building, RDF.type, SBUILDING.Room))
g1.add((globalSpace, PRIVVULN.star, building))

skeletonJoints = M['SkeletonJointsstream']
g1.add((skeletonJoints, RDF.type, SBUILDING.SkeletonJoints))
g1.add((skeletonJoints, RDF.type, PRIVVULN.TimeSeries))
g1.add((skeletonJoints, PRIVVULNV2.TemporalResolution, Literal("0.03", datatype=XSD.double)))
g1.add((building, PRIVVULNV2.has, skeletonJoints))

driver = Driver(debug_mode=True)
print("graph has %s statements." % len(g1))

folder = "output/papers/"
outputName = "Dziedzic et al 2019"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")
