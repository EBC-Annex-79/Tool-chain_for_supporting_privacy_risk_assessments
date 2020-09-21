# from Templates.ITemplate import ITransformation
# from rdflib import Graph, Namespace, URIRef, Literal
# import Framework.namespace_util as NSUtil

# class PhotoplethysmographyToStress(ITransformation):
#     __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

#     def __init__(self):
#         self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
#         super().__init__(self.__DOMAINNAMESPACE__)

#     def _build_model(self):
#         inputNode = self.MODELS['inputRequirement1']
#         self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Photoplethysmography))

#         timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
#         self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
#         self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
#         self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

#         photoplethysmographyToStress = self.MODELS['PhotoplethysmographyToStress']
#         self.graph.add((photoplethysmographyToStress, self.RDF.type, self.PRIVVULN.Transformation))
#         self.graph.add((inputNode, self.PRIVVULN['feeds'], photoplethysmographyToStress))

#         stress = self.MODELS['Stress']
#         self.graph.add((stress, self.RDF.type, self.PRIVVULN.TimeSeries))
#         self.graph.add((stress, self.RDF.type, self.__DOMAINNAMESPACE__.Stress))
#         self.graph.add((photoplethysmographyToStress, self.PRIVVULN.feeds, stress))

