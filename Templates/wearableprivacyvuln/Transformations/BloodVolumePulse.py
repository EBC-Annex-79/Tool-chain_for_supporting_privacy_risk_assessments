from rdflib import Namespace, Literal, RDF

from Templates.ITemplate import ITransformation


# https://arxiv.org/abs/2106.11900
class BloodVolumePulse(ITransformation):
    __DOMAINNAMESPACE__ = Namespace(
        "https://emikr15.student,sdu.dk/21/10/05/wearableprivacyvunl.ttl#"
    )

    def __init__(self):
        self.MODELS = Namespace(
            "https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#"
        )
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        input_node_ppg = self.MODELS["inputRequirementPPG"]
        triples = [
            (input_node_ppg, self.RDF.type, self.PRIVVULNV2.Constraint),
            (input_node_ppg, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Photoplethysmography)
        ]

        # TODO: fix time
        time_resolution_ppg = self.MODELS['timeResolutionLinearPPG']
        triples += [
            (time_resolution_ppg, RDF.type, self.PRIVVULNV2.TimeResolutionLinear),
            (time_resolution_ppg, self.PRIVVULNV2.TimeInput, Literal(1.0, datatype=self.XSD.double)),
            (time_resolution_ppg, self.PRIVVULNV2.TimeOutput, Literal(1.0, datatype=self.XSD.double)),
            (input_node_ppg, self.PRIVVULN.feeds, time_resolution_ppg)
        ]

        ppg_to_bvp = self.MODELS["PcgToBvp"]
        triples += [
            (ppg_to_bvp, RDF.type, self.PRIVVULN.Transformation),
            (input_node_ppg, self.PRIVVULN["feeds"], ppg_to_bvp)
        ]

        blood_volume_pulse = self.MODELS["BloodVolumePulse"]
        triples += [
            (blood_volume_pulse, RDF.type, self.PRIVVULN.TimeSeries),
            (blood_volume_pulse, RDF.type, self.__DOMAINNAMESPACE__.BloodVolumePulse),
            (ppg_to_bvp, self.PRIVVULN.feeds, blood_volume_pulse)
        ]

        [self.graph.add(triple) for triple in triples]
