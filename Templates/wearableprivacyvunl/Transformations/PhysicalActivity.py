from rdflib import Namespace, RDF, Literal

from Templates.ITemplate import ITransformation


# https://dl.acm.org/doi/pdf/10.1145/3309074.3309076


class PhysicalActivity(ITransformation):
    # noinspection SpellCheckingInspection
    __DOMAINNAMESPACE__ = Namespace(
        "https://emikr15.student.sdu.dk/21/10/05/wearableprivacyvunl.ttl#"
    )

    def __init__(self):
        self.MODELS = Namespace(
            "https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#"
        )
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        input_node = self.MODELS["inputRequirement"]
        triples = [
            (input_node, self.RDF.type, self.PRIVVULNV2.Constraint),
            (input_node, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Accelerometer)
        ]
        time_resolution = self.MODELS['timeResolutionLinear']
        triples += [
            (time_resolution, RDF.type, self.PRIVVULNV2.TimeResolutionLinear),
            (time_resolution, self.PRIVVULNV2.TimeInput, Literal(1.0, datatype=self.XSD.double)),
            (time_resolution, self.PRIVVULNV2.TimeOutput, Literal(1.0, datatype=self.XSD.double)),
            (input_node, self.PRIVVULN.feeds, time_resolution)
        ]

        accelerometer_to_physical_activity = self.MODELS["AccToPhysicalActivity"]
        triples += [
            (accelerometer_to_physical_activity, RDF.type, self.PRIVVULN.Transformation),
            (input_node, self.PRIVVULN["feeds"], accelerometer_to_physical_activity)
        ]

        physical_activity = self.MODELS["physicalActivity"]
        triples += [
            (physical_activity, RDF.type, self.PRIVVULN.TimeSeries),
            (physical_activity, RDF.type, self.__DOMAINNAMESPACE__.PhysicalActivity),
            (accelerometer_to_physical_activity, self.PRIVVULN.feeds, physical_activity)
        ]

        [self.graph.add(triple) for triple in triples]
