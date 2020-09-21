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

temperature = M['Temperature_outside']
g1.add((temperature, RDF.type, SBUILDING.Temperature))
g1.add((temperature, RDF.type, PRIVVULN.TimeSeries))
g1.add((temperature, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((outside, PRIVVULNV2.has, temperature))

room = M['Room']
g1.add((room, RDF.type, SBUILDING.Room))
g1.add((outside, PRIVVULN.star, room))

pm = M['ParticulateMatter25_room']
g1.add((pm, RDF.type, SBUILDING.ParticulateMatter25))
g1.add((pm, RDF.type, PRIVVULN.TimeSeries))
g1.add((pm, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, pm))

dewPoint = M['DewPoint_room']
g1.add((dewPoint, RDF.type, SBUILDING.DewPoint))
g1.add((dewPoint, RDF.type, PRIVVULN.TimeSeries))
g1.add((dewPoint, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, dewPoint))

tVOC = M['TVOC_room']
g1.add((tVOC, RDF.type, SBUILDING.TVOC))
g1.add((tVOC, RDF.type, PRIVVULN.TimeSeries))
g1.add((tVOC, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, tVOC))

enthalpy = M['Enthalpy_room']
g1.add((enthalpy, RDF.type, SBUILDING.Enthalpy))
g1.add((enthalpy, RDF.type, PRIVVULN.TimeSeries))
g1.add((enthalpy, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, enthalpy))

humidity = M['Humidity_room']
g1.add((humidity, RDF.type, SBUILDING.Humidity))
g1.add((humidity, RDF.type, PRIVVULN.TimeSeries))
g1.add((humidity, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, humidity))

noise = M['Noise_room']
g1.add((noise, RDF.type, SBUILDING.Noise))
g1.add((noise, RDF.type, PRIVVULN.TimeSeries))
g1.add((noise, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((room, PRIVVULNV2.has, noise))

for i in range(0,15):
    bay = M['Bay_' + str(i+1)]
    g1.add((bay, RDF.type, SBUILDING.Single_Office_Room))
    g1.add((room, PRIVVULN.star, bay))

    co = M['CO_'+ str(i)]
    g1.add((co, RDF.type, SBUILDING.CO))
    g1.add((co, RDF.type, PRIVVULN.TimeSeries))
    g1.add((co, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
    g1.add((bay, PRIVVULNV2.has, co))

    co2 = M['CO2_'+ str(i)]
    g1.add((co2, RDF.type, SBUILDING.CO2))
    g1.add((co2, RDF.type, PRIVVULN.TimeSeries))
    g1.add((co2, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
    g1.add((bay, PRIVVULNV2.has, co2))

    tVOC = M['TVOC'+ str(i)]
    g1.add((tVOC, RDF.type, SBUILDING.TVOC))
    g1.add((tVOC, RDF.type, PRIVVULN.TimeSeries))
    g1.add((tVOC, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
    g1.add((bay, PRIVVULNV2.has, tVOC))

    if not i in [14,13,0,10,11]:
        temperature = M['Temperature'+ str(i)]
        g1.add((temperature, RDF.type, SBUILDING.Temperature))
        g1.add((temperature, RDF.type, PRIVVULN.TimeSeries))
        g1.add((temperature, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
        g1.add((bay, PRIVVULNV2.has, temperature))

        humidity = M['Humidity'+ str(i)]
        g1.add((humidity, RDF.type, SBUILDING.Humidity))
        g1.add((humidity, RDF.type, PRIVVULN.TimeSeries))
        g1.add((humidity, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
        g1.add((bay, PRIVVULNV2.has, humidity))

        illuminance = M['Illuminance'+ str(i)]
        g1.add((illuminance, RDF.type, SBUILDING.Illuminance))
        g1.add((illuminance, RDF.type, PRIVVULN.TimeSeries))
        g1.add((illuminance, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
        g1.add((bay, PRIVVULNV2.has, illuminance))

        pIR = M['PIR'+ str(i)]
        g1.add((pIR, RDF.type, SBUILDING.PIR))
        g1.add((pIR, RDF.type, PRIVVULN.TimeSeries))
        g1.add((pIR, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
        g1.add((bay, PRIVVULNV2.has, pIR))

        noise = M['Noise'+ str(i)]
        g1.add((noise, RDF.type, SBUILDING.Noise))
        g1.add((noise, RDF.type, PRIVVULN.TimeSeries))
        g1.add((noise, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
        g1.add((bay, PRIVVULNV2.has, noise))

    if i in [11,12,5]:
        pm = M['ParticulateMatter25_'+ str(i)]
        g1.add((pm, RDF.type, SBUILDING.ParticulateMatter25))
        g1.add((pm, RDF.type, PRIVVULN.TimeSeries))
        g1.add((pm, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
        g1.add((bay, PRIVVULNV2.has, pm))

        dewPoint = M['DewPoint_'+ str(i)]
        g1.add((dewPoint, RDF.type, SBUILDING.DewPoint))
        g1.add((dewPoint, RDF.type, PRIVVULN.TimeSeries))
        g1.add((dewPoint, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
        g1.add((bay, PRIVVULNV2.has, dewPoint))

        tVOC = M['TVOC_'+ str(i)]
        g1.add((tVOC, RDF.type, SBUILDING.TVOC))
        g1.add((tVOC, RDF.type, PRIVVULN.TimeSeries))
        g1.add((tVOC, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
        g1.add((bay, PRIVVULNV2.has, tVOC))

        enthalpy = M['Enthalpy_'+ str(i)]
        g1.add((enthalpy, RDF.type, SBUILDING.Enthalpy))
        g1.add((enthalpy, RDF.type, PRIVVULN.TimeSeries))
        g1.add((enthalpy, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
        g1.add((bay, PRIVVULNV2.has, enthalpy))




conference = M['Conference']
g1.add((conference, RDF.type, SBUILDING.Meeting_Room))
g1.add((room, PRIVVULN.star, conference))

co = M['CO_Conference']
g1.add((co, RDF.type, SBUILDING.CO))
g1.add((co, RDF.type, PRIVVULN.TimeSeries))
g1.add((co, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, co))

co2 = M['CO2_Conference']
g1.add((co2, RDF.type, SBUILDING.CO2))
g1.add((co2, RDF.type, PRIVVULN.TimeSeries))
g1.add((co2, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, co2))

tVOC = M['TVOC_Conference']
g1.add((tVOC, RDF.type, SBUILDING.TVOC))
g1.add((tVOC, RDF.type, PRIVVULN.TimeSeries))
g1.add((tVOC, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, tVOC))

temperature = M['Temperature_conference']
g1.add((temperature, RDF.type, SBUILDING.Temperature))
g1.add((temperature, RDF.type, PRIVVULN.TimeSeries))
g1.add((temperature, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, temperature))

humidity = M['Humidity_conference']
g1.add((humidity, RDF.type, SBUILDING.Humidity))
g1.add((humidity, RDF.type, PRIVVULN.TimeSeries))
g1.add((humidity, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, humidity))

illuminance = M['Illuminance_conference']
g1.add((illuminance, RDF.type, SBUILDING.Illuminance))
g1.add((illuminance, RDF.type, PRIVVULN.TimeSeries))
g1.add((illuminance, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, illuminance))

pIR = M['PIR_Conference']
g1.add((pIR, RDF.type, SBUILDING.PIR))
g1.add((pIR, RDF.type, PRIVVULN.TimeSeries))
g1.add((pIR, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, pIR))

noise = M['Noise_Conference']
g1.add((noise, RDF.type, SBUILDING.Noise))
g1.add((noise, RDF.type, PRIVVULN.TimeSeries))
g1.add((noise, PRIVVULNV2.TemporalResolution, Literal("60.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, noise))

pm = M['ParticulateMatter25_Conference']
g1.add((pm, RDF.type, SBUILDING.ParticulateMatter25))
g1.add((pm, RDF.type, PRIVVULN.TimeSeries))
g1.add((pm, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, pm))

dewPoint = M['DewPoint_Conference']
g1.add((dewPoint, RDF.type, SBUILDING.DewPoint))
g1.add((dewPoint, RDF.type, PRIVVULN.TimeSeries))
g1.add((dewPoint, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, dewPoint))

enthalpy = M['Enthalpy_Conference']
g1.add((enthalpy, RDF.type, SBUILDING.Enthalpy))
g1.add((enthalpy, RDF.type, PRIVVULN.TimeSeries))
g1.add((enthalpy, PRIVVULNV2.TemporalResolution, Literal("1200.0", datatype=XSD.double)))
g1.add((conference, PRIVVULNV2.has, enthalpy))

driver = Driver(debug_mode=True)
print("graph has %s statements." % len(g1))

folder = "output/paper/"
outputName = "Dong et al 2010"

g1 = driver.run(g1, folder + outputName)

print("graph has %s statements." % len(g1))

g1.serialize(folder+outputName+".rdf")