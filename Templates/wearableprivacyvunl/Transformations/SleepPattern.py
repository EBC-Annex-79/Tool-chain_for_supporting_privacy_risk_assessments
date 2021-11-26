from rdflib import Literal
from rdflib.namespace import RDF, Namespace


# https://dl.acm.org/doi/pdf/10.1145/3309074.3309076
from Templates.ITemplate import ITransformation


class SleepPattern(ITransformation):
    __DOMAINNAMESPACE__ = Namespace(
        "https://emikr15.student.sdu.dk/21/10/05/wearableprivacyvunl.ttl#"
    )

    def __init__(self):
        self.MODELS = Namespace(
            "https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#"
        )
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        input_node = self.MODELS["inputRequirement1"]
        triples = [
            (input_node, RDF.type, self.PRIVVULNV2.Constraint),
            (input_node, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Accelerometer),
        ]

        time_resolution = self.MODELS['timeResolutionLinear']
        triples += [
            (time_resolution, RDF.type, self.PRIVVULNV2.TimeResolutionLinear),
            (time_resolution, self.PRIVVULNV2.TimeInput, Literal(1.0, datatype=self.XSD.double)),
            (time_resolution, self.PRIVVULNV2.TimeOutput, Literal(1.0, datatype=self.XSD.double)),
            (input_node, self.PRIVVULN.feeds, time_resolution)
        ]

        accelerometer_to_sleep_pattern = self.MODELS["accelerometerToSleepPattern"]
        triples += [
            (accelerometer_to_sleep_pattern, RDF.type, self.PRIVVULN.Transformation),
            (input_node, self.PRIVVULN["feeds"], accelerometer_to_sleep_pattern),
        ]

        sleep_pattern = self.MODELS["sleepPattern"]
        triples += [
            (sleep_pattern, RDF.type, self.PRIVVULN.TimeSeries),
            (sleep_pattern, RDF.type, self.__DOMAINNAMESPACE__.PhysicalActivity),
            (accelerometer_to_sleep_pattern, self.PRIVVULN.feeds, sleep_pattern),
        ]

        [self.graph.add(triple) for triple in triples]
