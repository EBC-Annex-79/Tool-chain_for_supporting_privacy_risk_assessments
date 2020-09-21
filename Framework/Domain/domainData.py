from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugin
import Framework.namespace_util as NSUtil

class DomainData:
    def __init__(self, domain_url, base_ontology_url, extention_ontology_url):
        self.domain_url = domain_url
        self.base_ontology_url =base_ontology_url
        self.extention_ontology_url = extention_ontology_url

    def find_context_structure(self):
        model = Graph()
        model.parse(self.domain_url)
        model.parse(self.extention_ontology_url)

        ro = model.query(
            """
                SELECT distinct ?root ?sub_class
                WHERE {
                    ?root a owl:Class .
                    ?root rdfs:subClassOf*  pv2:Context.
                    ?sub_class  rdfs:subClassOf ?root .
                }
            """,
                initNs = NSUtil.get_binding_namespaces()
                )

        contexts = {}

        for row in ro:
            contexts[row[1]] = row[0]
        return contexts


