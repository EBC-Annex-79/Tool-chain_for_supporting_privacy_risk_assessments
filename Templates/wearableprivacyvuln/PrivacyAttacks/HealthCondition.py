from rdflib import Namespace, RDF, XSD
from rdflib.term import Literal

from ITemplate import IPrivacyAttack


# https://dl.acm.org/doi/pdf/10.1145/3309074.3309076
class HealthCondition(IPrivacyAttack):
    # noinspection SpellCheckingInspection
    __DOMAINNAMESPACE__: Namespace = Namespace(
        "https://emikr15.student,sdu.dk/21/10/05/wearableprivacyvunl.ttl#"
    )

    def __init__(self):
        self.MODELS = Namespace(
            "https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#"
        )
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self) -> None:
        physical_activity = self.MODELS["inputRequirement1"]
        triples = [
            (physical_activity, self.RDF.type, self.PRIVVULNV2.Constraint),
            (physical_activity, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.PhysicalActivity)
        ]

        sleep_pattern = self.MODELS["inputRequirement2"]
        triples += [
            (sleep_pattern, RDF.type, self.PRIVVULNV2.Constraint),
            (sleep_pattern, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.SleepPattern)
        ]

        transformation = self.MODELS["physicalActivitySleepPatternToHealthCondition"]
        triples += [
            (transformation, RDF.type, self.PRIVVULN.PrivacyAttack),
            (physical_activity, self.PRIVVULN.feeds, transformation),
            (sleep_pattern, self.PRIVVULN.feeds, transformation)
        ]

        health_condition = self.MODELS["HealthCondition"]
        triples += [
            (health_condition, RDF.type, self.PRIVVULN.PrivacyRisk),
            (health_condition, self.PRIVVULNV2.description, Literal("This is bad!", datatype=XSD.string)),
            (transformation, self.PRIVVULN.creates, health_condition),
            # TODO fix score
            (health_condition, self.PRIVVULNV2.privacyRiskScore, Literal(5, datatype=XSD.int))
        ]

        [self.graph.add(triple) for triple in triples]
