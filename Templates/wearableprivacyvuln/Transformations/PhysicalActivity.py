from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal

# https://dl.acm.org/doi/pdf/10.1145/3309074.3309076

class PhysicalActivity(ITransformation):
    # noinspection SpellCheckingInspection
    __DOMAINNAMESPACE__ = Namespace("https://emikr15.student,sdu.dk/21/10/05/wearableprivacyvunl.ttl#")

    def __init__(self):
        self.MODELS = Namespace("https://ontology.hviidnet.com/2020/01/03/privacyvunl-model.ttl#")
        super().__init__(self.__DOMAINNAMESPACE__)

    def _build_model(self):
        input1 = self.MODELS['inputRequirement1']
        self.graph.add((input1, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((input1, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Accelerometer))

        pass
