from Templates.ITemplate import IPrivacyAttack
from rdflib import Graph, Namespace, URIRef, Literal
import Framework.namespace_util as NSUtil

class PresenceToOccupantOfficeHours_Shared_Office_Room(IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double))) #Hourly
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Shared_Office_Room))

        presenceToOccupantOfficeHours = self.MODELS['PresenceToOccupantOfficeHours']
        self.graph.add((presenceToOccupantOfficeHours, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], presenceToOccupantOfficeHours))

        occupantOfficeHours = self.MODELS['OccupantOfficeHours_Shared_Office_Room']
        self.graph.add((occupantOfficeHours, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((occupantOfficeHours, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((presenceToOccupantOfficeHours, self.PRIVVULN.creates, occupantOfficeHours))
        self.graph.add((occupantOfficeHours, self.PRIVVULNV2.privacyRiskScore, Literal("2", datatype=self.XSD.int)))

class PresenceToOccupantOfficeHours_Single_Office_Room(IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("3600", datatype=self.XSD.double))) #Hourly
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Single_Office_Room))

        presenceToOccupantOfficeHours = self.MODELS['PresenceToOccupantOfficeHours']
        self.graph.add((presenceToOccupantOfficeHours, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], presenceToOccupantOfficeHours))

        occupantOfficeHours = self.MODELS['OccupantOfficeHours_Single_Office_Room']
        self.graph.add((occupantOfficeHours, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((occupantOfficeHours, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((presenceToOccupantOfficeHours, self.PRIVVULN.creates, occupantOfficeHours))
        self.graph.add((occupantOfficeHours, self.PRIVVULNV2.privacyRiskScore, Literal("3", datatype=self.XSD.int)))

class PresenceToWorkDays_Single_Office_Room(IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("86400", datatype=self.XSD.double))) #Day
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Single_Office_Room))

        presenceToWorkDays = self.MODELS['PresenceToWorkDays']
        self.graph.add((presenceToWorkDays, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], presenceToWorkDays))

        workday = self.MODELS['Work_day_Single_Office_Room']
        self.graph.add((workday, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((workday, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((presenceToWorkDays, self.PRIVVULN.creates, workday))
        self.graph.add((workday, self.PRIVVULNV2.privacyRiskScore, Literal("3", datatype=self.XSD.int)))


class PresenceToWorkDays_Shared_Office_Room(IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("86400", datatype=self.XSD.double))) #Day
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Shared_Office_Room))

        presenceToWorkDays = self.MODELS['PresenceToWorkDays']
        self.graph.add((presenceToWorkDays, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], presenceToWorkDays))

        workday = self.MODELS['Work_day_Shared_Office_Room']
        self.graph.add((workday, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((workday, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((presenceToWorkDays, self.PRIVVULN.creates, workday))
        self.graph.add((workday, self.PRIVVULNV2.privacyRiskScore, Literal("2", datatype=self.XSD.int)))

class PresenceToWorkDays_Desk(IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Presence))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("86400", datatype=self.XSD.double))) #Day
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Desk))

        presenceToWorkDays = self.MODELS['PresenceToWorkDays']
        self.graph.add((presenceToWorkDays, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], presenceToWorkDays))

        workday = self.MODELS['Work_day_Desk']
        self.graph.add((workday, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((workday, self.PRIVVULNV2.description, Literal("This is bad!", datatype=self.XSD.string)))
        self.graph.add((presenceToWorkDays, self.PRIVVULN.creates, workday))
        self.graph.add((workday, self.PRIVVULNV2.privacyRiskScore, Literal("3", datatype=self.XSD.int)))

class PresenceToLunch(IPrivacyAttack):
    __DOMAINNAMESPACE__ = NSUtil.get_namespase_domain_smart_building()

    def __init__(self):
        self.MODELS =  Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        inputNode = self.MODELS['inputRequirement1']
        self.graph.add((inputNode, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((inputNode, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.CO2))
        self.graph.add((inputNode, self.PRIVVULNV2.TemporalResolution, Literal("60", datatype=self.XSD.double))) #Day
        self.graph.add((inputNode, self.PRIVVULNV2.spatialRequirement, self.__DOMAINNAMESPACE__.Office_Room))

        co2ToLunchLength = self.MODELS['PresenceToLunchLength']
        self.graph.add((co2ToLunchLength, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((inputNode, self.PRIVVULN['feeds'], co2ToLunchLength))

        lunchLength = self.MODELS['Lunch_Length']
        self.graph.add((lunchLength, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add((lunchLength, self.PRIVVULNV2.description, Literal("Lunch length", datatype=self.XSD.string)))
        self.graph.add((co2ToLunchLength, self.PRIVVULN.creates, lunchLength))
        self.graph.add((lunchLength, self.PRIVVULNV2.privacyRiskScore, Literal("1", datatype=self.XSD.int)))