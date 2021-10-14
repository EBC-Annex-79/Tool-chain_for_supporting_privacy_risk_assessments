from rdflib import Namespace
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
        physicalActivity = self.MODELS["inputRequirement1"]
        self.graph.add((physicalActivity, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add(
            (
                physicalActivity,
                self.PRIVVULN.feeds,
                self.__DOMAINNAMESPACE__.PhysicalActivity,
            )
        )

        sleepPattern = self.MODELS["inputRequirement2"]
        self.graph.add((sleepPattern, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add(
            (sleepPattern, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.SleepPattern)
        )

        transformation = self.MODELS["physicalActivitySleepPatternToHealthCondition"]
        self.graph.add((transformation, self.RDF.type, self.PRIVVULN.PrivacyAttack))
        self.graph.add((physicalActivity, self.PRIVVULN.feeds, transformation))
        self.graph.add((sleepPattern, self.PRIVVULN.feeds, transformation))

        health_condition = self.MODELS["HealthCondition"]
        self.graph.add((health_condition, self.RDF.type, self.PRIVVULN.PrivacyRisk))
        self.graph.add(
            (
                health_condition,
                self.PRIVVULNV2.description,
                Literal("This is bad!", datatype=self.XSD.string),
            )
        )
        self.graph.add((transformation, self.PRIVVULN.creates, health_condition))
        self.graph.add(
            (
                health_condition,
                self.PRIVVULNV2.privacyRiskScore,
                Literal("5", datatype=self.XSD.int),
            )
        )
