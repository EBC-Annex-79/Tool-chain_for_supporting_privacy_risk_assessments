from rdflib import Namespace, RDF, XSD
from rdflib.term import Literal



# https://ieeexplore-ieee-org.proxy1-bib.sdu.dk/document/7514649
from Templates.ITemplate import IPrivacyAttack


class Gender(IPrivacyAttack):
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
            (accelerometer, self.PRIVVULNV2.TemporalResolution, Literal("0.01", datatype=self.XSD.double)),
            (accelerometer, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.PhysicalActivity)
        ]

        transformation = self.MODELS["accelerometerToGender"]
        triples += [
            (transformation, RDF.type, self.PRIVVULN.PrivacyAttack),
            (accelerometer, self.PRIVVULN.feeds, transformation),
        ]

        gender = self.MODELS["Gender"]
        triples += [
            (gender, RDF.type, self.PRIVVULN.PrivacyRisk),
            (gender, self.PRIVVULNV2.description, Literal("This is bad!", datatype=XSD.string)),
            (transformation, self.PRIVVULN.creates, gender),
            # TODO fix score
            (gender, self.PRIVVULNV2.privacyRiskScore, Literal(5, datatype=XSD.int))
        ]

        [self.graph.add(triple) for triple in triples]
