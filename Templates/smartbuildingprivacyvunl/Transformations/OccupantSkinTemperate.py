from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class CamaraThermalCameraToSkinTemperate(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #DOI: 10.1145/3360322.3360848
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ThermalCamera))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("1", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))


        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Camera))
        self.graph.add((inputNode2, self.PRIVVULNV2.TemporalResolution, Literal("1", datatype=self.XSD.double)))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))

        timeResolutionLinear2 = self.MODELS['timeResolutionLinear2']
        self.graph.add((timeResolutionLinear2, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear2, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear2, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, timeResolutionLinear2))

        camaraThermalCameraToOccupantSkinTemperate = self.MODELS['CamaraThermalCameraToOccupantSkinTemperate']
        self.graph.add((camaraThermalCameraToOccupantSkinTemperate, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], camaraThermalCameraToOccupantSkinTemperate))
        self.graph.add((inputNode2, self.PRIVVULN['feeds'], camaraThermalCameraToOccupantSkinTemperate))

        occupantSkinTemperate = self.MODELS['OccupantSkinTemperate']
        self.graph.add((occupantSkinTemperate, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((occupantSkinTemperate, self.RDF.type, self.__DOMAINNAMESPACE__.SkinTemperature))
        self.graph.add((camaraThermalCameraToOccupantSkinTemperate, self.PRIVVULN.feeds, occupantSkinTemperate))