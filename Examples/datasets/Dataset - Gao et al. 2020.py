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

occupies = []

for index in range(2):
    occupant = M['Human' + str(index)]
    g1.add((occupant, RDF.type, SBUILDING.Occupant))
    occupies.append(occupant)

    thermometer = M['Thermometer'+ str(index)]
    g1.add((thermometer, RDF.type, SBUILDING.Thermometer))
    g1.add((thermometer, RDF.type, PRIVVULN.TimeSeries))
    g1.add((thermometer, PRIVVULNV2.TemporalResolution, Literal("60", datatype=XSD.double)))
    g1.add((occupant, PRIVVULNV2.has, thermometer))

    accelerometer = M['Accelerometer'+ str(index)]
    g1.add((accelerometer, RDF.type, SBUILDING.Accelerometer))
    g1.add((accelerometer, RDF.type, PRIVVULN.TimeSeries))
    g1.add((accelerometer, PRIVVULNV2.TemporalResolution, Literal("1", datatype=XSD.double)))
    g1.add((occupant, PRIVVULNV2.has, accelerometer))

    heartRate = M['HeartRate'+ str(index)]
    g1.add((heartRate, RDF.type, SBUILDING.HeartRate))
    g1.add((heartRate, RDF.type, PRIVVULN.TimeSeries))
    g1.add((heartRate, PRIVVULNV2.TemporalResolution, Literal("1", datatype=XSD.double)))
    g1.add((occupant, PRIVVULNV2.has, heartRate))

    eda = M['ElectrodermalActivity'+ str(index)]
    g1.add((eda, RDF.type, SBUILDING.ElectrodermalActivity))
    g1.add((eda, RDF.type, PRIVVULN.TimeSeries))
    g1.add((eda, PRIVVULNV2.TemporalResolution, Literal("1", datatype=XSD.double)))
    g1.add((occupant, PRIVVULNV2.has, eda))

    photoplethysmography = M['Photoplethysmography'+ str(index)]
    g1.add((photoplethysmography, RDF.type, SBUILDING.Photoplethysmography))
    g1.add((photoplethysmography, RDF.type, PRIVVULN.TimeSeries))
    g1.add((photoplethysmography, PRIVVULNV2.TemporalResolution, Literal("1", datatype=XSD.double)))
    g1.add((occupant, PRIVVULNV2.has, photoplethysmography))

    gender = M['Gender'+ str(index)]
    g1.add((gender, RDF.type, SBUILDING.Gender))
    g1.add((gender, RDF.type, PRIVVULN.Metadata))
    g1.add((occupant, PRIVVULNV2.has, gender))

    yearOfBirth = M['YearOfBirth'+ str(index)]
    g1.add((yearOfBirth, RDF.type, SBUILDING.YearOfBirth))
    g1.add((yearOfBirth, RDF.type, PRIVVULN.Metadata))
    g1.add((occupant, PRIVVULNV2.has, yearOfBirth))

teaching_Room = M['Teaching_Room_sub']
g1.add((teaching_Room, RDF.type, SBUILDING.Teaching_Room))
g1.add((teaching_Room, PRIVVULN.star, occupies[0]))

contextLocation1 = M['ContextLocation1']
g1.add((contextLocation1, RDF.type, SBUILDING.ContextLocation))
g1.add((contextLocation1, RDF.type, PRIVVULN.Metadata))
g1.add((teaching_Room, PRIVVULNV2.has, contextLocation1))

scheduleActivities = M['ScheduleActivitiesForRoom']
g1.add((scheduleActivities, RDF.type, SBUILDING.ScheduleActivities))
g1.add((scheduleActivities, RDF.type, PRIVVULN.External))
g1.add((teaching_Room, PRIVVULNV2.has, scheduleActivities))

temperature = M['TemperatureStream']
g1.add((temperature, RDF.type, SBUILDING.Temperature))
g1.add((temperature, RDF.type, PRIVVULN.TimeSeries))
g1.add((temperature, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
g1.add((teaching_Room, PRIVVULNV2.has, temperature))

cO2Steam = M['CO2Steam']
g1.add((cO2Steam, RDF.type, SBUILDING.CO2))
g1.add((cO2Steam, RDF.type, PRIVVULN.TimeSeries))
g1.add((cO2Steam, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
g1.add((teaching_Room, PRIVVULNV2.has, cO2Steam))

humidity = M['HumidityStream']
g1.add((humidity, RDF.type, SBUILDING.Humidity))
g1.add((humidity, RDF.type, PRIVVULN.TimeSeries))
g1.add((humidity, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
g1.add((teaching_Room, PRIVVULNV2.has, humidity))

hallway_Room = M['Hallway_Room_sub']
g1.add((hallway_Room, RDF.type, SBUILDING.Hallway_Room))
g1.add((hallway_Room, PRIVVULN.star, occupies[1]))

building = M['Building_sub']
g1.add((building, RDF.type, SBUILDING.Building))
g1.add((building, PRIVVULN.star, teaching_Room))
g1.add((building, PRIVVULN.star, hallway_Room))

contextLocation = M['ContextLocation']
g1.add((contextLocation, RDF.type, SBUILDING.ContextLocation))
g1.add((contextLocation, RDF.type, PRIVVULN.Metadata))
g1.add((building, PRIVVULNV2.has, contextLocation))

outdoorTemperature = M['OutdoorTemperature']
g1.add((outdoorTemperature, RDF.type, SBUILDING.OutdoorTemperature))
g1.add((outdoorTemperature, RDF.type, PRIVVULN.TimeSeries))
g1.add((outdoorTemperature, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
g1.add((building, PRIVVULNV2.has, outdoorTemperature))

driver = Driver(domain_NS=SBUILDING,debug_mode=True)
folder = "Output/Datasets/"
outputName = "Gao et al. 2020"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")