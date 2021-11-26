# https://ieeexplore-ieee-org.proxy1-bib.sdu.dk/stamp/stamp.jsp?tp=&arnumber=5325784

from rdflib import Namespace, RDF, Literal, XSD

from ITemplate import IPrivacyAttack


class Stress(IPrivacyAttack):
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
        eda = self.MODELS["inputRequirementEDA"]
        triples = [
            (eda, self.RDF.type, self.PRIVVULNV2.Constraint),
            (eda, self.PRIVVULNV2.TemporalResolution, Literal("0.0625", datatype=self.XSD.double)),
            (eda, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.ElectrodermalActivity)
        ]

        transformation = self.MODELS["edaToStress"]
        triples += [
            (transformation, RDF.type, self.PRIVVULN.PrivacyAttack),
            (eda, self.PRIVVULN.feeds, transformation),
        ]

        health_condition = self.MODELS["Stress"]
        triples += [
            (health_condition, RDF.type, self.PRIVVULN.PrivacyRisk),
            (health_condition, self.PRIVVULNV2.description, Literal("This is bad!", datatype=XSD.string)),
            (transformation, self.PRIVVULN.creates, health_condition),
            # TODO fix score
            (health_condition, self.PRIVVULNV2.privacyRiskScore, Literal(8, datatype=XSD.int))
        ]

        [self.graph.add(triple) for triple in triples]
