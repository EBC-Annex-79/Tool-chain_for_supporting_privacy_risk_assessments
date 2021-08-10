from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class UltrasonicDistanceToWalkingEvents(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #DOI: 10.1145/3137133.3137154
        #DOI: 10.1145/2993422.2993429
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.UltrasonicDistance))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("0", datatype=self.XSD.double))) #Event
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Door))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        ultrasonicDistanceToWalkingEvents = self.MODELS['UltrasonicDistanceToWalkingEvents']
        self.graph.add((ultrasonicDistanceToWalkingEvents, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN.feeds, ultrasonicDistanceToWalkingEvents))

        walkingEvents = self.MODELS['WalkingEvents']
        self.graph.add((walkingEvents, self.RDF.type, self.__DOMAINNAMESPACE__.WalkingEvents))
        self.graph.add((ultrasonicDistanceToWalkingEvents, self.PRIVVULN['feeds'], walkingEvents))
        self.graph.add((walkingEvents, self.RDF.type, self.PRIVVULN.TimeSeries))