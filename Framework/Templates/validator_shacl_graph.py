from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugin
import Framework.namespace_util as NSUtil
from pyshacl import validate

class Validator:
    def __init__(self, domain_path,base_ontology_path, extention_ontology_path):
        self.RDF  = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        self.PRIVVULN = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#')
        self.PRIVVULNV2 = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunlV2.ttl#')
        self.domain_path = domain_path
        self.base_ontology_path = base_ontology_path
        self.extention_ontology_path = extention_ontology_path
        self.domain_supported_data_types = None
        self.domain_supported_contexts = None

    def validate(self,template,class_name):
        pass



class Transforamtion_validator(Validator):
    def __init__(self,  domain_path,base_ontology_path, extention_ontology_path):
        super().__init__(domain_path,base_ontology_path, extention_ontology_path)

    def validate(self, template, class_name):
        print("validate")

        ontology =  Graph()
        ontology.parse(self.domain_path)
        ontology.parse(self.extention_ontology_path)
        ontology.parse(self.base_ontology_path)

        results = validate(template, shacl_graph=None, ont_graph=ontology, inference='rdfs', abort_on_error=False, serialize_report_graph=True, meta_shacl=False, debug=False)
        conforms, results_graph, results_text = results
        print(conforms)
        print(results_graph)
        print(results_text)
        import pdb; pdb.set_trace()
        validate_results = True
        ontology.serialize()
        return validate_results

class Privacy_attack_validator(Validator):
    def __init__(self,domain_path,base_ontology_path, extention_ontology_path):
        super().__init__(domain_path,base_ontology_path, extention_ontology_path)

    def validate(self, template, class_name):
        r = validate(data_graph, shacl_graph=sg, ont_graph=og, inference='rdfs', abort_on_error=False, meta_shacl=False, debug=False)
        validate_results = True
        return validate_results