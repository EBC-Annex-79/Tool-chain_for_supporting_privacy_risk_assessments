from logging import debug
from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugins
import copy
from Framework.Data.Data import Data
from Framework.Data.ContextInput import ContextInput
import time
import Framework.namespace_util as NSUtil

class Util:
    def __init__(self, domain_path, base_ontology_path, extention_ontology_path, max_transformation_count=6):
        self.domain_url = domain_path
        self.base_ontology_url =base_ontology_path
        self.extention_ontology_url = extention_ontology_path
        self.max_transformation_count = rdflib.Literal(max_transformation_count)

    def find_all_input_data(self,inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)

        inputModel_temp.parse(self.base_ontology_url)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT ?context ?inputName ?individualData ?resolution ?templateCount
                WHERE {
                    ?individualData rdf:type owl:NamedIndividual .
                    ?inputName rdf:type ?individualData .

                    ?dataTypes rdfs:subClassOf* pv:Data .
                    ?inputName rdf:type ?dataTypes .

                    #Finds datatypes supported by domain
                    ?directDataInputName  pv:feeds* ?inputName .

                    # ?context  pv:star* ?sub_context .
                    ?context  rdf:type pv2:Context .
                    ?sub_context  pv2:has* ?directDataInputName .

                    #Find transformation count for datainput if it is set
                    OPTIONAL {
                         ?inputName pv2:TemplateCount ?templateCount .
                    }.
                    OPTIONAL {
                        ?inputName pv2:TemporalResolution ?resolution .
                    }
                    FILTER ( !bound(?templateCount) || ?templateCount < ?max_count  )
                }
                """,
                initNs = NSUtil.get_binding_namespaces()
                # ,
                # initNs = {}
            )

        ro = inputModel_temp.query(q, initBindings={'?max_count': self.max_transformation_count})

        supported_data_types = {}

        for row in ro:
            if not row[0] in supported_data_types : supported_data_types[row[0]] = []
            template_count =  0 if row[4] is None else  int(row[4])
            supported_data_types[row[0]].append(Data(row[2], float(), subject_name=row[1], template_count= template_count))
        return supported_data_types

    def find_all_input_data_old(self,inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)

        inputModel_temp.parse(self.base_ontology_url)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT DISTINCT ?context ?inputName ?individualData ?resolution ?templateCount ?context_type
                WHERE {
                    ?individualData rdf:type owl:NamedIndividual .
                    ?inputName rdf:type ?individualData .

                    ?dataTypes rdfs:subClassOf pv:Data .
                    ?inputName rdf:type ?dataTypes .

                    ?context  rdf:type/rdfs:subClassOf* pv2:Context .
                    ?context  pv2:has* ?directDataInputName .
                    ?context  rdf:type ?context_type .

                    #Finds datatypes supported by domain
                    ?directDataInputName  pv:feeds* ?inputName .

                    #Find transformation count for datainput if it is set
                    OPTIONAL {
                         ?inputName pv2:TemplateCount ?templateCount .
                    }.
                    OPTIONAL {
                        ?inputName pv2:TemporalResolution ?resolution .
                    }
                    FILTER ( !bound(?templateCount) || ?templateCount < ?max_count  )
                }
                """,
                initNs = NSUtil.get_binding_namespaces()
                # ,
                # initNs = {}
            )
        ro = inputModel_temp.query(q, initBindings={'?max_count': self.max_transformation_count})

        supported_data_types = {}

        for row in ro:
            if not row[0] in supported_data_types : supported_data_types[row[0]] = []
            template_count =  0 if row[4] is None else  int(row[4])
            resolution =  None if row[3] is None else  float(row[3])
            supported_data_types[row[0]].append(Data(row[2], resolution, subject_name=row[1], template_count= template_count, context= row[5], context_subject=row[0]))
        return supported_data_types


    def find_all_data_types_for_domain_data(self,inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)

        inputModel_temp.parse(self.base_ontology_url)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT DISTINCT ?individualData ?inputName ?individualData_subData
                WHERE {
                    ?individualData rdf:type owl:NamedIndividual .
                    ?inputName rdf:type ?individualData .

                    ?dataTypes rdfs:subClassOf pv:Data .
                    ?inputName rdf:type ?dataTypes .

                    ?individualData_subData rdf:type owl:NamedIndividual .
                    ?inputName_subData rdf:type ?individualData_subData .

                    ?dataTypes_subData rdfs:subClassOf pv:Data .
                    ?inputName_subData rdf:type ?dataTypes_subData .

                    ?inputName pv:feeds* ?feedsRelations .
                    ?feedsRelations rdf:type ?individualData_subData .
                }
                """
                , initNs = NSUtil.get_binding_namespaces()
            )
        # ns = dict(pv=Namespace("<https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#>"))

        ro = inputModel_temp.query(q)

        domain_data_found_using_data = {}

        for row in ro:
            if not row[1] in domain_data_found_using_data : domain_data_found_using_data[row[1]] = []
            domain_data_found_using_data[row[1]].append(row[2])
        return domain_data_found_using_data

    def find_all_data_creates_from_data_types(self,inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)

        inputModel_temp.parse(self.base_ontology_url)

        q = rdflib.plugins.sparql.prepareQuery("""
                    SELECT DISTINCT ?transformation ?datainput  ?outputType
                    WHERE {
                        ?transformation pv2:creates ?output .
                        ?output rdf:type ?outputType .

                        ?datainput pv:feeds ?transformation .
                        # ?datainput rdf:type ?datainput_type .

                        # ?datainput_type rdf:type/rdfs:subClassOf pv:Data .
                        ?outputType rdf:type/rdfs:subClassOf pv:Data .
                    }
                """
                , initNs = NSUtil.get_binding_namespaces()
            )
        # ns = dict(pv=Namespace("<https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#>"))

        ro = inputModel_temp.query(q)

        domain_data_found_using_data = {}

        for row in ro:
            if not row[1] in domain_data_found_using_data : domain_data_found_using_data[row[1]] = []
            domain_data_found_using_data[row[1]].append(row[2])
        return domain_data_found_using_data

    def find_all_domain_types_from_input_data(self,inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)

        inputModel_temp.parse(self.base_ontology_url)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT DISTINCT  ?inputName ?individualData ?inputName_subData ?individualData_subData ?templateCount ?resolution ?context ?contextType
                WHERE {
                    ?individualData rdf:type owl:NamedIndividual .
                    ?inputName rdf:type ?individualData .

                    ?inputName rdf:type/rdfs:subClassOf pv:Data .
                    # ?inputName rdf:type ?dataTypes .

                    # ?individualData_subData rdf:type owl:NamedIndividual .

                    ?dataTypes_subData rdfs:subClassOf pv:Data .
                    ?inputName_subData rdf:type ?dataTypes_subData .
                    ?inputName_subData rdf:type ?individualData_subData .

                    ?inputName pv:feeds* ?inputName_subData .

                    ?context pv2:has ?inputName .
                    ?context  rdf:type/rdfs:subClassOf* pv2:Context .
                    ?context  rdf:type ?contextType  .

                    #Find transformation count for datainput if it is set
                    OPTIONAL {
                         ?inputName_subData pv2:TemplateCount ?templateCount .
                    }.
                    OPTIONAL {
                        ?inputName_subData pv2:TemporalResolution ?resolution .
                    }
                    FILTER ( !bound(?templateCount) || ?templateCount < ?max_count  )

                }
                """, initNs = NSUtil.get_binding_namespaces()
            )

        ro = inputModel_temp.query(q, initBindings={'?max_count': self.max_transformation_count})

        domain_data_found_using_data = {}

        for row in ro:
            if not row[6] in domain_data_found_using_data : domain_data_found_using_data[row[6]] = {}
            if not row[1] in domain_data_found_using_data[row[6]] : domain_data_found_using_data[row[6]][row[1]] = []
            template_count =  0 if row[4] is None else  int(row[4])
            resolution =  None if row[5] is None else  float(row[5])
            domain_data_found_using_data[row[6]][row[1]].append(Data(row[3], resolution, subject_name=row[2], template_count= template_count, base_subject_name = row[0], spatial_resolutions=row[7]))
            # domain_data_found_using_data[row[1]].append(row[2])
        return domain_data_found_using_data


    def find_all_domain_types_from_input_data_old(self,inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)

        inputModel_temp.parse(self.base_ontology_url)

        q = rdflib.plugins.sparql.prepareQuery("""
                # SELECT DISTINCT  ?inputName ?individualData ?inputName_subData ?individualData_subData ?templateCount ?resolution ?context ?contextType
                SELECT DISTINCT  ?inputName ?individualData ?inputName_subData ?individualData_subData ?templateCount ?resolution ?context ?contextType
                WHERE {
                    ?individualData rdf:type owl:NamedIndividual .
                    ?inputName rdf:type ?individualData .

                    ?inputName rdf:type/rdfs:subClassOf pv:Data .
                    # ?inputName rdf:type ?dataTypes .

                    ?individualData_subData rdf:type owl:NamedIndividual .
                    ?inputName_subData rdf:type ?individualData_subData .

                    ?dataTypes_subData rdfs:subClassOf pv:Data .
                    ?inputName_subData rdf:type ?dataTypes_subData .

                    ?inputName pv:feeds* ?inputName_subData .

                    ?context pv2:has ?inputName .
                    ?context  rdf:type/rdfs:subClassOf* pv2:Context .
                    ?context  rdf:type ?contextType  .

                    #Find transformation count for datainput if it is set
                    OPTIONAL {
                         ?inputName_subData pv2:TemplateCount ?templateCount .
                    }.
                    OPTIONAL {
                        ?inputName_subData pv2:TemporalResolution ?resolution .
                    }
                    FILTER ( !bound(?templateCount) || ?templateCount < ?max_count  )

                }
                """, initNs = NSUtil.get_binding_namespaces()
            )

        seconds = time.time()

        ro = inputModel_temp.query(q, initBindings={'?max_count': self.max_transformation_count})

        domain_data_found_using_data = {}

        for row in ro:
            print("Loop:", time.time()- seconds)
            if not row[6] in domain_data_found_using_data : domain_data_found_using_data[row[6]] = {}
            if not row[1] in domain_data_found_using_data[row[6]] : domain_data_found_using_data[row[6]][row[1]] = []
            template_count =  0 if row[4] is None else  int(row[4])
            resolution =  None if row[5] is None else  float(row[5])
            domain_data_found_using_data[row[6]][row[1]].append(Data(row[3], resolution, subject_name=row[2], template_count= template_count, base_subject_name = row[0], spatial_resolutions=row[7]))
            # domain_data_found_using_data[row[1]].append(row[2])
        return domain_data_found_using_data

    def find_context_structure(self, inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)
        inputModel_temp.parse(self.base_ontology_url)

        ro = inputModel_temp.query(
            """
                SELECT ?sub_class_types ?sub_class_subject ?root_type ?root_subject
                WHERE {
                    ?root_subject rdf:type ?root_type .
                    ?root_subject pv:star ?sub_class_subject .

                    ?sub_class_types rdfs:subClassOf* pv2:Context .
                    ?sub_class_subject rdf:type ?sub_class_types .
                }
            """, initNs = NSUtil.get_binding_namespaces())

        contexts = {}

        for row in ro:
            contexts[row[1]] = ContextInput(row[0], row[1], row[2], row[3])
        return contexts

    def find_all_data_types_for_domain_data(self,inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)

        inputModel_temp.parse(self.base_ontology_url)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT DISTINCT ?individualData ?inputName ?individualData_subData
                WHERE {
                    ?individualData         rdf:type        owl:NamedIndividual .
                    ?dataTypes              rdfs:subClassOf pv:Data .
                    
                    ?individualData_subData rdf:type        owl:NamedIndividual .
                    
                    ?inputName rdf:type ?individualData .
                    ?inputName rdf:type ?dataTypes .
                    
                    ?inputName_subData rdf:type ?individualData_subData .
                    
                    ?feedsRelations rdf:type ?individualData_subData .
                    
                    ?inputName pv:feeds* ?feedsRelations .
                }
                 """
                , initNs = NSUtil.get_binding_namespaces()
            )

        ro = inputModel_temp.query(q)

        domain_data_found_using_data = {}

        for row in ro:
            if not row[1] in domain_data_found_using_data : domain_data_found_using_data[row[1]] = []
            domain_data_found_using_data[row[1]].append(row[2])
        return domain_data_found_using_data

    def find_used_data_types(self,inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)

        inputModel_temp.parse(self.base_ontology_url)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT DISTINCT ?inputName ?individualData ?datatypes
                WHERE {
                    ?individualData rdf:type owl:NamedIndividual .
                    ?inputName rdf:type ?individualData .
                }
                """
                , initNs = NSUtil.get_binding_namespaces()
            )
        # ns = dict(pv=Namespace("<https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#>"))

        ro = inputModel_temp.query(q)

        used_data_types = {}

        for row in ro:
            used_data_types[row[0]] = row[1]
        return used_data_types

    def find_used_contexts(self,inputModel):
        inputModel_temp = copy.deepcopy(inputModel)
        inputModel_temp.parse(self.domain_url)
        inputModel_temp.parse(self.extention_ontology_url)

        inputModel_temp.parse(self.base_ontology_url)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT DISTINCT ?context_subject ?ContextType
                WHERE {
                    ?context_subject rdf:type/rdfs:subClassOf* pv2:Context .
                    ?context_subject  rdf:type ?ContextType .

                }
                """
                , initNs = NSUtil.get_binding_namespaces()
            )
        # ns = dict(pv=Namespace("<https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#>"))

        ro = inputModel_temp.query(q)

        used_contexts = {}

        for row in ro:
            used_contexts[row[0]] = row[1]
        return used_contexts


    # def find_subject_for_contexts(self,inputModel):
    #     inputModel_temp = copy.deepcopy(inputModel)
    #     inputModel_temp.parse(self.domain_url)
    #     inputModel_temp.parse(self.extention_ontology_url)

    #     inputModel_temp.parse(self.base_ontology_url)

    #     q = rdflib.plugins.sparql.prepareQuery("""
    #             SELECT DISTINCT ?context_subject ?ContextType
    #             WHERE {
    #                 ?context_subject rdf:type/rdfs:subClassOf* pv2:Context .
    #                 ?context_subject  rdf:type ?ContextType .
    #             }
    #             """
    #             , initNs = NSUtil.get_binding_namespaces()
    #         )
    #     # ns = dict(pv=Namespace("<https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#>"))

    #     ro = inputModel_temp.query(q)

    #     used_contexts = {}

    #     for row in ro:
    #         used_contexts[row[0]] = row[1]
    #     return used_contexts