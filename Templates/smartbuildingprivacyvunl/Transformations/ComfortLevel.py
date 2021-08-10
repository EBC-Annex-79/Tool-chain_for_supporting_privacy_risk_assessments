from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class TemperatureSkinTemperatureToComfortLevel(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #doi: 10.1145/3360322.3360858
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("30", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Temperature))

        spatialResolution1 = self.MODELS['SpatialResolution1']
        self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        spatialResolution2 = self.MODELS['SpatialResolution2']
        self.graph.add((spatialResolution2, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution2))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.SkinTemperature))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ClothingInsulation))

        inputNode4 = self.MODELS['inputRequirement4']
        self.graph.add((inputNode4, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode4, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode4, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Height))

        inputNode5 = self.MODELS['inputRequirement5']
        self.graph.add((inputNode5, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode5, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode5, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ShoulderCircumference))

        inputNode6 = self.MODELS['inputRequirement6']
        self.graph.add((inputNode6, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode6, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode6, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Wight))

        inputNode7 = self.MODELS['inputRequirement7']
        self.graph.add((inputNode7, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode7, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode7, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Gender))

        inputNode8 = self.MODELS['inputRequirement8']
        self.graph.add((inputNode8, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode8, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
        self.graph.add((inputNode8, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((inputNode8, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OutdoorTemperature))

        spatialResolution3 = self.MODELS['SpatialResolution3']
        self.graph.add((spatialResolution3, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution3, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((spatialResolution3, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode8, self.PRIVVULN.feeds, spatialResolution3))

        inputNode9 = self.MODELS['inputRequirement9']
        self.graph.add((inputNode9, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode9, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
        self.graph.add((inputNode9, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((inputNode9, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OutdoorHumidity))

        spatialResolution4 = self.MODELS['SpatialResolution4']
        self.graph.add((spatialResolution4, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution4, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((spatialResolution4, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode9, self.PRIVVULN.feeds, spatialResolution4))

        inputNode10 = self.MODELS['inputRequirement10']
        self.graph.add((inputNode10, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode10, self.PRIVVULNV2.TemporalResolution, Literal("300", datatype=self.XSD.double)))
        self.graph.add((inputNode10, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode10, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ThermalComfort))

        spatialResolution5 = self.MODELS['SpatialResolution5']
        self.graph.add((spatialResolution5, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution5, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((spatialResolution5, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode10, self.PRIVVULN.feeds, spatialResolution5))

        inputNode11 = self.MODELS['inputRequirement11']
        self.graph.add((inputNode11, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode11, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
        self.graph.add((inputNode11, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode11, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.HeartRate))

        inputNode12 = self.MODELS['inputRequirement12']
        self.graph.add((inputNode12, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode12, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
        self.graph.add((inputNode12, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode12, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.GalvanicSkinResponseFeedback))

        temperatureSkinTemperatureToComfortLevel = self.MODELS['TemperatureSkinTemperatureToComfortLevel']
        self.graph.add((temperatureSkinTemperatureToComfortLevel, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode2, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode3, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode4, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode5, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode6, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode7, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode8, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode9, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode10, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode11, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode12, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))

        comfortLevel = self.MODELS['ComfortLevel']
        self.graph.add((comfortLevel, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((comfortLevel, self.RDF.type, self.__DOMAINNAMESPACE__.ComfortLevel))
        self.graph.add((temperatureSkinTemperatureToComfortLevel, self.PRIVVULN.feeds, comfortLevel))

class TemperatureSkinTemperatureV2ToComfortLevel(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #doi: 10.1145/3408308.3427612
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("30", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Temperature))

        spatialResolution1 = self.MODELS['SpatialResolution1']
        self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        spatialResolution2 = self.MODELS['SpatialResolution2']
        self.graph.add((spatialResolution2, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution2))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.SkinTemperature))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ClothingInsulation))

        inputNode4 = self.MODELS['inputRequirement4']
        self.graph.add((inputNode4, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode4, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode4, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Height))

        inputNode5 = self.MODELS['inputRequirement5']
        self.graph.add((inputNode5, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode5, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode5, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ShoulderCircumference))

        inputNode6 = self.MODELS['inputRequirement6']
        self.graph.add((inputNode6, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode6, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode6, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Wight))

        inputNode7 = self.MODELS['inputRequirement7']
        self.graph.add((inputNode7, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode7, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode7, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Gender))

        inputNode8 = self.MODELS['inputRequirement8']
        self.graph.add((inputNode8, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode8, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
        self.graph.add((inputNode8, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((inputNode8, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OutdoorTemperature))

        spatialResolution3 = self.MODELS['SpatialResolution3']
        self.graph.add((spatialResolution3, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution3, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((spatialResolution3, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode8, self.PRIVVULN.feeds, spatialResolution3))

        inputNode9 = self.MODELS['inputRequirement9']
        self.graph.add((inputNode9, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode9, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
        self.graph.add((inputNode9, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((inputNode9, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OutdoorHumidity))

        spatialResolution4 = self.MODELS['SpatialResolution4']
        self.graph.add((spatialResolution4, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution4, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((spatialResolution4, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode9, self.PRIVVULN.feeds, spatialResolution4))

        inputNode10 = self.MODELS['inputRequirement10']
        self.graph.add((inputNode10, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode10, self.PRIVVULNV2.TemporalResolution, Literal("300", datatype=self.XSD.double)))
        self.graph.add((inputNode10, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode10, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ThermalComfort))

        spatialResolution5 = self.MODELS['SpatialResolution5']
        self.graph.add((spatialResolution5, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution5, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Outside))
        self.graph.add((spatialResolution5, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
        self.graph.add((inputNode10, self.PRIVVULN.feeds, spatialResolution5))

        temperatureSkinTemperatureToComfortLevel = self.MODELS['TemperatureSkinTemperatureToComfortLevel']
        self.graph.add((temperatureSkinTemperatureToComfortLevel, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode2, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode3, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode4, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode5, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode6, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode7, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode8, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode9, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))
        self.graph.add((inputNode10, self.PRIVVULN['feeds'], temperatureSkinTemperatureToComfortLevel))

        comfortLevel = self.MODELS['ComfortLevel']
        self.graph.add((comfortLevel, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((comfortLevel, self.RDF.type, self.__DOMAINNAMESPACE__.ComfortLevel))
        self.graph.add((temperatureSkinTemperatureToComfortLevel, self.PRIVVULN.feeds, comfortLevel))

