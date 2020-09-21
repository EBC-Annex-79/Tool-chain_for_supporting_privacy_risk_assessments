from sys import argv
from os import listdir
import json
from graphviz import Digraph
from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import copy
import Framework.namespace_util as NSUtil

class Visualize_full:
    def __init__(self, input_model, base_ontology_url, extention_ontology_url, domain_url   ):
        self.input_model = input_model
        self.PRIVVULN = NSUtil.get_namespase_base_ontology()
        self.PRIVVULNV2 = NSUtil.get_namespase_extrantion_ontology()
        self.RDF  = NSUtil.get_namespase_rdf()
        self.base_ontology_url =base_ontology_url
        self.extention_ontology_url = extention_ontology_url
        self.domain_url = domain_url

    def generated_visualization(self, nameing_of_output):
        # graph = Digraph(engine='dot')
        # graph = None
        graph = Digraph(engine='circo')
        graph.attr(size='6,6')

        edges = []
        names = {}

        # import pdb; pdb.set_trace()
        contexts = self.find_contexts(self.input_model)

        for subject in contexts:
            # import pdb; pdb.set_trace()
            self._add_context(graph,edges, names, subject)

        # export to dot
        with open('model_full.dot', 'w') as fo:
            fo.writelines([str(graph.source)])

        # export to pdf file
        if nameing_of_output is not None:
            graph.render(nameing_of_output, cleanup= True)
        else:
            graph.render('model_full', cleanup= True)

        return graph



    def _add_context (self,graph, edges, names, context_subject, parent=None):
        context_name = self._name(context_subject)
        if not context_subject in names:
            names[context_subject] = context_name
            graph.node(context_name, context_name, color='green', style='filled')

        if parent is not None and not (parent, context_name) in edges:
            edges.append((parent, context_name))
            graph.edge(parent, context_name, color='black')

        for sub_subject in self.input_model.objects(context_subject,self.PRIVVULN.star):
           sub_context_name = self._add_context(graph, edges, names, sub_subject, parent=context_name)
        for sub_subject in self.input_model.objects(context_subject,self.PRIVVULNV2.has):
           sub_context_name = self._add_datastream(graph, edges, names, sub_subject, context_name)
        return context_name

    def _add_datastream(self,graph, edges, names, entity, parent,label=None):
        datastream_base_subject = self._get_model_base_name(entity)

        datastream_name_label = self._name(datastream_base_subject)
        datastream_name = self._name(entity)

        if not entity in names:
            names[entity] = datastream_name
            graph.node(datastream_name, label=datastream_name_label, color='yellow', style='filled')
        if not (parent, datastream_name) in edges:
            edges.append((parent, datastream_name))
            graph.edge(parent, datastream_name, color='black', label=label)

        for sub_subject in self.input_model.objects(entity,self.PRIVVULN.star):
            sub_datastream = self._add_datastream(graph, edges, names, sub_subject, datastream_name)
        for sub_subject in self.input_model.objects(entity,self.PRIVVULN.feeds):

            # sub_subject_name =  self.input_model.objects(sub_subject,self.PRIVVULNV2.name)
            # import pdb; pdb.set_trace()
            if (sub_subject, self.RDF.type, self.PRIVVULN.Transformation) in self.input_model:
                sub_datastream = self._add_transformation(graph, edges, names, sub_subject, datastream_name)
            if (sub_subject, self.RDF.type, self.PRIVVULN.PrivacyAttack) in self.input_model:
                sub_datastream = self._add_privacy_attack(graph, edges, names, sub_subject, datastream_name)
        return datastream_name


    def _add_transformation(self,graph, edges, names, entity, parent):
        template_base_subject = self._get_model_base_name(entity)

        transformation_name_label = self._name(template_base_subject)
        transformation_name = self._name(entity)

        if not entity in names:
            names[entity] = transformation_name
            graph.node(transformation_name, label=transformation_name_label, color='blue', style='filled')
        if not (parent, transformation_name) in edges:
            edges.append((parent, transformation_name))
            graph.edge(parent, transformation_name, color='black')
        for sub_subject in self.input_model.objects(entity,self.PRIVVULN.feeds):
            sub_datastream = self._add_datastream(graph, edges, names, sub_subject, transformation_name)
        for sub_subject in self.input_model.objects(entity,self.PRIVVULNV2.creates):
            sub_datastream = self._add_datastream(graph, edges, names, sub_subject, transformation_name,label="creates")
        return transformation_name

    def _add_privacy_attack(self,graph, edges, names, entity, parent):

        privacy_attack_base_subject = self._get_model_base_name(entity)

        privacy_attack_name_label = self._name(privacy_attack_base_subject)
        privacy_attack_name = self._name(entity)

        if not entity in names:
            names[entity] = privacy_attack_name
            graph.node(privacy_attack_name, label=privacy_attack_name_label, color='purple', style='filled')
        if not (parent, privacy_attack_name) in edges:
            edges.append((parent, privacy_attack_name))
            graph.edge(parent, privacy_attack_name, color='black')
        for sub_subject in self.input_model.objects(entity,self.PRIVVULN.creates):
            sub_privacy_attack = self._add_privacy_risk(graph, edges, names, sub_subject, privacy_attack_name)
        return privacy_attack_name


    def _add_privacy_risk(self,graph, edges, names, entity, parent,label=None):
        privacy_risk_base_subject = self._get_model_base_name(entity)

        privacy_risk_name = self._name(privacy_risk_base_subject)
        if not privacy_risk_base_subject in names:
            names[privacy_risk_base_subject] = privacy_risk_name
            graph.node(privacy_risk_name, privacy_risk_name, color='red', style='filled')
        if not (parent, privacy_risk_name) in edges:
            edges.append((parent, privacy_risk_name))
            graph.edge(parent, privacy_risk_name, color='black', label=label)
        return privacy_risk_name

    def _get_model_base_name(self,entity):
        try:
            model_base_subject = self.input_model.value(predicate = self.PRIVVULNV2.name, subject=entity, any = False)
        except rdflib.exceptions.UniquenessError:
            return
        model_base_subject = model_base_subject if model_base_subject is not None else entity
        return model_base_subject

    def _name (self,entity):
        return entity.split('#')[-1]

    def find_contexts(self, inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)
        inputModel_temp.parse(self.base_ontology_url)

        ro = inputModel_temp.query(
            """
                SELECT DISTINCT ?sub_class_subject
                WHERE {
                    ?class_types rdfs:subClassOf* pv2:Context .
                    ?sub_class_subject rdf:type ?class_types .
                }
            """, initNs = NSUtil.get_binding_namespaces())

        contexts = []

        for row in ro:
            contexts.append(row[0])
        # import pdb; pdb.set_trace()
        return contexts


