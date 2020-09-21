from rdflib import Graph, Namespace, URIRef, Literal
import rdflib
from rdflib.compare import to_isomorphic, graph_diff, to_canonical_graph
import Framework.namespace_util as util

class ITemplate:
    def __init__(self, DOMAINNAMESPACE):
        self.RDF  = util.get_namespase_rdf()
        self.RDFS = util.get_namespase_rdfs()
        self.OWL  =util.get_namespase_owl()
        self.XSD  = util.get_namespase_xsd()
        self.PRIVVULN =  util.get_namespase_base_ontology()
        self.PRIVVULNV2 = util.get_namespase_extrantion_ontology()
        self.DOMAINNAMESPACE = DOMAINNAMESPACE
        self.graph = Graph()

    def _bind_namespaces(self):
        self.graph.bind('rdf' , self.RDF)
        self.graph.bind('rdfs', self.RDFS)
        self.graph.bind('owl' , self.OWL)
        self.graph.bind('xsd' , self.XSD)
        self.graph.bind('privvuln',self.PRIVVULN)
        self.graph.bind('privvulnv2',self.PRIVVULNV2)
        self.graph.bind('domain',self.DOMAINNAMESPACE)

    def get_model(self):
        self._bind_namespaces()
        self._build_model()
        return self.graph

    def _build_model(self):
        raise NotImplementedError

class ITransformation(ITemplate):
    def __init__(self, DOMAINNAMESPACE):
        super().__init__(DOMAINNAMESPACE)

class IPrivacyAttack(ITemplate):
    def __init__(self, DOMAINNAMESPACE):
        super().__init__(DOMAINNAMESPACE)