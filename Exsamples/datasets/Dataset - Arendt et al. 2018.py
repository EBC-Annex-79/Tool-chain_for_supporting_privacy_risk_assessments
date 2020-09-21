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


floor3_room1 = M['Teaching_Room_1']
g1.add((floor3_room1, RDF.type, SBUILDING.Teaching_Room))

scheduleActivities = M['ScheduleActivities']
g1.add((scheduleActivities, RDF.type, SBUILDING.ScheduleActivities))
g1.add((scheduleActivities, RDF.type, PRIVVULN.External))
g1.add((floor3_room1, PRIVVULNV2.has, scheduleActivities))

roomCountingLinesStream = M['CountingLinesStream']
g1.add((roomCountingLinesStream, RDF.type, SBUILDING.CountingLine))
g1.add((roomCountingLinesStream, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomCountingLinesStream, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor3_room1, PRIVVULNV2.has, roomCountingLinesStream))

vAVStream = M['VAVStream']
g1.add((vAVStream, RDF.type, SBUILDING.VariableAirVolume))
g1.add((vAVStream, RDF.type, PRIVVULN.TimeSeries))
g1.add((vAVStream, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor3_room1, PRIVVULNV2.has, vAVStream))

cO2Steam = M['CO2Steam']
g1.add((cO2Steam, RDF.type, SBUILDING.CO2))
g1.add((cO2Steam, RDF.type, PRIVVULN.TimeSeries))
g1.add((cO2Steam, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor3_room1, PRIVVULNV2.has, cO2Steam))

floor3_room4 = M['Teaching_Room_2']
g1.add((floor3_room4, RDF.type, SBUILDING.Teaching_Room))

scheduleActivities1 = M['ScheduleActivitiesForRoom1']
g1.add((scheduleActivities1, RDF.type, SBUILDING.ScheduleActivities))
g1.add((scheduleActivities1, RDF.type, PRIVVULN.External))
g1.add((floor3_room4, PRIVVULNV2.has, scheduleActivities1))

roomCountingLinesStream1 = M['CountingLinesStream1']
g1.add((roomCountingLinesStream1, RDF.type, SBUILDING.CountingLine))
g1.add((roomCountingLinesStream1, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomCountingLinesStream1, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor3_room4, PRIVVULNV2.has, roomCountingLinesStream1))

vAVStream1 = M['VAVStream1']
g1.add((vAVStream1, RDF.type, SBUILDING.VariableAirVolume))
g1.add((vAVStream1, RDF.type, PRIVVULN.TimeSeries))
g1.add((vAVStream1, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor3_room4, PRIVVULNV2.has, vAVStream1))

cO2Steam1 = M['CO2Steam1']
g1.add((cO2Steam1, RDF.type, SBUILDING.CO2))
g1.add((cO2Steam1, RDF.type, PRIVVULN.TimeSeries))
g1.add((cO2Steam1, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor3_room4, PRIVVULNV2.has, cO2Steam1))

floor2_room2 = M['StudyZone_Room1']
g1.add((floor2_room2, RDF.type, SBUILDING.Studyzone_Room))

scheduleActivities2 = M['ScheduleActivitiesForRoom2']
g1.add((scheduleActivities2, RDF.type, SBUILDING.ScheduleActivities))
g1.add((scheduleActivities2, RDF.type, PRIVVULN.External))
g1.add((floor2_room2, PRIVVULNV2.has, scheduleActivities2))

roomCountingLinesStream2 = M['CountingLinesStream2']
g1.add((roomCountingLinesStream2, RDF.type, SBUILDING.CountingLine))
g1.add((roomCountingLinesStream2, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomCountingLinesStream2, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor2_room2, PRIVVULNV2.has, roomCountingLinesStream2))

vAVStream2 = M['VAVStream2']
g1.add((vAVStream2, RDF.type, SBUILDING.VariableAirVolume))
g1.add((vAVStream2, RDF.type, PRIVVULN.TimeSeries))
g1.add((vAVStream2, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor2_room2, PRIVVULNV2.has, vAVStream2))

cO2Steam2 = M['CO2Steam2']
g1.add((cO2Steam2, RDF.type, SBUILDING.CO2))
g1.add((cO2Steam2, RDF.type, PRIVVULN.TimeSeries))
g1.add((cO2Steam2, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor2_room2, PRIVVULNV2.has, cO2Steam2))

floor2_room3 = M['StudyZone_Room2']
g1.add((floor2_room3, RDF.type, SBUILDING.Studyzone_Room))

scheduleActivities3 = M['ScheduleActivitiesForRoom3']
g1.add((scheduleActivities3, RDF.type, SBUILDING.ScheduleActivities))
g1.add((scheduleActivities3, RDF.type, PRIVVULN.External))
g1.add((floor2_room3, PRIVVULNV2.has, scheduleActivities3))

roomCountingLinesStream3 = M['CountingLinesStream3']
g1.add((roomCountingLinesStream3, RDF.type, SBUILDING.CountingLine))
g1.add((roomCountingLinesStream3, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomCountingLinesStream3, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor2_room3, PRIVVULNV2.has, roomCountingLinesStream3))

vAVStream3 = M['VAVStream3']
g1.add((vAVStream3, RDF.type, SBUILDING.VariableAirVolume))
g1.add((vAVStream3, RDF.type, PRIVVULN.TimeSeries))
g1.add((vAVStream3, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor2_room3, PRIVVULNV2.has, vAVStream3))

cO2Steam3 = M['CO2Steam3']
g1.add((cO2Steam3, RDF.type, SBUILDING.CO2))
g1.add((cO2Steam3, RDF.type, PRIVVULN.TimeSeries))
g1.add((cO2Steam3, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
g1.add((floor2_room3, PRIVVULNV2.has, cO2Steam3))

floor3 = M['Floor_3']
g1.add((floor3, RDF.type, SBUILDING.Floor))
g1.add((floor3, PRIVVULN.star, floor3_room1))
g1.add((floor3, PRIVVULN.star, floor3_room4))

floor2 = M['Floor_2']
g1.add((floor2, RDF.type, SBUILDING.Floor))
g1.add((floor2, PRIVVULN.star, floor2_room2))
g1.add((floor2, PRIVVULN.star, floor2_room3))

building = M['Building_sub']
g1.add((building, RDF.type, SBUILDING.Building))
g1.add((building, PRIVVULN.star, floor2))
g1.add((building, PRIVVULN.star, floor3))

contextLocation = M['ContextLocation_input']
g1.add((contextLocation, RDF.type, SBUILDING.ContextLocation))
g1.add((contextLocation, RDF.type, PRIVVULN.Metadata))
g1.add((building, PRIVVULNV2.has, contextLocation))

driver = Driver(debug_mode=True)
print("graph has %s statements." % len(g1))

folder = "output/Datasets/"
outputName = "Arendt et al 2018"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")