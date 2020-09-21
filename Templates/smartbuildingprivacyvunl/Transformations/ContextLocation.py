from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class ContextLocationPresenceAndScheduleActivitiesToRoomIdentity(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Presence))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ScheduleActivities))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ContextLocation))

        contextLocationPresenceAndScheduleActivitiesToRoomIdentity = self.MODELS['ContextLocationPresenceAndScheduleActivitiesToRoomIdentity']
        self.graph.add((contextLocationPresenceAndScheduleActivitiesToRoomIdentity, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], contextLocationPresenceAndScheduleActivitiesToRoomIdentity))
        self.graph.add((inputNode2, self.PRIVVULN['feeds'], contextLocationPresenceAndScheduleActivitiesToRoomIdentity))
        self.graph.add((inputNode3, self.PRIVVULN['feeds'], contextLocationPresenceAndScheduleActivitiesToRoomIdentity))

        contextIdentity = self.MODELS['ContextIdentity']
        self.graph.add((contextIdentity, self.RDF.type, self.PRIVVULN.Metadata))
        self.graph.add((contextIdentity, self.RDF.type, self.__DOMAINNAMESPACE__.ContextLocation))
        self.graph.add((contextLocationPresenceAndScheduleActivitiesToRoomIdentity, self.PRIVVULN.feeds, contextIdentity))

class ContextLocationOccupantCountAndScheduleActivitiesToRoomIdentity(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OccupantCount))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ScheduleActivities))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ContextLocation))

        contextLocationOccupantCountAndScheduleActivitiesToRoomIdentity = self.MODELS['ContextLocationOccupantCountAndScheduleActivitiesToRoomIdentity']
        self.graph.add((contextLocationOccupantCountAndScheduleActivitiesToRoomIdentity, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], contextLocationOccupantCountAndScheduleActivitiesToRoomIdentity))
        self.graph.add((inputNode2, self.PRIVVULN['feeds'], contextLocationOccupantCountAndScheduleActivitiesToRoomIdentity))
        self.graph.add((inputNode3, self.PRIVVULN['feeds'], contextLocationOccupantCountAndScheduleActivitiesToRoomIdentity))

        contextIdentity = self.MODELS['ContextIdentity']
        self.graph.add((contextIdentity, self.RDF.type, self.PRIVVULN.Metadata))
        self.graph.add((contextIdentity, self.RDF.type, self.__DOMAINNAMESPACE__.ContextLocation))
        self.graph.add((contextLocationOccupantCountAndScheduleActivitiesToRoomIdentity, self.PRIVVULN.feeds, contextIdentity))

class ContextLocationPresenceAndScheduleActivitiesToFloorIdentity(ITransformation):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Presence))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ScheduleActivities))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Building))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ContextLocation))

        contextLocationPresenceAndScheduleActivitiesToFloorIdentity = self.MODELS['ContextLocationPresenceAndScheduleActivitiesToFloorIdentity']
        self.graph.add((contextLocationPresenceAndScheduleActivitiesToFloorIdentity, self.RDF.type, self.PRIVVULN.Transformation))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], contextLocationPresenceAndScheduleActivitiesToFloorIdentity))
        self.graph.add((inputNode2, self.PRIVVULN['feeds'], contextLocationPresenceAndScheduleActivitiesToFloorIdentity))
        self.graph.add((inputNode3, self.PRIVVULN['feeds'], contextLocationPresenceAndScheduleActivitiesToFloorIdentity))

        contextIdentity = self.MODELS['ContextIdentity']
        self.graph.add((contextIdentity, self.RDF.type, self.PRIVVULN.Metadata))
        self.graph.add((contextIdentity, self.RDF.type, self.__DOMAINNAMESPACE__.ContextLocation))
        self.graph.add((contextLocationPresenceAndScheduleActivitiesToFloorIdentity, self.PRIVVULN.feeds, contextIdentity))

