from Templates.ITemplate import IPrivacyAttack
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

# class OccupantNetworkToSocialRelation(IPrivacyAttack):
#     __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

#     def __init__(self):
#         #DOI: 10.1145/3276774.3276779
#         self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
#         super().__init__(self.__DOMAINNAMESPACE__)

#     def _build_model(self):
#         inputNode = self.MODELS['inputRequirement1']
#         self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OccupantNetwork))
#         #Can be combined using a multiple sources, however, this makes the privacy score a bit geneal
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Space))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Wing))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))

#         occupantNetworkToSocialRelation = self.MODELS['OccupantNetworkToSocialRelation']
#         self.graph.add((occupantNetworkToSocialRelation, self.RDF.type, self.PRIVVULN.PrivacyAttack))
#         self.graph.add((inputNode, self.PRIVVULN['feeds'], occupantNetworkToSocialRelation))

#         socialRelation = self.MODELS['SocialRelation']
#         self.graph.add((socialRelation, self.RDF.type, self.PRIVVULN.PrivacyRisk))
#         self.graph.add((socialRelation, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
#         self.graph.add((occupantNetworkToSocialRelation, self.PRIVVULN.creates, socialRelation))
#         self.graph.add((socialRelation, self.PRIVVULNV2.privacyRiskScore, Literal("3", datatype=self.XSD.int)))

class OccupantNetworkToSocialRelationFloor(IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #DOI: 10.1145/3276774.3276779
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OccupantNetwork))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))

        occupantCountToOccupantActivities = self.MODELS['OccupantCountToOccupantActivities']
        self.graph.add((occupantCountToOccupantActivities, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], occupantCountToOccupantActivities))

        socialRelation = self.MODELS['SocialRelation']
        self.graph.add((socialRelation, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((socialRelation, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((occupantCountToOccupantActivities, self.PRIVVULN.creates, socialRelation))
        self.graph.add((socialRelation, self.PRIVVULNV2.privacyRiskScore, Literal("3", datatype=self.XSD.int)))


class OccupantNetworkToSocialRelationRoom(IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #DOI: 10.1145/3276774.3276779
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OccupantNetwork))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))

        occupantCountToOccupantActivities = self.MODELS['OccupantCountToOccupantActivities']
        self.graph.add((occupantCountToOccupantActivities, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], occupantCountToOccupantActivities))

        socialRelation = self.MODELS['SocialRelation']
        self.graph.add((socialRelation, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((socialRelation, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((occupantCountToOccupantActivities, self.PRIVVULN.creates, socialRelation))
        self.graph.add((socialRelation, self.PRIVVULNV2.privacyRiskScore, Literal("3", datatype=self.XSD.int)))

