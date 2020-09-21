from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class CountingLineToOccupantCountRoom(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.CountingLine))

        countingLineToOccupantCount = self.MODELS['CountingLineToOccupantCount']
        self.graph.add((countingLineToOccupantCount, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], countingLineToOccupantCount))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        occupantCount = self.MODELS['OccupantCount']
        self.graph.add((occupantCount, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantCount))
        self.graph.add((countingLineToOccupantCount, self.PRIVVULN['feeds'], occupantCount))
        self.graph.add((occupantCount, self.RDF.type, self.PRIVVULN.TimeSeries))

class PresenceCO2AndTemperatureToOccupantCount(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Presence))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Temperature))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.CO2))

        presenceCO2AndTemperatureToOccupantCount = self.MODELS['PresenceCO2AndTemperatureToOccupantCount']
        self.graph.add((presenceCO2AndTemperatureToOccupantCount, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], presenceCO2AndTemperatureToOccupantCount))
        self.graph.add((inputNode2, self.PRIVVULN['feeds'], presenceCO2AndTemperatureToOccupantCount))
        self.graph.add((inputNode3, self.PRIVVULN['feeds'], presenceCO2AndTemperatureToOccupantCount))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        timeResolutionLinear2 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear2, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear2, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear2, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, timeResolutionLinear2))

        timeResolutionLinear3 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear3, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear3, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear3, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, timeResolutionLinear3))

        occupantCount = self.MODELS['OccupantCount']
        self.graph.add((occupantCount, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantCount))
        self.graph.add((presenceCO2AndTemperatureToOccupantCount, self.PRIVVULN['feeds'], occupantCount))
        self.graph.add((occupantCount, self.RDF.type, self.PRIVVULN.TimeSeries))

class CountingLineToOccupantCountFloor(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.CountingLine))

        countingLineToOccupantCountFloor = self.MODELS['CountingLineToOccupantCountFloor']
        self.graph.add((countingLineToOccupantCountFloor, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], countingLineToOccupantCountFloor))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        spatialResolution1 = self.MODELS['SpatialResolution1']
        self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        occupantCount = self.MODELS['OccupantCount']
        self.graph.add((occupantCount, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantCount))
        self.graph.add((occupantCount, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((countingLineToOccupantCountFloor, self.PRIVVULN['feeds'], occupantCount))



class CO2ToOccupantCount(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()
    # doi:10.1016/j.enbuild.2010.01.016

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.DESK))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.CO2))

        cO2ToOccupantCount = self.MODELS['CO2ToOccupantCount']
        self.graph.add((cO2ToOccupantCount, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], cO2ToOccupantCount))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        occupantCount = self.MODELS['OccupantCount']
        self.graph.add((occupantCount, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantCount))
        self.graph.add((occupantCount, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((cO2ToOccupantCount, self.PRIVVULN['feeds'], occupantCount))


# class NoiseToOccupantCount(ITransformation):
#     __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

#     def __init__(self):
#         self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
#         super().__init__(self.__DOMAINNAMESPACE__)

#     def _build_model(self):
#         inputNode = self.MODELS['inputRequirement1']
#         self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.DESK))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Noise))

#         noiseToOccupantCount = self.MODELS['NoiseToOccupantCount']
#         self.graph.add((noiseToOccupantCount, self.RDF.type, self.PRIVVULN.Transformation))
#         self.graph.add((inputNode, self.PRIVVULN['feeds'], noiseToOccupantCount))

#         timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
#         self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
#         self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
#         self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

#         occupantCount = self.MODELS['OccupantCount']
#         self.graph.add((occupantCount, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantCount))
#         self.graph.add((occupantCount, self.RDF.type, self.PRIVVULN.TimeSeries))
#         self.graph.add((noiseToOccupantCount, self.PRIVVULN['feeds'], occupantCount))