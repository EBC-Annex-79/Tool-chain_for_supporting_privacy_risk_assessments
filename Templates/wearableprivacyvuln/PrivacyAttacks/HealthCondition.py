from rdflib import Namespace

from ITemplate import IPrivacyAttack


# https://dl.acm.org/doi/pdf/10.1145/3309074.3309076

class HealthCondition(IPrivacyAttack):
    # noinspection SpellCheckingInspection
    __DOMAINNAMESPACE__: Namespace = Namespace("https://emikr15.student,sdu.dk/21/10/05/wearableprivacyvunl.ttl#")

    def __init__(self):
        self.MODELS = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#')
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self) -> None:
        input1 = self.MODELS['inputRequirement1']
        self.graph.add((input1, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((input1, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.PhysicalActivity))

        input2 = self.MODELS['inputRequirement2']
        self.graph.add((input2, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((input2, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.SleepPattern))

        health_condition = self.MODELS['HealthCondition']
        self.graph.add((health_condition, self.RDF.type, self.PRIVVULN.PrivacyRisk))
