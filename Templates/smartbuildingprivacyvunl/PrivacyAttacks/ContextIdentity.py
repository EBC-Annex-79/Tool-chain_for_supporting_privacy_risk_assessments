from Templates.ITemplate import IPrivacyAttack
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class ContextLocationToRoomIdentity (IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ContextLocation))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Room))

        contextLocationToRoomIdentity = self.MODELS['ContextLocationToRoomIdentity']
        self.graph.add((contextLocationToRoomIdentity, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN.feeds, contextLocationToRoomIdentity))

        contextIdentity = self.MODELS['ContextIdentity_Room']
        self.graph.add((contextIdentity, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((contextIdentity, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((contextLocationToRoomIdentity, self.PRIVVULN.creates, contextIdentity))
        self.graph.add((contextIdentity, self.PRIVVULNV2.privacyRiskScore, Literal("1", datatype=self.XSD.int)))

class ContextLocationToFloorIdentity (IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ContextLocation))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Floor))

        contextLocationToFloorIdentity = self.MODELS['ContextLocationToFloorIdentity']
        self.graph.add((contextLocationToFloorIdentity, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN.feeds, contextLocationToFloorIdentity))

        contextIdentity = self.MODELS['ContextIdentity_Floor']
        self.graph.add((contextIdentity, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((contextIdentity, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((contextLocationToFloorIdentity, self.PRIVVULN.creates, contextIdentity))
        self.graph.add((contextIdentity, self.PRIVVULNV2.privacyRiskScore, Literal("1", datatype=self.XSD.int)))

class ContextLocationOccupantCountAndScheduleActivitiesToTeachingPerformance (IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ContextLocation))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Teaching_Room))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ScheduleActivities))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Teaching_Room))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.OccupantCount))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Teaching_Room))

        contextLocationOccupantCountAndScheduleActivitiesToTeachingPerformance = self.MODELS['ContextLocationOccupantCountAndScheduleActivitiesToTeachingPerformance']
        self.graph.add((contextLocationOccupantCountAndScheduleActivitiesToTeachingPerformance, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN.feeds, contextLocationOccupantCountAndScheduleActivitiesToTeachingPerformance))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, contextLocationOccupantCountAndScheduleActivitiesToTeachingPerformance))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, contextLocationOccupantCountAndScheduleActivitiesToTeachingPerformance))

        teachingPerformance = self.MODELS['Teaching_Performance_based_On_Occupant_Count']
        self.graph.add((teachingPerformance, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((teachingPerformance, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((contextLocationOccupantCountAndScheduleActivitiesToTeachingPerformance, self.PRIVVULN.creates, teachingPerformance))
        self.graph.add((teachingPerformance, self.PRIVVULNV2.privacyRiskScore, Literal("1", datatype=self.XSD.int)))

class ContextLocationPresenceAndScheduleActivitiesToTeachingPerformance (IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ContextLocation))
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Teaching_Room))

        inputNode2 = self.MODELS['inputRequirement2']
        self.graph.add((inputNode2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ScheduleActivities))
        self.graph.add((inputNode2, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Teaching_Room))

        inputNode3 = self.MODELS['inputRequirement3']
        self.graph.add((inputNode3, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode3, self.PRIVVULNV2.TemporalResolution, Literal("900", datatype=self.XSD.double)))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((inputNode3, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Teaching_Room))

        contextLocationPresenceAndScheduleActivitiesToTeachingPerformance = self.MODELS['ContextLocationPresenceAndScheduleActivitiesToTeachingPerformance']
        self.graph.add((contextLocationPresenceAndScheduleActivitiesToTeachingPerformance, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN.feeds, contextLocationPresenceAndScheduleActivitiesToTeachingPerformance))
        self.graph.add((inputNode2, self.PRIVVULN.feeds, contextLocationPresenceAndScheduleActivitiesToTeachingPerformance))
        self.graph.add((inputNode3, self.PRIVVULN.feeds, contextLocationPresenceAndScheduleActivitiesToTeachingPerformance))

        teachingPerformance = self.MODELS['Teaching_Performance_based_On_Presence']
        self.graph.add((teachingPerformance, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((teachingPerformance, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((contextLocationPresenceAndScheduleActivitiesToTeachingPerformance, self.PRIVVULN.creates, teachingPerformance))
        self.graph.add((teachingPerformance, self.PRIVVULNV2.privacyRiskScore, Literal("1", datatype=self.XSD.int)))