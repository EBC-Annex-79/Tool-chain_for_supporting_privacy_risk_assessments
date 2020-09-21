import pandas
from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugin
from rdflib.compare import to_isomorphic, graph_diff, to_canonical_graph
import json
from Framework.Data import Data
from Framework.Templates.transforamtion import Util as TransformationUtil
from Framework.Templates.privacyAttack import Util as PrivacyAttackUtil

"""
    combind_graphs.py
"""

class GraphCombind:
    def __init__(self, domain_url=None, base_ontology_url=None, extention_ontology_url=None):
        self.domain_url = domain_url if domain_url is not None else "./Ontologies/smartbuildingprivacyvunl.ttl"
        self.base_ontology_url = base_ontology_url if base_ontology_url is not None else "./Ontologies/privacyvunl.ttl"
        self.extention_ontology_url = extention_ontology_url if extention_ontology_url is not None else "./Ontologies/privacyvunlv2.ttl"
        self.transformationUtil = TransformationUtil(self.domain_url,self.base_ontology_url,self.extention_ontology_url)
        self.privacyAttackUtil = PrivacyAttackUtil(self.domain_url,self.base_ontology_url,self.extention_ontology_url)

    def combind_graphs(self,inputModel,template):
        templateUtil = None
        templateName = ""

        valied_transformation = self.transformationUtil.validate_template(template)
        valied_privacy_attack = self.privacyAttackUtil.validate_template(template)

        if valied_transformation is not None and valied_privacy_attack is not None:
            print("Template most have either a transforamtion or a privacy attack")
            return inputModel
        elif valied_transformation is not None and valied_privacy_attack is not None and valied_transformation ^ valied_privacy_attack:
            print("Template may only have a transformation or privacy attack")
            return inputModel

        if valied_transformation:
            templateUtil = self.transformationUtil
            templateName = templateUtil.get_template_name(template)
        elif valied_privacy_attack:
            templateUtil = self.privacyAttackUtil
            templateName = templateUtil.get_template_name(template)

        context_used_data_inputs =  templateUtil.can_template_be_used(inputModel, template, templateName)

        for context in context_used_data_inputs.keys():
            #use the template to extend the input model.
            inputModel = templateUtil.combind_using_template(inputModel,template, context_used_data_inputs[context])
        return inputModel

