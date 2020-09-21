from Templates.ITemplate import IPrivacyAttack
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class LimbMassLimbSurfaceAreaAndAverageBMIToWeight(IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.LimbMass))
        # self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("450", datatype=self.XSD.double)))
        #Can be combined using a multiple sources, however, this makes the privacy score a bit geneal
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Space))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Wing))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Door))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.LimbSurfaceArea))
        # self.graph.add((inputNode2, self.PRIVVULNV2.TemporalResolution, Literal("450", datatype=self.XSD.double)))
        #Can be combined using a multiple sources, however, this makes the privacy score a bit geneal
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Space))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Wing))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Door))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.AverageBMI))

        limbMassLimbSurfaceAreaAndAverageBMIToWeight = self.MODELS['LimbMassLimbSurfaceAreaAndAverageBMIToWeight']
        self.graph.add((limbMassLimbSurfaceAreaAndAverageBMIToWeight, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], limbMassLimbSurfaceAreaAndAverageBMIToWeight))
        self.graph.add((inputNode2, self.PRIVVULN['feeds'], limbMassLimbSurfaceAreaAndAverageBMIToWeight))
        self.graph.add((inputNode3, self.PRIVVULN['feeds'], limbMassLimbSurfaceAreaAndAverageBMIToWeight))

        weight = self.MODELS['Weight']
        self.graph.add((weight, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((weight, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((limbMassLimbSurfaceAreaAndAverageBMIToWeight, self.PRIVVULN.creates, weight))
        self.graph.add((weight, self.PRIVVULNV2.privacyRiskScore, Literal("3", datatype=self.XSD.int)))