from rdflib import Namespace, RDF, Literal, XSD



# https://arxiv.org/abs/2106.11900
from Templates.ITemplate import IPrivacyAttack


class PersonReIdentificationHR(IPrivacyAttack):
    # noinspection SpellCheckingInspection
    __DOMAINNAMESPACE__: Namespace = Namespace(
        "https://emikr15.student.sdu.dk/21/10/05/wearableprivacyvunl.ttl#"
    )

    def __init__(self):
        self.MODELS = Namespace(
            "https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#"
        )
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        heart_rate = self.MODELS["inputRequirementHR"]
        triples = [
            (heart_rate, self.RDF.type, self.PRIVVULNV2.Constraint),
            (heart_rate, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.HeartRate)
        ]

        hand_gestures = self.MODELS["inputRequirementHandGestures"]
        triples += [
            (hand_gestures, RDF.type, self.PRIVVULNV2.Constraint),
            (hand_gestures, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.HandGestures)
        ]

        transformation = self.MODELS["physicalActivitySleepPatternToHealthCondition"]
        triples += [
            (transformation, RDF.type, self.PRIVVULN.PrivacyAttack),
            (heart_rate, self.PRIVVULN.feeds, transformation),
            (hand_gestures, self.PRIVVULN.feeds, transformation)
        ]

        health_condition = self.MODELS["PersonReIdentification"]
        triples += [
            (health_condition, RDF.type, self.PRIVVULN.PrivacyRisk),
            (health_condition, self.PRIVVULNV2.description, Literal("This is bad!", datatype=XSD.string)),
            (transformation, self.PRIVVULN.creates, health_condition),
            # TODO fix score
            (health_condition, self.PRIVVULNV2.privacyRiskScore, Literal(5, datatype=XSD.int))
        ]

        [self.graph.add(triple) for triple in triples]
