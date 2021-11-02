from rdflib import Namespace, Literal, RDF

from Templates.ITemplate import ITransformation


# https://arxiv.org/abs/2106.11900
class InterbeatInterval(ITransformation):
    # noinspection SpellCheckingInspection
    __DOMAINNAMESPACE__ = Namespace(
        "https://emikr15.student,sdu.dk/21/10/05/wearableprivacyvunl.ttl#"
    )

    def __init__(self):
        self.MODELS = Namespace(
            "https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#"
        )
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        ecg = self.MODELS["inputRequirementECG"]
        triples = [
            (ecg, self.RDF.type, self.PRIVVULNV2.Constraint),
            (ecg, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Electrocardiography)
        ]

        # TODO: fix time
        time_resolution = self.MODELS['timeResolutionLinear']
        triples += [
            (time_resolution, RDF.type, self.PRIVVULNV2.TimeResolutionLinear),
            (time_resolution, self.PRIVVULNV2.TimeInput, Literal(1.0, datatype=self.XSD.double)),
            (time_resolution, self.PRIVVULNV2.TimeOutput, Literal(1.0, datatype=self.XSD.double)),
            (ecg, self.PRIVVULN.feeds, time_resolution)
        ]

        ecg_to_ibi = self.MODELS["EcgToIbi"]
        triples += [
            (ecg_to_ibi, RDF.type, self.PRIVVULN.Transformation),
            (ecg, self.PRIVVULN["feeds"], ecg_to_ibi)
        ]

        physical_activity = self.MODELS["interbeatInterval"]
        triples += [
            (physical_activity, RDF.type, self.PRIVVULN.TimeSeries),
            (physical_activity, RDF.type, self.__DOMAINNAMESPACE__.InterbeatInterval),
            (ecg, self.PRIVVULN.feeds, physical_activity)
        ]

        [self.graph.add(triple) for triple in triples]
