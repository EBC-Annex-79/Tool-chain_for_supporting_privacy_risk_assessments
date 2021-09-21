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

sensors = []

for index in range(4):
    if index == 2:
        sensor1 = M['ZCH_Shared_Office_Room']
        g1.add((sensor1, RDF.type, SBUILDING.Shared_Office_Room))
    elif index == 3:
        sensor1 = M['ZCH_Single_Office_Room']
        g1.add((sensor1, RDF.type, SBUILDING.Single_Office_Room))
    else:
        sensor1 = M['Foobot_ZCH_'+ str(index)]
        g1.add((sensor1, RDF.type, SBUILDING.Desk))
    sensors.append(sensor1)

    cO2Stream = M['CO2Stream'+ str(index)]
    g1.add((cO2Stream, RDF.type, SBUILDING.CO2))
    g1.add((cO2Stream, RDF.type, PRIVVULN.TimeSeries))
    g1.add((cO2Stream, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((sensor1, PRIVVULNV2.has, cO2Stream))

    humidity = M['HumidityStream'+ str(index)]
    g1.add((humidity, RDF.type, SBUILDING.Humidity))
    g1.add((humidity, RDF.type, PRIVVULN.TimeSeries))
    g1.add((humidity, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((sensor1, PRIVVULNV2.has, humidity))

    pm = M['ParticulateMatter25Stream'+ str(index)]
    g1.add((pm, RDF.type, SBUILDING.ParticulateMatter25))
    g1.add((pm, RDF.type, PRIVVULN.TimeSeries))
    g1.add((pm, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((sensor1, PRIVVULNV2.has, pm))

    pollution = M['PollutionStream'+ str(index)]
    g1.add((pollution, RDF.type, SBUILDING.Pollution))
    g1.add((pollution, RDF.type, PRIVVULN.TimeSeries))
    g1.add((pollution, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((sensor1, PRIVVULNV2.has, pollution))

    temperature = M['TemperatureStream'+ str(index)]
    g1.add((temperature, RDF.type, SBUILDING.Temperature))
    g1.add((temperature, RDF.type, PRIVVULN.TimeSeries))
    g1.add((temperature, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((sensor1, PRIVVULNV2.has, temperature))

    volatileOrganicCompounds = M['VOCStream'+ str(index)]
    g1.add((volatileOrganicCompounds, RDF.type, SBUILDING.VolatileOrganicCompounds))
    g1.add((volatileOrganicCompounds, RDF.type, PRIVVULN.TimeSeries))
    g1.add((volatileOrganicCompounds, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((sensor1, PRIVVULNV2.has, volatileOrganicCompounds))

zones = []
for index in range(4,9):
    if index == 7:
        zone = sensors[2]
        # g1.add((zone, RDF.type, SBUILDING.Shared_Office_Room))
    elif index == 8:
        zone = sensors[3]
        # g1.add((zone, RDF.type, SBUILDING.Single_Office_Room))
    else:
        zone = M['Netatmo_ZCH__'+ str(index-4)]
        g1.add((zone, RDF.type, SBUILDING.Zone))
    zones.append(zone)

    cO2Stream = M['CO2Stream'+ str(index)]
    g1.add((cO2Stream, RDF.type, SBUILDING.CO2))
    g1.add((cO2Stream, RDF.type, PRIVVULN.TimeSeries))
    g1.add((cO2Stream, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((zone, PRIVVULNV2.has, cO2Stream))

    humidity = M['HumidityStream'+ str(index)]
    g1.add((humidity, RDF.type, SBUILDING.Humidity))
    g1.add((humidity, RDF.type, PRIVVULN.TimeSeries))
    g1.add((humidity, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((zone, PRIVVULNV2.has, humidity))

    noise = M['NoiseStream'+ str(index-4)]
    g1.add((noise, RDF.type, SBUILDING.Noise))
    g1.add((noise, RDF.type, PRIVVULN.TimeSeries))
    g1.add((noise, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((zone, PRIVVULNV2.has, noise))

    pressure = M['PressureStream'+ str(index-4)]
    g1.add((pressure, RDF.type, SBUILDING.Pressure))
    g1.add((pressure, RDF.type, PRIVVULN.TimeSeries))
    g1.add((pressure, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((zone, PRIVVULNV2.has, pressure))

    temperature = M['TemperatureStream'+ str(index)]
    g1.add((temperature, RDF.type, SBUILDING.Temperature))
    g1.add((temperature, RDF.type, PRIVVULN.TimeSeries))
    g1.add((temperature, PRIVVULNV2.TemporalResolution, Literal("300", datatype=XSD.double)))
    g1.add((zone, PRIVVULNV2.has, temperature))

room = M['Room_GCH']
g1.add((room, RDF.type, SBUILDING.Shared_Office_Room))
g1.add((room, PRIVVULN.star, sensors[0]))
g1.add((room, PRIVVULN.star, sensors[1]))
g1.add((room, PRIVVULN.star, zones[0]))
g1.add((room, PRIVVULN.star, zones[1]))
g1.add((room, PRIVVULN.star, zones[2]))

floor = M['Floor_GCH']
g1.add((floor, RDF.type, SBUILDING.Floor))
g1.add((floor, PRIVVULN.star, room))
g1.add((floor, PRIVVULN.star, sensors[2]))
g1.add((floor, PRIVVULN.star, sensors[3]))

building = M['Building_GCH']
g1.add((building, RDF.type, SBUILDING.Building))
g1.add((building, PRIVVULN.star, floor))

driver = Driver()
print("graph has %s statements." % len(g1))

folder = "Output/Datasets/"
outputName = "Office_building_2"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")
