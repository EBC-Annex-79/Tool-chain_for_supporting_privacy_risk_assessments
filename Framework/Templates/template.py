from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugin
from Framework.Input.InputData import Util as IntupUtil
from Framework.Data.Data import Data
from Framework.Domain.domainData import DomainData
import Framework.namespace_util as NSUtil

class Util:
    def __init__(self, domain_path, base_ontology_path, extention_ontology_path):
        self.domain_path = domain_path
        self.base_ontology_path =base_ontology_path
        self.extention_ontology_path = extention_ontology_path
        self.RDF  = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        self.PRIVVULN = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#')
        self.PRIVVULNV2 = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunlV2.ttl#')
        self.inputUtil = IntupUtil(domain_path,base_ontology_path,extention_ontology_path)
        self._context_structure = None
        self.domain_supported_data_streams = None
        self.input_context_structure = None
        self.domain_types_from_input_data = None
        self.context_data_types = None

    def _get_input_context_structure(self, inputModel):
        if self.input_context_structure is None:
            self.input_context_structure =  self.inputUtil.find_context_structure(inputModel)
        return self.input_context_structure

    def get_domain_supported_data_streams(self):
        if self.domain_supported_data_streams is None:
            self.domain_supported_data_streams = self._find_domain_supported_data_streams()
        return self.domain_supported_data_streams

    def _get_context_structure(self):
        if self._context_structure is None:
            domainData = DomainData(self.domain_path, self.base_ontology_path, self.extention_ontology_path)
            self._context_structure = domainData.find_context_structure()
        return self._context_structure

    def _context_match(self,template_context,input_context):
        context_structure = self._get_context_structure()

        if input_context == template_context:
            return True
        elif input_context == self.PRIVVULNV2.Context or template_context == self.PRIVVULNV2.Context:
            return False

        match = False
        base_context = input_context

        while not match:
            base_context = context_structure[base_context]
            match = base_context == template_context
            if base_context == self.PRIVVULNV2.Context:
                break
        return match

    def _context_base_type(self,input_context):
        context_structure = self._get_context_structure()

        base_context = input_context

        while True:
            temp_base_context = context_structure[base_context]
            if temp_base_context == self.PRIVVULNV2.Context:
                break
            else:
                base_context =    temp_base_context
        return base_context

    def _get_context_data_types(self, inputModel):
        if self.context_data_types is None:
            self.context_data_types = self.inputUtil.find_all_input_data_old(inputModel)
        return self.context_data_types

    def data_input_in_same_spatial_resultion(self,used_data_inputs):
        if len(used_data_inputs) == 1:
            return True
        spatial_resolution = self._context_base_type(used_data_inputs[0].spatial_resolutions)
        for index in range(len(used_data_inputs)-1):
            if not self._context_match(spatial_resolution,used_data_inputs[index+1].spatial_resolutions):
                return False
        return True

    def _find_constraint_data_types_for_template(self,template):
        constraint_List = []
        for s in template.subjects(self.RDF.type, self.PRIVVULNV2.Constraint):
            if (s,  self.PRIVVULN.feeds, self.get_template_name(template)) in template:
                constraint_List.append(s)
            else:
                print("Constraint element %s does not ref to the template model"%s)
        return constraint_List

    def _find_data_types_for_template(self, template):
        constraint_List = self._find_constraint_data_types_for_template(template)
        model_data_types = []
        for cName in constraint_List:
            data_type  = self._find_used_data_input_for_constraint(template,cName)
            if data_type.domain_data_type:
                model_data_types.append(data_type)
        return model_data_types

    def _find_used_data_input_for_constraint(self,template,name_of_constraint):
        dataTypes = self._find_domain_supported_data_streams()
        dataType = None
        temporalResolution = None
        spatialResolution = None
        for o in template.objects(name_of_constraint,self.PRIVVULN.feeds):
            if o in dataTypes:
                dataType = o
                break

        if dataType is None:
            print(name_of_constraint, " uses not support data stream or no stream defined")
        else:
            try:
                #Only one transformation or PrivacyAttacks per model.
                temporalResolution = template.value(predicate = self.PRIVVULNV2.TemporalResolution, subject=name_of_constraint, any = False)
            except rdflib.exceptions.UniquenessError:
                return
        spatialResolutions = []
        for spatialResolution in template.objects(name_of_constraint,self.PRIVVULNV2.spatialRequirement):
            spatialResolutions.append(spatialResolution)
        temporalResolution = float(temporalResolution.value) if temporalResolution is not None else None
        return Data(dataType, temporalResolution, spatial_resolutions=spatialResolutions)

    def _find_domain_supported_data_streams(self):
        #all inputs needs to be in the inputModel in order to use the template.
        model = Graph()
        #Load domain ontology
        model.parse(self.domain_path)

        #Load base ontology
        model.parse(self.base_ontology_path)

        ro = model.query(
            """
            SELECT ?data
            WHERE {
                ?dataTypes rdfs:subClassOf pv:Data .
                ?data rdf:type ?dataTypes .
            }
            """,
            initNs = NSUtil.get_binding_namespaces())

        dataTypes = []
        for row in ro:
            dataTypes.append(row[0])
        return dataTypes

    def _find_domain_supported_spatial_resolutions(self):
        #all inputs needs to be in the inputModel in order to use the template.
        model = Graph()
        #Load domain ontology
        model.parse(self.domain_path)

        #Load base ontology
        model.parse(self.base_ontology_path)

        #TODO: update from pv:Data to something spatial
        ro = model.query(
            """
            SELECT ?data
            WHERE {
                ?dataTypes rdfs:subClassOf pv:Data .
                ?data rdf:type ?dataTypes .
            }
            """,
            initNs = NSUtil.get_binding_namespaces())

        dataTypes = []
        for row in ro:
            dataTypes.append(row[0])

        return dataTypes

    # def _spatial_resolutions_the_same_for_all_inputs(self,template_needed_data_types):
    #     if len(template_needed_data_types) == 1:
    #         return True

    #     spatial_resolutions = []
    #     for template_needed_data_type in template_needed_data_types:
    #         if len(template_needed_data_type.spatial_resolutions) > 0:
    #             if spatial_resolutions == []:
    #                 spatial_resolutions = template_needed_data_type.spatial_resolutions
    #                 continue
    #             match = False
    #             for template_spatial_resolution in template_needed_data_type.spatial_resolutions:
    #                 for spatial_resolution in spatial_resolutions:
    #                     if self._context_match(template_spatial_resolution, spatial_resolution):
    #                         match = True
    #                         break
    #                 if match == True:
    #                     break
    #             if match == False:
    #                 return False
    #     return True

    def _get_constraint_triple(self):
            return (None,  self.RDF.type, self.PRIVVULNV2.Constraint)

    def _find_template_count(self,used_data_inputs):
        counts = [d.template_count  for d in used_data_inputs]
        return max(counts)+1

    def get_template_name(self, template):
       pass

    def _get_template_triple(self):
        pass

    def validate_template(self, template):
        pass

    def combind_using_template(self,inputModel,template,used_data_inputs):
        pass

    def _find_output_for_template(self,template):
        pass