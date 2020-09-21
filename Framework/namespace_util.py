from rdflib import Graph, Namespace, URIRef, Literal

def get_namespase_domain_smart_home():
    return Namespace('https://ontology.hviidnet.com/2020/01/03/smarthomesprivacyvunl.ttl#')

def get_namespase_domain_smart_building():
    return Namespace('https://ontology.hviidnet.com/2020/01/03/smartbuildingprivacyvunl.ttl#')

def get_namespase_domain_health():
    return Namespace('https://ontology.hviidnet.com/2020/01/03/healthprivacyvunl.ttl#')

def get_namespase_rdf():
    return Namespace(get_url_rdf())

def get_namespase_rdfs():
    return Namespace(get_url_rdfs())

def get_namespase_owl():
    return Namespace(get_url_owl())

def get_namespase_xsd():
    return Namespace(get_url_xsd())

def get_namespase_base_ontology():
    return Namespace(get_url_base_ontology())

def get_namespase_extrantion_ontology():
    return Namespace(get_url_extrantion_ontology())

def get_url_owl():
    return 'http://www.w3.org/2002/07/owl#'

def get_url_base_ontology():
    return 'https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#'

def get_url_extrantion_ontology():
    return 'https://ontology.hviidnet.com/2020/01/03/privacyvunlV2.ttl#'

def get_url_rdf():
    return 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

def get_url_rdfs():
    return 'http://www.w3.org/2000/01/rdf-schema#'

def get_url_xsd():
    return 'http://www.w3.org/2001/XMLSchema#'

def get_binding_namespaces():
    NS = {
        "pv" : get_url_base_ontology(),
        "pv2" : get_url_extrantion_ontology(),
        "rdf" : get_url_rdf(),
        "rdfs" : get_url_rdfs(),
        "owl" : get_url_owl()
    }
    return NS