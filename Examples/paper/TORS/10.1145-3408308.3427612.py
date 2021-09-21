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

outside = M['outside']
g1.add((outside, RDF.type, SBUILDING.Outside))

temperatureOutside = M['Temperature_outside']
g1.add((temperatureOutside, RDF.type, SBUILDING.OutdoorTemperature))
g1.add((temperatureOutside, RDF.type, PRIVVULN.TimeSeries))
g1.add((temperatureOutside, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((outside, PRIVVULNV2.has, temperatureOutside))

humidityOutside = M['Humidity_outside']
g1.add((humidityOutside, RDF.type, SBUILDING.OutdoorHumidity))
g1.add((humidityOutside, RDF.type, PRIVVULN.TimeSeries))
g1.add((humidityOutside, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((outside, PRIVVULNV2.has, humidityOutside))

room = M['room']
g1.add((room, RDF.type, SBUILDING.Room))
g1.add((outside, PRIVVULN.star, room))

temperatureRoom = M['Temperature_Room']
g1.add((temperatureRoom, RDF.type, SBUILDING.Temperature))
g1.add((temperatureRoom, RDF.type, PRIVVULN.TimeSeries))
g1.add((temperatureRoom, PRIVVULNV2.TemporalResolution, Literal("30.0", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, temperatureRoom))

occ = M['occ']
g1.add((occ, RDF.type, SBUILDING.Occupant))
g1.add((room, PRIVVULN.star, occ))

skinTemperature = M['SkinTemperature_Occ']
g1.add((skinTemperature, RDF.type, SBUILDING.SkinTemperature))
g1.add((skinTemperature, RDF.type, PRIVVULN.TimeSeries))
g1.add((skinTemperature, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((occ, PRIVVULNV2.has, skinTemperature))

thermalComfortOcc = M['ThermalComfort_Occ']
g1.add((thermalComfortOcc, RDF.type, SBUILDING.ThermalComfort))
g1.add((thermalComfortOcc, RDF.type, PRIVVULN.TimeSeries))
g1.add((thermalComfortOcc, PRIVVULNV2.TemporalResolution, Literal("300.0", datatype=XSD.double)))
g1.add((occ, PRIVVULNV2.has, thermalComfortOcc))

clothingInsulationOcc = M['clothingInsulation_Occ']
g1.add((clothingInsulationOcc, RDF.type, SBUILDING.ClothingInsulation))
g1.add((clothingInsulationOcc, RDF.type, PRIVVULN.Metadata))
g1.add((occ, PRIVVULNV2.has, clothingInsulationOcc))

heightOcc = M['height_Occ']
g1.add((heightOcc, RDF.type, SBUILDING.Height))
g1.add((heightOcc, RDF.type, PRIVVULN.Metadata))
g1.add((occ, PRIVVULNV2.has, heightOcc))

shoulderCircumferenceOcc = M['shoulderCircumference_Occ']
g1.add((shoulderCircumferenceOcc, RDF.type, SBUILDING.ShoulderCircumference))
g1.add((shoulderCircumferenceOcc, RDF.type, PRIVVULN.Metadata))
g1.add((occ, PRIVVULNV2.has, shoulderCircumferenceOcc))

wightOcc = M['wight_Occ']
g1.add((wightOcc, RDF.type, SBUILDING.Wight))
g1.add((wightOcc, RDF.type, PRIVVULN.Metadata))
g1.add((occ, PRIVVULNV2.has, wightOcc))

genderOcc = M['gender_Occ']
g1.add((genderOcc, RDF.type, SBUILDING.Gender))
g1.add((genderOcc, RDF.type, PRIVVULN.Metadata))
g1.add((occ, PRIVVULNV2.has, genderOcc))

driver = Driver(debug_mode=True)
print("graph has %s statements." % len(g1))

folder = "Output/Papers/TORS/"
outputName = "10.1145-3408308.3427612"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")