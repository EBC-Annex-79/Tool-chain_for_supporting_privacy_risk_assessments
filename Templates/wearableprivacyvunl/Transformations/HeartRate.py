from rdflib import Namespace, Literal, RDF

from Templates.ITemplate import ITransformation


# https://arxiv.org/abs/2106.11900
class HeartRate(ITransformation):
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
        input_node_ecg = self.MODELS["inputRequirementECG"]
        triples = [
            (input_node_ecg, self.RDF.type, self.PRIVVULNV2.Constraint),
            (input_node_ecg, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Electrocardiography)
        ]
        time_resolution_ecg = self.MODELS['timeResolutionLinearECG']
        triples += [
            (time_resolution_ecg, RDF.type, self.PRIVVULNV2.TimeResolutionLinear),
            (time_resolution_ecg, self.PRIVVULNV2.TimeInput, Literal(1.0, datatype=self.XSD.double)),
            (time_resolution_ecg, self.PRIVVULNV2.TimeOutput, Literal(1.0, datatype=self.XSD.double)),
            (input_node_ecg, self.PRIVVULN.feeds, time_resolution_ecg)
        ]

        # input_node_ppg = self.MODELS["inputRequirementPPG"]
        # triples = [
        #     (input_node_ppg, self.RDF.type, self.PRIVVULNV2.Constraint),
        #     (input_node_ppg, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Photoplethysmography)
        # ]
        # time_resolution_ppg = self.MODELS['timeResolutionLinearPPG']
        # triples += [
        #     (time_resolution_ppg, RDF.type, self.PRIVVULNV2.TimeResolutionLinear),
        #     (time_resolution_ppg, self.PRIVVULNV2.TimeInput, Literal(1.0, datatype=self.XSD.double)),
        #     (time_resolution_ppg, self.PRIVVULNV2.TimeOutput, Literal(1.0, datatype=self.XSD.double)),
        #     (input_node_ppg, self.PRIVVULN.feeds, time_resolution_ppg)
        # ]

        ecg_to_hr = self.MODELS["ecgToHeartRate"]
        triples += [
            (ecg_to_hr, RDF.type, self.PRIVVULN.Transformation),
            (input_node_ecg, self.PRIVVULN["feeds"], ecg_to_hr)
        ]

        # ppg_to_hr = self.MODELS["ppgToHeartRate"]
        # triples += [
        #     (ppg_to_hr, RDF.type, self.PRIVVULN.Transformation),
        #     (input_node_ecg, self.PRIVVULN["feeds"], ppg_to_hr)
        # ]

        physical_activity = self.MODELS["InterbeatInterval"]
        triples += [
            (physical_activity, RDF.type, self.PRIVVULN.TimeSeries),
            (physical_activity, RDF.type, self.__DOMAINNAMESPACE__.InterbeatInterval),
            # (ppg_to_hr, self.PRIVVULN.feeds, physical_activity),
            (ecg_to_hr, self.PRIVVULN.feeds, physical_activity)

        ]

        [self.graph.add(triple) for triple in triples]
