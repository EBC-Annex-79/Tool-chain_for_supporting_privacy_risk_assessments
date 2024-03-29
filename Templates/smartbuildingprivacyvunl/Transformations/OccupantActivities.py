from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class PlugloadToOccupantActivitiesDesk(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Desk))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.PowerMeter))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        plugloadToOccupantActivitiesDesk = self.MODELS['PlugloadToOccupantActivitiesDesk']
        self.graph.add((plugloadToOccupantActivitiesDesk, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], plugloadToOccupantActivitiesDesk))

        occupantActivities = self.MODELS['OccupantActivities']
        self.graph.add((occupantActivities, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((occupantActivities, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantActivities))
        self.graph.add((plugloadToOccupantActivitiesDesk, self.PRIVVULN.feeds, occupantActivities))

class PlugloadToOccupantActivitiesPrivateOffice(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Single_Office_Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.PowerMeter))

        plugloadToOccupantActivitiesSingleOfficeRoom = self.MODELS['PlugloadToOccupantActivitiesSingleOfficeRoom']
        self.graph.add((plugloadToOccupantActivitiesSingleOfficeRoom, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], plugloadToOccupantActivitiesSingleOfficeRoom))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        occupantActivities = self.MODELS['OccupantActivities']
        self.graph.add((occupantActivities, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((occupantActivities, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantActivities))
        self.graph.add((plugloadToOccupantActivitiesSingleOfficeRoom, self.PRIVVULN.feeds, occupantActivities))

class ChannelStateInformationToOccupantActivities(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        #doi: 10.1145/3408308.3427624
        #doi: 10.1145/3408308.3427983
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("0.1", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ChannelStateInformation))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        channelStateInformationToOccupantActivities = self.MODELS['ChannelStateInformationToOccupantActivities']
        self.graph.add((channelStateInformationToOccupantActivities, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], channelStateInformationToOccupantActivities))

        occupantActivities = self.MODELS['OccupantActivities']
        self.graph.add((occupantActivities, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((occupantActivities, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantActivities))
        self.graph.add((channelStateInformationToOccupantActivities, self.PRIVVULN.feeds, occupantActivities))

class WalkingEventsToOccupantActivities(ITransformation):
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

# class AccelerometerToOccupantActivities(ITransformation):
#     __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

#     def __init__(self):
#         self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
#         super().__init__(self.__DOMAINNAMESPACE__)

#     def _build_model(self):
#         inputNode = self.MODELS['inputRequirement1']
#         self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Accelerometer))

#         timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
#         self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
#         self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
#         self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

#         accelerometerToOccupantActivities = self.MODELS['AccelerometerToOccupantActivities']
#         self.graph.add((accelerometerToOccupantActivities, self.RDF.type, self.PRIVVULN.Transformation))
#         self.graph.add((inputNode, self.PRIVVULN['feeds'], accelerometerToOccupantActivities))

#         occupantActivities = self.MODELS['OccupantActivities']
#         self.graph.add((occupantActivities, self.RDF.type, self.PRIVVULN.TimeSeries))
#         self.graph.add((occupantActivities, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantActivities))
#         self.graph.add((accelerometerToOccupantActivities, self.PRIVVULN.feeds, occupantActivities))

# class ThermometerToOccupantActivities(ITransformation):
#     __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

#     def __init__(self):
#         self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
#         super().__init__(self.__DOMAINNAMESPACE__)

#     def _build_model(self):
#         inputNode = self.MODELS['inputRequirement1']
#         self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
#         self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
#         self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Occupant))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Thermometer))

#         timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
#         self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
#         self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
#         self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
#         self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

#         thermometerToOccupantActivities = self.MODELS['ThermometerToOccupantActivities']
#         self.graph.add((thermometerToOccupantActivities, self.RDF.type, self.PRIVVULN.Transformation))
#         self.graph.add((inputNode, self.PRIVVULN['feeds'], thermometerToOccupantActivities))

#         occupantActivities = self.MODELS['OccupantActivities']
#         self.graph.add((occupantActivities, self.RDF.type, self.PRIVVULN.TimeSeries))
#         self.graph.add((occupantActivities, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantActivities))
#         self.graph.add((thermometerToOccupantActivities, self.PRIVVULN.feeds, occupantActivities))

class SkeletonJointsToOccupantActivities(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal(0.03, datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Door))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Zone))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.SkeletonJoints))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        skeletonJointsToOccupantActivities = self.MODELS['SkeletonJointsToOccupantActivities']
        self.graph.add((skeletonJointsToOccupantActivities, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], skeletonJointsToOccupantActivities))

        occupantActivities = self.MODELS['OccupantActivities']
        self.graph.add((occupantActivities, self.RDF.type, self.PRIVVULN.TimeSeries))
        self.graph.add((occupantActivities, self.RDF.type, self.__DOMAINNAMESPACE__.OccupantActivities))
        self.graph.add((skeletonJointsToOccupantActivities, self.PRIVVULN.feeds, occupantActivities))
