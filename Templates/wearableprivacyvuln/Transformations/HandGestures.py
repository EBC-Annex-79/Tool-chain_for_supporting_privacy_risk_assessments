from rdflib import Literal
from rdflib.namespace import RDF, Namespace

from ITemplate import ITransformation


# https://arxiv.org/pdf/2106.11900.pdf
class HandGestures(ITransformation):
    __DOMAINNAMESPACE__ = Namespace(
        "https://emikr15.student,sdu.dk/21/10/05/wearableprivacyvunl.ttl#"
    )

    def __init__(self):
        self.MODELS = Namespace(
            "https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#"
        )
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        acc = self.MODELS["inputRequirementACC"]
        triples = [
            (acc, RDF.type, self.PRIVVULNV2.Constraint),
            (acc, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Accelerometer),
        ]

        time_resolution = self.MODELS['timeResolutionLinear']
        triples += [
            (time_resolution, RDF.type, self.PRIVVULNV2.TimeResolutionLinear),
            (time_resolution, self.PRIVVULNV2.TimeInput, Literal(0.03125, datatype=self.XSD.double)),
            (time_resolution, self.PRIVVULNV2.TimeOutput, Literal(0.03125, datatype=self.XSD.double)),
            (acc, self.PRIVVULN.feeds, time_resolution)
        ]

        acc_to_hand_gestures = self.MODELS["AccToHandGestures"]
        triples += [
            (acc_to_hand_gestures, RDF.type, self.PRIVVULN.Transformation),
            (acc, self.PRIVVULN["feeds"], acc_to_hand_gestures),
        ]

        hand_gestures = self.MODELS["HandGestures"]
        triples += [
            (hand_gestures, RDF.type, self.PRIVVULN.TimeSeries),
            (hand_gestures, RDF.type, self.__DOMAINNAMESPACE__.HandGestures),
            (acc_to_hand_gestures, self.PRIVVULN.feeds, hand_gestures),
        ]

        [self.graph.add(triple) for triple in triples]
