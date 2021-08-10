import pdb
from sys import argv
from os import listdir
from os.path import exists
from os import mkdir
import json
import copy
from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugins.sparql
from Framework.Data.PrivacyRisk import PrivacyRisk
import Framework.namespace_util as NSUtil
from Framework.Input.InputData import Util as InputUtil

class Analysis:
    def __init__(self, domain_path=None, base_ontology_path=None, extention_ontology_path=None):
        self.domain_path = domain_path if domain_path is not None else "./Ontologies/smartbuildingprivacyvunl.ttl"
        self.base_ontology_path = base_ontology_path if base_ontology_path is not None else "./Ontologies/privacyvunl.ttl"
        self.extention_ontology_path = extention_ontology_path if extention_ontology_path is not None else "./Ontologies/privacyvunlv2.ttl"
        self.input_util =  InputUtil(self.domain_path, self.base_ontology_path, self.extention_ontology_path)
        self.PRIVVULN = NSUtil.get_namespase_base_ontology()
        self.PRIVVULNV2 = NSUtil.get_namespase_extrantion_ontology()
        self.RDF = NSUtil.get_namespase_rdf()
        self.total_score = 0


    def run_analysis(self, import_model):
        summary = []
        privacy_risks = self._find_risk_for_context(import_model)
        json_contexts = {}
        for privacy_risk in privacy_risks:
            if not privacy_risk in json_contexts: json_contexts[privacy_risk] = {'type': "context", "substream" : {}}
            for risk_for_context in privacy_risks[privacy_risk]:
                if not risk_for_context.input_data_context in json_contexts[privacy_risk]["substream"]: json_contexts[privacy_risk]["substream"][risk_for_context.input_data_context] = { 'type': "datastream", "substream" : []}
                entry = {
                    'privacy attack name': risk_for_context.privacy_attack_name,
                    'privacy risk name' : risk_for_context.privacy_risk_name,
                    'privacy risk template count': risk_for_context.template_count,
                    'privacy risk description': risk_for_context.description,
                    'type' : "privacy risk"
                }
                json_contexts[privacy_risk]["substream"][risk_for_context.input_data_context]["substream"].append(entry)
        with open("results.json", 'w') as fo:
            fo.writelines(json.dumps(json_contexts, sort_keys=True, indent=4, separators=(',', ': ')))
        return json_contexts
        # ro = model.query(query)
        # s = list(map(lambda row: list(map(lambda element: str(element), row)), ro))
        # result = [json.dumps(s, sort_keys=True, indent=4, separators=(',', ': '))+'\n']
        # with open(output_filename, 'w') as fo:
        #     fo.writelines(result)
        # entry = {
        #     'model': model_filename,
        #     'query': query_filename,
        #     'result': output_filename,
        # }
        # summary.append(entry)

        # with open('%s/summary.json' % result_dir, 'w') as fo:
        #     fo.writelines(json.dumps(summary, sort_keys=True, indent=4, separators=(',', ': ')))


    def _find_risk_for_context(self,input_model):
        input_model_temp = copy.deepcopy(input_model)
        input_model_temp.parse(self.domain_path)
        input_model_temp.parse(self.extention_ontology_path)

        input_model_temp.parse(self.base_ontology_path)

        q = rdflib.plugins.sparql.prepareQuery("""
                PREFIX rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX pv:     <https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#>
                PREFIX pv2:     <https://ontology.hviidnet.com/2020/01/03/privacyvunlV2.ttl#>
                PREFIX owl:   <http://www.w3.org/2002/07/owl#>

                SELECT ?context ?directDataInputName ?privacy_attack_name ?privacy_risk_name ?templateCount ?description ?privacyStrategy ?privacy_risk_subject
                WHERE {
                        ?privacy_risk_subject rdf:type pv:PrivacyRisk .
                        ?privacy_risk_subject pv2:name ?privacy_risk_name .

                        ?privacy_attack_subject pv:creates+ ?privacy_risk_subject .
                        ?privacy_attack_subject rdf:type pv:PrivacyAttack .
                        ?privacy_attack_subject pv2:name ?privacy_attack_name .

                        ?directDataInputName  pv:feeds* ?privacy_attack_subject .

                        ?context  rdf:type pv2:Context .
                        ?context  pv2:has+ ?directDataInputName .

                        # ?directDataInputName  pv:feeds* ?privacy_attack_subject .

                    #Find transformation count for privacy_risk if it is set
                    OPTIONAL {
                         ?privacy_risk_subject pv2:TemplateCount ?templateCount .
                    }.
                    OPTIONAL {
                         ?privacy_risk_subject pv2:description ?description .
                    }.
                     OPTIONAL {
                         ?privacy_risk_subject pv2:privacyStrategy ?privacyStrategy .
                    }.

                }
                """
            )
        ro = input_model_temp.query(q)

        supported_data_types = {}

        privacy_risk_subject = {}

        for row in ro:
            if not row[0] in supported_data_types : supported_data_types[row[0]] = []
            template_count =  0 if row[4] is None else  int(row[4])
            privacyStrategy =  None if row[6] is None else [row[6].value]
            privacyRisk = None
            if not row[7] in privacy_risk_subject:
                privacyRisk = PrivacyRisk(row[0], row[1], row[2], row[3], template_count, row[5].value, privacyStrategy)
                supported_data_types[row[0]].append(privacyRisk)
                privacy_risk_subject[row[7]] = privacyRisk
            elif privacyStrategy is not None:
                privacyRisk = privacy_risk_subject[row[7]]
                privacyRisk.privacyStrategies.append(privacyStrategy)
        return supported_data_types

    def find_privacy_scores(self, input_model, nameing_of_output = None):
        context_structures = self._find_context_roots(input_model)
        json_contexts = {}
        usered_risks = {}
        for context_structure in context_structures:
            privacy_risks_dict = {}
            privacy_score = 0
            temp_privacy_score, privacy_risks_list = self._add_contexts(input_model,context_structure, json_contexts, usered_risks)
            for privacy_risk in privacy_risks_list:
                privacy_risk_item = privacy_risks_list[privacy_risk]
                privacy_risk_name = privacy_risk_item['privacy_risks_name']
                if privacy_risk_name not in privacy_risks_dict:
                    privacy_risks_dict[privacy_risk_name] = privacy_risks_list[privacy_risk]
                    privacy_score = privacy_score + privacy_risks_list[privacy_risk]['privacy_score']
            json_object = {
                "type" : "Context",
                "privacy_score" : privacy_score,
                "privacy_risks" : [*privacy_risks_list.values()]
            }
            list(privacy_risks_list.values())
            json_contexts[context_structure] = json_object
        if nameing_of_output is not None:
            with open(nameing_of_output +".json", 'w') as fo:
                fo.writelines(json.dumps(json_contexts, sort_keys=True, indent=4, separators=(',', ': ')))
        return json_contexts

    def _add_contexts(self, input_model,context_subject,json_contexts, usered_risks):
        privacy_score = 0
        privacy_risks_dict = {}
        for entity in input_model.objects(subject= context_subject,predicate=self.PRIVVULN.star):
            temp_privacy_score, privacy_risks_list = self._add_contexts(input_model, entity,json_contexts, usered_risks)
            for privacy_risk in privacy_risks_list:
                privacy_risk_item = privacy_risks_list[privacy_risk]
                privacy_risk_name = privacy_risk_item['privacy_risks_name']
                if privacy_risk_name not in privacy_risks_dict:
                    privacy_risks_dict[privacy_risk_name] = privacy_risks_list[privacy_risk]
                    privacy_score = privacy_score + privacy_risks_list[privacy_risk]['privacy_score']
        for entity in input_model.objects(subject= context_subject,predicate=self.PRIVVULNV2.has):
            temp_privacy_score, privacy_risks_list = self._add_datastream(input_model, entity,json_contexts, usered_risks)
            for privacy_risk in privacy_risks_list:
                privacy_risk_item = privacy_risks_list[privacy_risk]
                privacy_risk_name = privacy_risk_item['privacy_risks_name']
                if privacy_risk_name not in privacy_risks_dict:
                    privacy_risks_dict[privacy_risk_name] = privacy_risks_list[privacy_risk]
                    privacy_score = privacy_score + privacy_risks_list[privacy_risk]['privacy_score']
        json_object = {
            "type" : "Context",
            "privacy_score" : privacy_score,
            "privacy_risks" : [*privacy_risks_dict.values()]
        }
        json_contexts[context_subject] = json_object
        return privacy_score, privacy_risks_dict

    def _add_datastream(self, input_model,data_subject,json_contexts, usered_risks):
        privacy_score = 0
        privacy_risks_dict = {}
        for entity in input_model.objects(subject= data_subject,predicate=self.PRIVVULN.feeds):
            if (entity, self.RDF.type, self.PRIVVULN.Transformation) in input_model:
                temp_privacy_score, privacy_risks_list = self._add_transformation(input_model, entity,json_contexts, usered_risks)
            elif (entity, self.RDF.type, self.PRIVVULN.PrivacyAttack) in input_model:
                temp_privacy_score, privacy_risks_list = self._add_privacy_attack(input_model, entity)
            else:
                continue
            # import pdb; pdb.set_trace()
            for privacy_risk in privacy_risks_list:
                privacy_risk_item = privacy_risks_list[privacy_risk]
                privacy_risk_name = privacy_risk_item['privacy_risks_name']
                if privacy_risk_name not in privacy_risks_dict:
                    privacy_risks_dict[privacy_risk_name] = privacy_risks_list[privacy_risk]
                    privacy_score = privacy_score + privacy_risks_list[privacy_risk]['privacy_score']
        json_object = {
            "type" : "Data Stream",
            "privacy_score" : privacy_score,
            "privacy_risks" : [*privacy_risks_dict.values()]
        }
        json_contexts[data_subject] = json_object
        return privacy_score, privacy_risks_dict

    def _add_transformation(self, input_model,data_subject, json_contexts, usered_risks):
        privacy_score = 0
        privacy_risks_dict = {}
        for entity in input_model.objects(data_subject,self.PRIVVULN.feeds):
            temp_privacy_score, risk_json_object = self._add_datastream(input_model, entity, json_contexts, usered_risks)
            for privacy_risk in risk_json_object:
                    if privacy_risk not in privacy_risks_dict:
                        privacy_risks_dict[privacy_risk] = risk_json_object[privacy_risk]
                        privacy_score = privacy_score + risk_json_object[privacy_risk]['privacy_score']
        for entity in input_model.objects(data_subject,self.PRIVVULNV2.creates):
            temp_privacy_score, risk_json_object = self._add_datastream(input_model, entity, json_contexts, usered_risks)
            for privacy_risk in risk_json_object:
                    if privacy_risk not in privacy_risks_dict:
                        privacy_risks_dict[privacy_risk] = risk_json_object[privacy_risk]
                        privacy_score = privacy_score + risk_json_object[privacy_risk]['privacy_score']
        return privacy_score, privacy_risks_dict

    def _add_privacy_attack(self, input_model,data_subject):
        privacy_score = 0
        privacy_risks_dict = {}
        for entry in input_model.objects(subject= data_subject,predicate=self.PRIVVULN.creates):
            if (entry, self.RDF.type, self.PRIVVULN.PrivacyRisk) in input_model:
                temp_privacy_score, risk_json_object = self._add_privacy_risk(input_model, entry)
                if risk_json_object is not None:
                    privacy_score = privacy_score + risk_json_object['privacy_score']
                    privacy_risks_dict[data_subject] = risk_json_object
        return privacy_score, privacy_risks_dict

    def _add_privacy_risk(self, input_model,data_subject):
        privacy_score = 0
        description = ""
        template_count = ""
        privacy_risks_name = ""
        privacy_strategies = []
        try:
            privacy_score = input_model.value(predicate = self.PRIVVULNV2.privacyRiskScore, subject=data_subject, any = False)
            description = input_model.value(predicate = self.PRIVVULNV2.description, subject=data_subject, any = False)
            template_count = input_model.value(predicate = self.PRIVVULNV2.TemplateCount, subject=data_subject, any = False)
            privacy_risks_name = input_model.value(predicate = self.PRIVVULNV2.name, subject=data_subject, any = False)
        except rdflib.exceptions.UniquenessError:
            return 0
        for privacyStrategy in input_model.objects(data_subject, self.PRIVVULNV2.privacyStrategy):
            # import pdb; pdb.set_trace()
            privacy_strategies.append(privacyStrategy)
        privacy_score = privacy_score.value
        json_object = {
            "privacy_risks_name" : privacy_risks_name,
            "privacy_risk_description" : description.value,
            "privacy_score" : privacy_score,
            "privacy_strategies" : privacy_strategies,
            "template_count" : template_count.value
        }
        self.total_score =  self.total_score + privacy_score
        return privacy_score, json_object

    def _find_context_roots(self,input_model):
        input_model_temp = copy.deepcopy(input_model)
        input_model_temp.parse(self.domain_path)
        input_model_temp.parse(self.extention_ontology_path)

        input_model_temp.parse(self.base_ontology_path)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT ?context
                WHERE {
                    ?context  rdf:type/rdfs:subClassOf* pv2:Context .
                    FILTER NOT EXISTS { ?subject pv2:star ?context}
                }
                """,
                initNs = NSUtil.get_binding_namespaces()
            )
        ro = input_model_temp.query(q)

        context_roots = []

        for row in ro:
            context_roots.append(row[0])
        return context_roots