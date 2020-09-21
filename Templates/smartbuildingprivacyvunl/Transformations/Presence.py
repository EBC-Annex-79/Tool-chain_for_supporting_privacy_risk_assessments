from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class CountingLineToPresence(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("300", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.CountingLine))

        countingLineToPresence = self.MODELS['CountingLineToPresence']
        self.graph.add((countingLineToPresence, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], countingLineToPresence))

        # spatialResolution1 = self.MODELS['SpatialResolution1']
        # self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        # self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Room))
        # self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Room))
        # self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        # spatialResolution2 = self.MODELS['SpatialResolution2']
        # self.graph.add((spatialResolution2, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        # self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Teaching_Room))
        # self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Teaching_Room))
        # self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution2))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        presenceStream = self.MODELS['PresenceStream']
        self.graph.add((presenceStream, self.RDF.type, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((countingLineToPresence, self.PRIVVULN['feeds'], presenceStream))
        self.graph.add((presenceStream, self.RDF.type, self.PRIVVULN.TimeSeries))


class PIRToPresence(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("300", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.PIR))

        pirToPresence = self.MODELS['PIRToPresence']
        self.graph.add((pirToPresence, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], pirToPresence))

        # spatialResolution1 = self.MODELS['SpatialResolution1']
        # self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        # self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Room))
        # self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Room))
        # self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        presenceStream = self.MODELS['PresenceStream']
        self.graph.add((presenceStream, self.RDF.type, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((pirToPresence, self.PRIVVULN['feeds'], presenceStream))
        self.graph.add((presenceStream, self.RDF.type, self.PRIVVULN.TimeSeries))

class DoorOpenAndPIRToPresence(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("300", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.DoorOpen))

        inputRequirement2 = self.MODELS['inputRequirement2']
        self.graph.add((inputRequirement2, self.RDF.type, self.PRIVVULNV2.Require))
        self.graph.add((inputRequirement2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.PIR))
        self.graph.add((inputRequirement2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputRequirement2, self.PRIVVULNV2.TemporalResolution, Literal("300", datatype=self.XSD.double)))

        doorOpenToPressens = self.MODELS['DoorOpenAndPIRToPresence']
        self.graph.add((doorOpenToPressens, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], doorOpenToPressens))
        self.graph.add((inputRequirement2, self.PRIVVULN['feeds'], doorOpenToPressens))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        timeResolutionLinear2 = self.MODELS['timeResolutionLinear2']
        self.graph.add((timeResolutionLinear2, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((doorOpenToPressens, self.PRIVVULN.TimeFactor, timeResolutionLinear2))
        self.graph.add((timeResolutionLinear2, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear2, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputRequirement2, self.PRIVVULN.feeds, timeResolutionLinear2))

        spatialResolution1 = self.MODELS['SpatialResolution1']
        self.graph.add((spatialResolution1, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((spatialResolution1, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULN.feeds, spatialResolution1))

        spatialResolution2 = self.MODELS['spatialResolution2']
        self.graph.add((spatialResolution2, self.RDF.type, self.PRIVVULNV2.SpatialResolution))
        self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialInput, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((spatialResolution2, self.PRIVVULNV2.spatialOutput, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputRequirement2, self.PRIVVULN.feeds, spatialResolution2))

        presenceStream = self.MODELS['PresenceStream']
        self.graph.add((presenceStream, self.RDF.type, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((doorOpenToPressens, self.PRIVVULN['feeds'], presenceStream))
        self.graph.add((presenceStream, self.RDF.type, self.PRIVVULN.TimeSeries))

class PowerMeterToPresence(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.PowerMeter))

        meanThresholdingDetectionForOccupied = self.MODELS['MeanThresholdingDetectionForOccupied']
        self.graph.add((meanThresholdingDetectionForOccupied, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], meanThresholdingDetectionForOccupied))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        presenceStream = self.MODELS['PresenceStream']
        self.graph.add((presenceStream, self.RDF.type, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((meanThresholdingDetectionForOccupied, self.PRIVVULN['feeds'], presenceStream))
        self.graph.add((presenceStream, self.RDF.type, self.PRIVVULN.TimeSeries))

class CO2ToPresence(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Desk))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.CO2))

        cO2ToPresence = self.MODELS['CO2ToPresence']
        self.graph.add((cO2ToPresence, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], cO2ToPresence))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        presenceStream = self.MODELS['PresenceStream']
        self.graph.add((presenceStream, self.RDF.type, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((cO2ToPresence, self.PRIVVULN['feeds'], presenceStream))
        self.graph.add((presenceStream, self.RDF.type, self.PRIVVULN.TimeSeries))


class VAVToPresence(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.VariableAirVolume))

        timeResolutionLinear1 = self.MODELS['timeResolutionLinear1']
        self.graph.add((timeResolutionLinear1, self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeInput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((timeResolutionLinear1, self.PRIVVULNV2.TimeOutput, Literal("1",datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULN.feeds, timeResolutionLinear1))

        vAVToPresence = self.MODELS['VAVToPresence']
        self.graph.add((vAVToPresence, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], vAVToPresence))

        presenceStream = self.MODELS['PresenceStream']
        self.graph.add((presenceStream, self.RDF.type, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((vAVToPresence, self.PRIVVULN['feeds'], presenceStream))
        self.graph.add((presenceStream, self.RDF.type, self.PRIVVULN.TimeSeries))