from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

# class GenderYearOfBirthAndContextLocationToOccupantIdentity(ITransformation):
#     __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

#     def __init__(self):
#         self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
#         super().__init__(self.__DOMAINNAMESPACE__)

#     def _build_model(self):
#         inputNode = self.MODELS['inputRequirement1']
#         self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Gender))

#         inputNode2 = self.MODELS['inputRequirement2']
#         self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.YearOfBirth))

#         inputNode3 = self.MODELS['inputRequirement3']
#         self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ContextLocation))
#         self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
#         self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))

#         spatialResolution = self.MODELS['spatialResolution']
#         self.graph.add((spatialResolution, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
#         self.graph.add((spatialResolution, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((spatialResolution, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution))

#         spatialResolution1 = self.MODELS['spatialResolution1']
#         self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
#         self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((inputNode2, self.PRIVVULN.feeds, spatialResolution1))

#         spatialResolution2 = self.MODELS['spatialResolution2']
#         self.graph.add((spatialResolution2, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
#         self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Room))
#         self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((inputNode3, self.PRIVVULN.feeds, spatialResolution2))

#         genderYearOfBirthAndContextLocationToOccupantIdentity = self.MODELS['GenderYearOfBirthAndContextLocationToOccupantIdentity']
#         self.graph.add((genderYearOfBirthAndContextLocationToOccupantIdentity, self.RDF.type, self.PRIVVULN.Transformation))
#         self.graph.add((inputNode, self.PRIVVULN['feeds'], genderYearOfBirthAndContextLocationToOccupantIdentity))
#         self.graph.add((inputNode2, self.PRIVVULN['feeds'], genderYearOfBirthAndContextLocationToOccupantIdentity))
#         self.graph.add((inputNode3, self.PRIVVULN['feeds'], genderYearOfBirthAndContextLocationToOccupantIdentity))

#         occupantIdentity = self.MODELS['OccupantIdentity']
#         self.graph.add((occupantIdentity, self.RDF.type, self.PRIVVULN.Metadata))
#         self.graph.add((occupantIdentity, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantIdentity))
#         self.graph.add((genderYearOfBirthAndContextLocationToOccupantIdentity, self.PRIVVULN.feeds, occupantIdentity))


class WalkingEventsToOccupantIdentity(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #DOI: 10.1145/3137133.3137154
        #DOI: 10.1145/2993422.2993429
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.WalkingEvents))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("0", datatype=self.XSD.double))) #Event
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Door))

        spatialResolution1 = self.MODELS['SpatialResolution1']
        self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Door))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        walkingEventsToOccupantIdentity = self.MODELS['WalkingEventsToOccupantIdentity']
        self.graph.add((walkingEventsToOccupantIdentity, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], walkingEventsToOccupantIdentity))

        occupantIdentities = self.MODELS['OccupantIdentities']
        self.graph.add((occupantIdentities, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantIdentity))
        self.graph.add((occupantIdentities, self.RDF.type, self.PRIVVULN.Metadata))
        self.graph.add((walkingEventsToOccupantIdentity, self.PRIVVULN['feeds'], occupantIdentities))

