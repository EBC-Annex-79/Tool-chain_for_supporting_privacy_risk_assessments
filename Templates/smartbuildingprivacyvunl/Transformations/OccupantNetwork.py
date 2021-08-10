from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class OccupantActivitiesToOccupantNetworkRoom(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #DOI: 10.1145/3276774.3276779
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Desk))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OccupantActivities))

        spatialResolution1 = self.MODELS['SpatialResolution1']
        self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Desk))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        occupantActivitiesToOccupantNetwork = self.MODELS['OccupantActivitiesToOccupantNetworkRoom']
        self.graph.add((occupantActivitiesToOccupantNetwork, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], occupantActivitiesToOccupantNetwork))

        occupantNetwork = self.MODELS['OccupantNetwork']
        self.graph.add((occupantNetwork, self.RDF.type, self.PRIVVULN.Graph))
        self.graph.add((occupantNetwork, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantNetwork))
        self.graph.add((occupantActivitiesToOccupantNetwork, self.PRIVVULN.feeds, occupantNetwork))

class OccupantActivitiesToOccupantNetworkFloor(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Desk))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OccupantActivities))

        spatialResolution1 = self.MODELS['SpatialResolution1']
        self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        spatialResolution2 = self.MODELS['SpatialResolution2']
        self.graph.add((spatialResolution2, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Desk))
        self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution2))

        occupantActivitiesToOccupantNetwork = self.MODELS['OccupantActivitiesToOccupantNetworkFloor']
        self.graph.add((occupantActivitiesToOccupantNetwork, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], occupantActivitiesToOccupantNetwork))

        occupantNetwork = self.MODELS['OccupantNetwork']
        self.graph.add((occupantNetwork, self.RDF.type, self.PRIVVULN.Graph))
        self.graph.add((occupantNetwork, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantNetwork))
        self.graph.add((occupantActivitiesToOccupantNetwork, self.PRIVVULN.feeds, occupantNetwork))
