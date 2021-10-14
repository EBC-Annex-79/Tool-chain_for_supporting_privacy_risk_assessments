from rdflib import graph
from rdflib.namespace import RDF, Namespace
from ITemplate import ITransformation


# https://dl.acm.org/doi/pdf/10.1145/3309074.3309076


class SleepPattern(ITransformation):

    __DOMAINNAMESPACE__ = Namespace(
        "https://emikr15.student,sdu.dk/21/10/05/wearableprivacyvunl.ttl#"
    )

    def __init__(self):
        self.MODELS = Namespace(
            "https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#"
        )
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        input1 = self.MODELS["inputRequirement1"]
        triples = [
            (input1, RDF.type, self.PRIVVULNV2.Constraint),
            (input1, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Accelerometer),
        ]

        accelerometerToSleepPattern = self.MODELS["accelerometerToSleepPattern"]
        triples += [
            (accelerometerToSleepPattern, RDF.type, self.PRIVVULN.Transformation),
            (input1, self.PRIVVULN["feeds"], accelerometerToSleepPattern),
        ]

        sleepPattern = self.MODELS["sleepPattern"]
        triples += [
            (sleepPattern, RDF.type, self.PRIVVULN.TimeSeries),
            (sleepPattern, RDF.type, self.__DOMAINNAMESPACE__.PhysicalActivity),
            (accelerometerToSleepPattern, self.PRIVVULN.feeds, sleepPattern),
        ]
        [self.graph.add(triple) for triple in triples]
