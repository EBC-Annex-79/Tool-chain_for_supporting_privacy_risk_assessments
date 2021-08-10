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

#Kjærgaard papper
troom = M['TeachingRoom_sub']
g1.add((troom, RDF.type, SBUILDING.Teaching_Room))

scheduleActivities = M['ScheduleActivitiesForTeachingRoom']
g1.add((scheduleActivities, RDF.type, SBUILDING.ScheduleActivities))
g1.add((scheduleActivities, RDF.type, PRIVVULN.External))
g1.add((troom, PRIVVULNV2.has, scheduleActivities))

roomDoorOpenStream = M['DoorOpenStream']
g1.add((roomDoorOpenStream, RDF.type, SBUILDING.DoorOpen))
g1.add((roomDoorOpenStream, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomDoorOpenStream, PRIVVULNV2.TemporalResolution, Literal("15", datatype=XSD.double)))
g1.add((troom, PRIVVULNV2.has, roomDoorOpenStream))

roomPIRStream = M['PIRStream']
g1.add((roomPIRStream, RDF.type, SBUILDING.PIR))
g1.add((roomPIRStream, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomPIRStream, PRIVVULNV2.TemporalResolution, Literal("5", datatype=XSD.double)))
g1.add((troom, PRIVVULNV2.has, roomPIRStream))

roomCountingLinesStream = M['CountingLinesStream']
g1.add((roomCountingLinesStream, RDF.type, SBUILDING.CountingLine))
g1.add((roomCountingLinesStream, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomCountingLinesStream, PRIVVULNV2.TemporalResolution, Literal("15", datatype=XSD.double)))
g1.add((troom, PRIVVULNV2.has, roomCountingLinesStream))

sroom = M['StudyZone_sub']
g1.add((sroom, RDF.type, SBUILDING.Studyzone_Room))

scheduleActivitiesStudyZone = M['ScheduleActivitiesForStudyZone']
g1.add((scheduleActivitiesStudyZone, RDF.type, SBUILDING.ScheduleActivities))
g1.add((scheduleActivitiesStudyZone, RDF.type, PRIVVULN.External))
g1.add((sroom, PRIVVULNV2.has, scheduleActivitiesStudyZone))

roomDoorOpenStream2 = M['DoorOpenStream2']
g1.add((roomDoorOpenStream2, RDF.type, SBUILDING.DoorOpen))
g1.add((roomDoorOpenStream2, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomDoorOpenStream2, PRIVVULNV2.TemporalResolution, Literal("15", datatype=XSD.double)))
g1.add((sroom, PRIVVULNV2.has, roomDoorOpenStream2))

roomPIRStream2 = M['PIRStream2']
g1.add((roomPIRStream2, RDF.type, SBUILDING.PIR))
g1.add((roomPIRStream2, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomPIRStream2, PRIVVULNV2.TemporalResolution, Literal("5", datatype=XSD.double)))
g1.add((sroom, PRIVVULNV2.has, roomPIRStream2))
g1.add((roomPIRStream2, PRIVVULNV2.TemplateCount, Literal("0", datatype=XSD.integer)))

roomCountingLinesStream2 = M['CountingLinesStream2']
g1.add((roomCountingLinesStream2, RDF.type, SBUILDING.CountingLine))
g1.add((roomCountingLinesStream2, RDF.type, PRIVVULN.TimeSeries))
g1.add((roomCountingLinesStream2, PRIVVULNV2.TemporalResolution, Literal("15", datatype=XSD.double)))
g1.add((sroom, PRIVVULNV2.has, roomCountingLinesStream2))

floor = M['FloorSub']
g1.add((floor, RDF.type, SBUILDING.Floor))
g1.add((floor, PRIVVULN.star, troom))
g1.add((floor, PRIVVULN.star, sroom))

scheduleActivities = M['ScheduleActivitiesForFloor']
g1.add((scheduleActivities, RDF.type, SBUILDING.ScheduleActivities))
g1.add((scheduleActivities, RDF.type, PRIVVULN.External))
g1.add((floor, PRIVVULNV2.has, scheduleActivities))

driver = Driver()
print("graph has %s statements." % len(g1))

folder = "output/paper/"
outputName = "Kjaergaard et al 2019"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")