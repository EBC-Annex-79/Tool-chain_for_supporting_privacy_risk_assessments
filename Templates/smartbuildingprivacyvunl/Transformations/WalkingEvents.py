from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class WalkingEventsToOccupantActivities(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.WalkingEvents))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("0", datatype=self.XSD.double))) #Event
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Door))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        spatialResolution1 = self.MODELS['SpatialResolution1']
        self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Door))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        walkingEventsToOccupantActivities = self.MODELS['WalkingEventsToOccupantActivities']
        self.graph.add((walkingEventsToOccupantActivities, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], walkingEventsToOccupantActivities))

        occupantActivities = self.MODELS['OccupantActivities']
        self.graph.add((occupantActivities, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantActivities))
        self.graph.add((walkingEventsToOccupantActivities, self.PRIVVULN['feeds'], occupantActivities))
        self.graph.add((occupantActivities, self.RDF.type, self.PRIVVULN.TimeSeries))
