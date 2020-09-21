from Templates.ITemplate import IPrivacyAttack
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class OccupantActivitiesOccupantIdentity (IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OccupantActivities))
        # self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("0", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Door))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))

        occupantActivitiesOccupantIdentity = self.MODELS['OccupantActivitiesOccupantIdentity']
        self.graph.add((occupantActivitiesOccupantIdentity, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN.feeds, occupantActivitiesOccupantIdentity))

        occupantIdentity = self.MODELS['OccupantIdentity']
        self.graph.add((occupantIdentity, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((occupantIdentity, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((occupantActivitiesOccupantIdentity, self.PRIVVULN.creates, occupantIdentity))
        self.graph.add((occupantIdentity, self.PRIVVULNV2.privacyRiskScore, Literal("4", datatype=self.XSD.int)))