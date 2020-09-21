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

room = M['Studyzone_Room']
g1.add((room, RDF.type, SBUILDING.Studyzone_Room))

pirStream = M['PIRStream']
g1.add((pirStream, RDF.type, SBUILDING.PIR))
g1.add((pirStream, RDF.type, PRIVVULN.TimeSeries))
g1.add((pirStream, PRIVVULNV2.TemporalResolution, Literal("0", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, pirStream))

temperatureStream = M['TemperatureStream']
g1.add((temperatureStream, RDF.type, SBUILDING.Temperature))
g1.add((temperatureStream, RDF.type, PRIVVULN.TimeSeries))
g1.add((temperatureStream, PRIVVULNV2.TemporalResolution, Literal("900", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, temperatureStream))

cO2Stream = M['CO2Stream']
g1.add((cO2Stream, RDF.type, SBUILDING.CO2))
g1.add((cO2Stream, RDF.type, PRIVVULN.TimeSeries))
g1.add((cO2Stream, PRIVVULNV2.TemporalResolution, Literal("900", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, cO2Stream))

countingLine = M['CountingLine']
g1.add((countingLine, RDF.type, SBUILDING.CountingLine))
g1.add((countingLine, RDF.type, PRIVVULN.TimeSeries))
g1.add((countingLine, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, countingLine))

room2 = M['Teaching_Room']
g1.add((room2, RDF.type, SBUILDING.Teaching_Room))

pirStream2 = M['PIRStream2']
g1.add((pirStream2, RDF.type, SBUILDING.PIR))
g1.add((pirStream2, RDF.type, PRIVVULN.TimeSeries))
g1.add((pirStream2, PRIVVULNV2.TemporalResolution, Literal("0", datatype=XSD.double)))
g1.add((room2, PRIVVULNV2.has, pirStream2))

temperatureStream2 = M['TemperatureStream2']
g1.add((temperatureStream2, RDF.type, SBUILDING.Temperature))
g1.add((temperatureStream2, RDF.type, PRIVVULN.TimeSeries))
g1.add((temperatureStream2, PRIVVULNV2.TemporalResolution, Literal("900", datatype=XSD.double)))
g1.add((room2, PRIVVULNV2.has, temperatureStream2))

cO2Stream2 = M['CO2Stream2']
g1.add((cO2Stream2, RDF.type, SBUILDING.CO2))
g1.add((cO2Stream2, RDF.type, PRIVVULN.TimeSeries))
g1.add((cO2Stream2, PRIVVULNV2.TemporalResolution, Literal("900", datatype=XSD.double)))
g1.add((room2, PRIVVULNV2.has, cO2Stream2))

countingLine2 = M['CountingLine2']
g1.add((countingLine2, RDF.type, SBUILDING.CountingLine))
g1.add((countingLine2, RDF.type, PRIVVULN.TimeSeries))
g1.add((countingLine2, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((room2, PRIVVULNV2.has, countingLine2))

floor = M['Floor']
g1.add((floor, RDF.type, SBUILDING.Floor))
g1.add((floor, PRIVVULN.star, room))
g1.add((floor, PRIVVULN.star, room2))

driver = Driver(domain_NS=SBUILDING, debug_mode=True)
print("graph has %s statements." % len(g1))

folder = "output/papers/"
outputName = "Sangogboye et al 2019"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")