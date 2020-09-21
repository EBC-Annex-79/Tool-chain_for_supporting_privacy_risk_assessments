# from Templates.ITemplate import IPrivacyAttack
# from rdflib import Graph, Namespace, URIRef, Literal
# import Framework.namespace_util as NSUtil

# class CountingLineToOccupantActivities(IPrivacyAttack):
#     __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

#     def __init__(self):
#         self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
#         super().__init__(self.__DOMAINNAMESPACE__)

#     def _build_model(self):
#         inputNode = self.MODELS['inputRequirement1']
#         self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double)))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.CountingLine))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))

#         occupantCountToOccupantActivities = self.MODELS['OccupantCountToOccupantActivities']
#         self.graph.add((occupantCountToOccupantActivities, self.RDF.type, self.PRIVVULN.PrivacyAttack))
#         self.graph.add((inputNode, self.PRIVVULN['feeds'], occupantCountToOccupantActivities))

#         occupantActivities = self.MODELS['OccupantActivities']
#         self.graph.add((occupantActivities, self.RDF.type, self.PRIVVULN.PrivacyRisk))
#         self.graph.add((occupantActivities, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
#         self.graph.add((occupantCountToOccupantActivities, self.PRIVVULN.creates, occupantActivities))

