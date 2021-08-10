from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class TimeTempAndCountsToPowerMeter(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #DOI: 10.1145/2993422.2993427
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Timestamp))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Outside))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Temperature))
        self.graph.add((inputNode2, self.PRIVVULNV2.TemporalResolution, Literal("300", datatype=self.XSD.double)))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Office_Room))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OccupantCount))
        self.graph.add((inputNode3, self.PRIVVULNV2.TemporalResolution, Literal("300", datatype=self.XSD.double)))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Office_Room))

        timeTempAndCountsToSmartMeter = self.MODELS['TimeTempAndCountsToSmartMeter']
        self.graph.add((timeTempAndCountsToSmartMeter, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeTempAndCountsToSmartMeter))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, timeTempAndCountsToSmartMeter))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, timeTempAndCountsToSmartMeter))

        powerMeter = self.MODELS['PowerMeter']
        self.graph.add((powerMeter, self.RDF.type, self.__DOMAINNAMESPACE__.PowerMeter))
        self.graph.add((timeTempAndCountsToSmartMeter, self.PRIVVULN['feeds'], powerMeter))
        self.graph.add((powerMeter, self.RDF.type, self.PRIVVULN.TimeSeries))