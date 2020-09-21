from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class SkeletonJointsSkeletonModelAndTypicalBodyShapeToLimbMass(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("1", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Door))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.SkeletonJoints))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.SkeletonModel))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.TypicalBodyShape))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        skeletonJointsSkeletonModelAndTypicalBodyShapeToLimbMass = self.MODELS['SkeletonJointsSkeletonModelAndTypicalBodyShapeToLimbMass']
        self.graph.add((skeletonJointsSkeletonModelAndTypicalBodyShapeToLimbMass, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], skeletonJointsSkeletonModelAndTypicalBodyShapeToLimbMass))
        self.graph.add((inputNode2, self.PRIVVULN['feeds'], skeletonJointsSkeletonModelAndTypicalBodyShapeToLimbMass))
        self.graph.add((inputNode3, self.PRIVVULN['feeds'], skeletonJointsSkeletonModelAndTypicalBodyShapeToLimbMass))

        limbMass = self.MODELS['LimbMass']
        self.graph.add((limbMass, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((limbMass, self.RDF.type, self.__DOMAINNAMESPACE__.LimbMass))
        self.graph.add((skeletonJointsSkeletonModelAndTypicalBodyShapeToLimbMass, self.PRIVVULN.feeds, limbMass))