# from Templates.ITemplate import IPrivacyAttack
# from rdflib import Graph, Namespace, URIRef, Literal
# import Framework.namespace_util as NSUtil

# class ContextLocationToRoomIdentity (IPrivacyAttack):
#     __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_health()

#     def __init__(self):
#         self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
#         super().__init__(self.__DOMAINNAMESPACE__)

#     def _build_model(self):
#         inputNode = self.MODELS['inputRequirement']
#         self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ContextLocation))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Human))

#         contextLocationToRoomIdentity = self.MODELS['ContextLocationToRoomIdentity']
#         self.graph.add((contextLocationToRoomIdentity, self.RDF.type, self.PRIVVULN.PrivacyAttack))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, contextLocationToRoomIdentity))

#         contextIdentity = self.MODELS['ContextIdentity_Room']
#         self.graph.add((contextIdentity, self.RDF.type, self.PRIVVULN.PrivacyRisk))
#         self.graph.add((contextIdentity, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
#         self.graph.add((contextLocationToRoomIdentity, self.PRIVVULN.creates, contextIdentity))
#         self.graph.add((contextIdentity, self.PRIVVULNV2.privacyRiskScore, Literal("5", datatype=self.XSD.int)))