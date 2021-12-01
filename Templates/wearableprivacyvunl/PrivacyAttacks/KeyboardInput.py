# https://ieeexplore-ieee-org.proxy1-bib.sdu.dk/document/7917140
from rdflib import Namespace, Literal, XSD, RDF

from Templates.ITemplate import IPrivacyAttack


class KeyboardInput(IPrivacyAttack):
    # noinspection SpellCheckingInspection
    __DOMAINNAMESPACE__: Namespace = Namespace(
        "https://emikr15.student.sdu.dk/21/10/05/wearableprivacyvunl.ttl#"
    )

    def __init__(self):
        self.MODELS = Namespace(
            "https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#"
        )
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self) -> None:
        accelerometer = self.MODELS["inputRequirementACC"]
        triples = [
            (accelerometer, self.RDF.type, self.PRIVVULNV2.Constraint),
            (accelerometer, self.PRIVVULNV2.TemporalResolution, Literal("0.02", datatype=self.XSD.double)),
            (accelerometer, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Accelerometer)
        ]

        transformation = self.MODELS["accToKeyboardInput"]
        triples += [
            (transformation, RDF.type, self.PRIVVULN.PrivacyAttack),
            (accelerometer, self.PRIVVULN.feeds, transformation),
        ]

        keyboard_input = self.MODELS["KeyboardInput"]
        triples += [
            (keyboard_input, RDF.type, self.PRIVVULN.PrivacyRisk),
            (keyboard_input, self.PRIVVULNV2.description, Literal("This is bad!", datatype=XSD.string)),
            (transformation, self.PRIVVULN.creates, keyboard_input),
            # TODO fix score
            (keyboard_input, self.PRIVVULNV2.privacyRiskScore, Literal(5, datatype=XSD.int))
        ]

        [self.graph.add(triple) for triple in triples]
