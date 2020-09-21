from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugin
import uuid
from Framework.Templates.template import Util as BaseUtil
from Framework.Data.ResolutionForTransformation import ResolutionForTransformation
from Framework.Data.SpatialRelation import SpatialRelation
from Framework.Data.Data import Data
from Framework.Data.Transformation import Transformation
import Framework.Domain.util as DataUtil
import time
import Framework.namespace_util as NSUtil
import itertools
import copy

# from Templates.template.util import Util as BaseUtil

class Util(BaseUtil):
    def __init__(self, domain_path, base_ontology_path, extention_ontology_path):
        super().__init__(domain_path, base_ontology_path, extention_ontology_path)
        self.loaded_transformations = {}
        self.data_creates_from_data_types = None

    def _clear_stored_data_types(self):
        self.context_data_types = None
        self.domain_types_from_input_data = None
        self.data_creates_from_data_types = None

    def _get_data_creates_from_data_types(self, inputModel):
        if self.data_creates_from_data_types is None:
            self.data_creates_from_data_types = self.inputUtil.find_all_data_creates_from_data_types(inputModel)
        return self.data_creates_from_data_types

    def _get_domain_types_from_input_data(self, inputModel):
        if self.domain_types_from_input_data is None:
            self.domain_types_from_input_data = self.inputUtil.find_all_data_types_for_domain_data(inputModel)
        return self.domain_types_from_input_data

    def get_loaded_transformation(self,template):
        if not template in self.loaded_transformations:
            self.loaded_transformations[template] = Transformation(template, self.domain_path,self.base_ontology_path, self.extention_ontology_path, self.get_domain_supported_data_streams())
        return self.loaded_transformations[template]

    def __add_element_to_max_resolutions(self,resolution, max_resolutions):
        if not resolution.domain_data_type in max_resolutions: max_resolutions[resolution.domain_data_type] =[]
        max_resolutions[resolution.domain_data_type].append(resolution.output_spatial_resolution)

    def _find_output_spatial_resultion_for_transformation(self,resolutions,used_data_inputs):
        max_resolutions = {}

        for used_data_input in used_data_inputs:
            if used_data_input.domain_data_type in resolutions:
                for domain_data_type in resolutions:
                        for resolution in resolutions[domain_data_type]:
                            if used_data_input.domain_data_type == resolution.domain_data_type:
                                if resolution.input_spatial_resolution == used_data_input.spatial_resolutions:
                                    self.__add_element_to_max_resolutions(resolution, max_resolutions)
            else:
               if not used_data_input.domain_data_type in max_resolutions: max_resolutions[used_data_input.domain_data_type] =[]
               max_resolutions[used_data_input.domain_data_type].append(used_data_input.spatial_resolutions)
        #Does all datatypes have an output
        if len(used_data_inputs) > len(max_resolutions):
            domain_data_types = DataUtil.find_domain_data_in_data_list(used_data_inputs)
            missing_resolutions =  domain_data_types -max_resolutions.keys()

            context_structure = self._get_context_structure()

            for missing_resolution in missing_resolutions:
                # data_input = used_data_inputs[missing_resolution]
                for domain_data_type in resolutions:
                    if missing_resolution == domain_data_type:
                        for resolution in resolutions[domain_data_type]:
                            spatial_resolution = used_data_input.spatial_resolutions
                            #Loops over to find if base contexts match
                            while (not spatial_resolution == self.PRIVVULNV2.Context):
                                if spatial_resolution == used_data_input.spatial_resolutions:
                                    self.__add_element_to_max_resolutions(resolution, max_resolutions)
                                    break
                                spatial_resolution = context_structure[spatial_resolution]
            if len(used_data_inputs) > len(max_resolutions):
                return None

        output_resolutions = None
        for domain_data_type in max_resolutions:
            temp_output_resolutions = max_resolutions[domain_data_type][0]
            for resolution in max_resolutions[domain_data_type]:
                if not resolution == temp_output_resolutions:
                    if not self._context_match(temp_output_resolutions, resolution):
                        temp_output_resolutions =  resolution
            if output_resolutions is None:
                output_resolutions = temp_output_resolutions
            elif not self._context_match(temp_output_resolutions, resolution):
                output_resolutions =  temp_output_resolutions
        return output_resolutions

    def combind_using_template(self,inputModel,template,used_data_inputs,context=None):
        stored_transformation = self.get_loaded_transformation(template)
        user_data_input_list =used_data_inputs.values()

        template_name = self.get_template_name(template)

        combination_of_user_inputs = list(itertools.product(*user_data_input_list))

        spatial_resolutions = stored_transformation.get_spatial_relations_for_transformation()

        for combination_of_user_input in combination_of_user_inputs:
            used_data_input = []
            for user_input in combination_of_user_input:
                used_data_input.append(user_input)

            spatial_resultion = self._find_output_spatial_resultion_for_transformation(spatial_resolutions,used_data_input)

            if spatial_resultion is None:
                return inputModel
            elif not self.data_input_in_same_spatial_resultion(combination_of_user_input):
                inputModel = self.combind_using_template_to_base_context(inputModel, combination_of_user_input, stored_transformation, template, context_url=context)
            elif not self.spatial_resultion_in_same_context_struckter(combination_of_user_input,spatial_resultion):
                inputModel = self.combind_using_template_to_super_context(inputModel, combination_of_user_input, stored_transformation, template, spatial_resultion)
            else:
                inputModel = self.combind_using_template_context(inputModel, combination_of_user_input, stored_transformation, template)

        #data model updating, therefore can domain_types not be reused, for the next transformation
        self._clear_stored_data_types()

        return inputModel

    def combind_using_template_old(self,inputModel,template,used_data_inputs):
        stored_transformation = self.get_loaded_transformation(template)

        spatial_resolutions = stored_transformation.get_spatial_relations_for_transformation()
        spatial_resultion = self._find_output_spatial_resultion_for_transformation(spatial_resolutions,used_data_inputs)
        if spatial_resultion is None:
            return inputModel
        elif not self.spatial_resultion_in_same_context_struckter(used_data_inputs,spatial_resultion):
            inputModel = self.combind_using_template_to_super_context(inputModel, used_data_inputs, stored_transformation, template, spatial_resultion)
        else:
            inputModel = self.combind_using_template_context(inputModel, used_data_inputs, stored_transformation, template)

        #data model updating, therefore can domain_types not be reused, for the next transformation
        self._clear_stored_data_types()

        return inputModel

    def combind_using_template_to_super_context(self,inputModel,used_data_inputs,stored_transformation, template, spatial_resultion):
        super_class_name_url = self.find_context_super_class(used_data_inputs,spatial_resultion, inputModel)
        if super_class_name_url is None:
            return inputModel

        super_class_name = super_class_name_url.split('#')[-1]

        for data_obj in used_data_inputs:
            inputModel.add((data_obj.subject_name, self.PRIVVULN.feeds, data_obj.template_name+super_class_name))
            inputModel.add((data_obj.domain_data_type, self.PRIVVULN.feeds, data_obj.template_name+super_class_name))

        inputModel.add((data_obj.template_name+super_class_name, self.RDF.type, self.PRIVVULN.Transformation))
        inputModel.add((data_obj.template_name+super_class_name, self.PRIVVULNV2.name, data_obj.template_name))

        output_subjet = stored_transformation.get_template_output_subject()
        output_data_type = stored_transformation.get_template_template_output_data_type()
        output_domain_data_type = stored_transformation.get_template_output_domain_data_type()

        inputModel.add((output_subjet+super_class_name, self.RDF.type, output_domain_data_type))
        inputModel.add((output_subjet+super_class_name, self.RDF.type, output_data_type))
        inputModel.add((output_subjet+super_class_name, self.PRIVVULNV2.name, output_subjet))

        inputModel.add((data_obj.template_name+super_class_name, self.PRIVVULNV2.creates, output_subjet+super_class_name))

        inputModel.add((super_class_name_url, self.PRIVVULNV2.has,output_subjet+super_class_name))

        time_resolutions = stored_transformation.get_time_relations_for_transformation()
        time_resultion = self._find_output_time_resultion_for_transformation(time_resolutions,used_data_inputs)

        if time_resultion is not None:
            if (output_subjet+super_class_name,self.PRIVVULNV2.TemporalResolution, None ) in inputModel:
                temporalResolution = inputModel.value(subject=output_subjet+super_class_name, predicate=self.PRIVVULNV2.TemporalResolution)
                if temporalResolution.value < time_resultion:
                    inputModel.remove((output_subjet+super_class_name, self.PRIVVULNV2.TemporalResolution, temporalResolution))
                    inputModel.add((output_subjet+super_class_name, self.PRIVVULNV2.TemporalResolution, rdflib.Literal(time_resultion)))
            else:
                inputModel.add((output_subjet+super_class_name, self.PRIVVULNV2.TemporalResolution, rdflib.Literal(time_resultion)))

        template_count = self._find_template_count(used_data_inputs)
        inputModel.add((output_subjet+super_class_name, self.PRIVVULNV2.TemplateCount, rdflib.Literal(template_count)))

        return inputModel

    def combind_using_template_to_base_context(self,inputModel,used_data_inputs,stored_transformation, template, context_url):
        context_subject_url = context_url

        template_rand_nr = uuid.uuid4().__str__()

        class_name = context_subject_url.split('#')[-1] + template_rand_nr

        for data_obj in used_data_inputs:
            inputModel.add((data_obj.subject_name, self.PRIVVULN.feeds, data_obj.template_name+class_name))
            inputModel.add((data_obj.domain_data_type, self.PRIVVULN.feeds, data_obj.template_name+class_name))

        inputModel.add((data_obj.template_name+class_name, self.RDF.type, self.PRIVVULN.Transformation))
        inputModel.add((data_obj.template_name+class_name, self.PRIVVULNV2.name, data_obj.template_name))

        output_subjet = stored_transformation.get_template_output_subject()
        output_data_type = stored_transformation.get_template_template_output_data_type()
        output_domain_data_type = stored_transformation.get_template_output_domain_data_type()

        inputModel.add((output_subjet+class_name, self.RDF.type, output_domain_data_type))
        inputModel.add((output_subjet+class_name, self.RDF.type, output_data_type))
        inputModel.add((output_subjet+class_name, self.PRIVVULNV2.name, output_subjet))

        inputModel.add((data_obj.template_name+class_name, self.PRIVVULNV2.creates, output_subjet+class_name))

        inputModel.add((context_subject_url, self.PRIVVULNV2.has,output_subjet+class_name))

        time_resolutions = stored_transformation.get_time_relations_for_transformation()
        time_resultion = self._find_output_time_resultion_for_transformation(time_resolutions,used_data_inputs)

        if time_resultion is not None:
            if (output_subjet+class_name,self.PRIVVULNV2.TemporalResolution, None ) in inputModel:
                temporalResolution = inputModel.value(subject=output_subjet+class_name, predicate=self.PRIVVULNV2.TemporalResolution)
                if temporalResolution.value < time_resultion:
                    inputModel.remove((output_subjet+class_name, self.PRIVVULNV2.TemporalResolution, temporalResolution))
                    inputModel.add((output_subjet+class_name, self.PRIVVULNV2.TemporalResolution, rdflib.Literal(time_resultion)))
            else:
                inputModel.add((output_subjet+class_name, self.PRIVVULNV2.TemporalResolution, rdflib.Literal(time_resultion)))

        template_count = self._find_template_count(used_data_inputs)
        inputModel.add((output_subjet+class_name, self.PRIVVULNV2.TemplateCount, rdflib.Literal(template_count)))

        return inputModel

    def combind_using_template_context(self,inputModel,used_data_inputs, stored_transformation, template):
        template_rand_nr = uuid.uuid4().__str__()

        for data_obj in used_data_inputs:
            inputModel.add((data_obj.subject_name, self.PRIVVULN.feeds, data_obj.template_name+template_rand_nr))
            inputModel.add((data_obj.domain_data_type, self.PRIVVULN.feeds, data_obj.template_name+template_rand_nr))

        inputModel.add((data_obj.template_name+template_rand_nr, self.RDF.type, self.PRIVVULN.Transformation))
        inputModel.add((data_obj.template_name+template_rand_nr, self.PRIVVULNV2.name, data_obj.template_name))

        output_subjet = stored_transformation.get_template_output_subject()
        output_data_type = stored_transformation.get_template_template_output_data_type()
        output_domain_data_type = stored_transformation.get_template_output_domain_data_type()

        # output_subjet, output_data_type, output_domain_data_type = self._find_output_for_template(template)

        inputModel.add((output_subjet+template_rand_nr, self.RDF.type, output_domain_data_type))
        inputModel.add((output_subjet+template_rand_nr, self.RDF.type, output_data_type))
        inputModel.add((output_subjet+template_rand_nr, self.PRIVVULNV2.name, output_subjet))

        inputModel.add((data_obj.template_name+template_rand_nr, self.PRIVVULN.feeds, output_subjet+template_rand_nr))

        time_resolutions = stored_transformation.get_time_relations_for_transformation()
        time_resultion = self._find_output_time_resultion_for_transformation(time_resolutions,used_data_inputs)

        if time_resultion is not None:
            inputModel.add((output_subjet+template_rand_nr, self.PRIVVULNV2.TemporalResolution, rdflib.Literal(time_resultion)))

        template_count = self._find_template_count(used_data_inputs)
        inputModel.add((output_subjet+template_rand_nr, self.PRIVVULNV2.TemplateCount, rdflib.Literal(template_count)))

        return inputModel


    def spatial_resultion_in_same_context_struckter(self,used_data_inputs,spatial_resultion):
        for used_data_input in used_data_inputs:
            if not self._context_match(spatial_resultion,used_data_input.spatial_resolutions):
                return False
        return True

    def find_context_super_class(self,used_data_inputs,spatial_resultion, inputModel):
        input_context_structures = self._get_input_context_structure(inputModel)
        super_subject = None
        for used_data_input in used_data_inputs:
            context_structure = used_data_input.context_subject
            found_spatial_resultion = False
            while context_structure in input_context_structures.keys():
                if input_context_structures[context_structure].super_domain_class_type == spatial_resultion:
                    super_subject =  input_context_structures[context_structure].super_subject
                    found_spatial_resultion = True
                    break
                else:
                    context_structure = input_context_structures[context_structure].super_subject
            if not found_spatial_resultion:
                return None
        return super_subject

    def find_context_subject(self,used_data_inputs,spatial_resultion, inputModel):
        input_context_structures = self._get_input_context_structure(inputModel)
        subject = None
        for used_data_input in used_data_inputs:
            context_structure = used_data_input.context_subject
            found_spatial_resultion = False
            if input_context_structures[context_structure].domain_class_type == spatial_resultion:
                subject =  input_context_structures[context_structure].subject
                found_spatial_resultion = True
                break
        if not found_spatial_resultion:
            return None
        return subject

    def _find_output_time_resultion_for_transformation(self,resolutions,used_data_inputs):
        temp_max_resolutions = {}
        max_resolutions =  {}

        for used_data_input in used_data_inputs:
            for resolution in resolutions:
                if used_data_input.domain_data_type == resolution.domain_data_type:
                    if self.PRIVVULNV2.TimeResolutionLinear in resolution.time_resolution_type:
                        if not resolution.domain_data_type in temp_max_resolutions.keys():
                            max_resolution = used_data_input.temporal_resolutions *  (resolution.time_resolution_output / resolution.time_resolution_input)
                            if not resolution.domain_data_type in temp_max_resolutions.keys() or temp_max_resolutions[resolution.domain_data_type] < max_resolution:
                                temp_max_resolutions[resolution.domain_data_type] = max_resolution
                    elif self.PRIVVULNV2.TimeResolutionPair in resolution.time_resolution_type:
                        if used_data_input.temporal_resolutions == resolution.input_temporal_resolution:
                            #IF a custom rule is set use it
                            max_resolutions[resolution.domain_data_type] = resolution.time_resolution_output

        for domain_data_type, max_resolution in temp_max_resolutions.items():
            if not domain_data_type in max_resolutions.keys():
                max_resolutions[domain_data_type] = max_resolution
        if len(max_resolutions) > 0:
            return max(max_resolutions.values())
        else:
            return None

    def get_template_name(self, template):
        transformationName = ""
        try:
            #Only one transformation
            transformationName = template.value(predicate = self.RDF.type, object = self.PRIVVULN.Transformation , any = False, default="")
        except rdflib.exceptions.UniquenessError:
            return None
        return transformationName

    def _get_template_triple(self):
        return (None,  self.RDF.type, self.PRIVVULN.Transformation)

    def validate_template(self, template):
        template_name = self.get_template_name(template)
        if template_name == "":
            #Does not have any transformation
            return None
        elif not super()._get_constraint_triple() in template:
           print("template:%s most have a constraint triple", template_name)
           return False
        elif template_name is None:
            print("template can not have more then one transformation")
            return False
        elif template_name is not None:
            return True
        return False

    # def can_template_be_used_old(self,inputModel, template):
    #     loaded_tempated = self.get_loaded_transformation(template)

    #     template_needed_data_types = loaded_tempated.get_model_requeued_data_types()

    #     context_data_types = self._get_context_data_types(inputModel)

    #     domain_data_types_found_using_transformations = self._get_domain_types_from_input_data(inputModel)

    #     outpout_type = loaded_tempated.get_template_output_domain_data_type()

    #     template_name = loaded_tempated.get_template_name()

    #     usefull_data_input = {}
    #     for context in context_data_types.keys():
    #         context_data_type = context_data_types[context]
    #         template_can_be_used_in_context = True
    #         domain_type_has_output = False
    #         temp_data_objects = []
    #         for template_data_type in template_needed_data_types:
    #             context_data_object = None
    #             context_data_objects = []
    #             for elem in context_data_type:
    #                 if elem.domain_data_type == template_data_type.domain_data_type:
    #                     context_data_object = elem
    #                     context_data_objects.append(elem)
    #             if context_data_object:
    #                 if context_data_object.subject_name in domain_data_types_found_using_transformations and outpout_type in domain_data_types_found_using_transformations[context_data_object.subject_name]:
    #                     template_can_be_used_in_context = False
    #                     domain_type_has_output = True
    #                     break
    #                 if len(template_data_type.spatial_resolutions) > 0:
    #                     spatial_resolution_match = False
    #                     for spatial_resolutions in template_data_type.spatial_resolutions:
    #                         if self._context_match(spatial_resolutions, context_data_object.context):
    #                             spatial_resolution_match = True
    #                             break
    #                 else:
    #                     spatial_resolution_match = True
    #                 if not spatial_resolution_match:
    #                     template_can_be_used_in_context = False
    #                     break
    #                 elif template_data_type.temporal_resolutions is None or context_data_object.temporal_resolutions is None or template_data_type.temporal_resolutions >= context_data_object.temporal_resolutions :
    #                     temp_data_objects.append(
    #                         Data(template_data_type.domain_data_type,
    #                             context_data_object.temporal_resolutions,
    #                             template_name = template_name,
    #                             subject_name = context_data_object.subject_name,
    #                             template_count = context_data_object.template_count,
    #                             spatial_resolutions=context_data_object.context,
    #                             context_subject=context_data_object.context_subject
    #                             ))
    #                 # elif context_data_object.temporal_resolutions is None or template_data_type.temporal_resolutions >= context_data_object.temporal_resolutions:
    #                 #     temp_data_objects.append(
    #                 #         Data(template_data_type.domain_data_type,
    #                 #             context_data_object.temporal_resolutions,
    #                 #             template_name = template_name,
    #                 #             subject_name = context_data_object.subject_name,
    #                 #             template_count = context_data_object.template_count,
    #                 #             spatial_resolutions=context_data_object.context,
    #                 #             context_subject=context_data_object.context_subject))
    #                 else:
    #                     template_can_be_used_in_context = False
    #                     break
    #             else:
    #                 template_can_be_used_in_context = False
    #                 break

    #         if template_can_be_used_in_context:
    #             usefull_data_input[context] = temp_data_objects

    #     return usefull_data_input


    def can_template_be_used(self,inputModel, template):
        loaded_tempated = self.get_loaded_transformation(template)

        template_needed_data_types = loaded_tempated.get_model_requeued_data_types()

        context_structure = self._get_input_context_structure(inputModel)

        context_data_types = self._get_context_data_types(inputModel)

        domain_data_types_found_using_transformations = self._get_domain_types_from_input_data(inputModel)

        data_creates_from_data_types = self._get_data_creates_from_data_types(inputModel)

        outpout_type = loaded_tempated.get_template_output_domain_data_type()

        template_name = loaded_tempated.get_template_name()

        template_needed_data_dict = DataUtil.find_domain_data_in_data_list_dict(template_needed_data_types)

        usefull_data_input = {}
        for context in context_data_types.keys():
            context_data_type = context_data_types[context]
            context_has_not_all_doamin_data_types = True
            context_has_not_all_doamin_data_types = True
            some_domain_type_has_not_output = False
            temp_data_objects = {}
            for template_needed_data_type in template_needed_data_types:
                types_found_in_context = []
                for data_type in context_data_type:
                    if data_type.domain_data_type == template_needed_data_type.domain_data_type:
                        if len(template_needed_data_type.spatial_resolutions) > 0:
                            spatial_resolution_match = False
                            for spatial_resolutions in template_needed_data_type.spatial_resolutions:
                                if self._context_match(spatial_resolutions, data_type.context):
                                    spatial_resolution_match = True
                                    break
                        else:
                            spatial_resolution_match = True
                        if spatial_resolution_match:
                            data_type.spatial_resolutions = data_type.context
                            data_type.template_name = template_name
                            if template_needed_data_type.temporal_resolutions is None or template_needed_data_type.temporal_resolutions >= data_type.temporal_resolutions:
                                if template_needed_data_type.domain_data_type not in temp_data_objects: temp_data_objects[template_needed_data_type.domain_data_type] =[]
                                temp_data_objects[template_needed_data_type.domain_data_type].append(data_type)
                            # elif template_needed_data_type.temporal_resolutions >= data_type.temporal_resolutions:
                            #     if template_needed_data_type.domain_data_type not in temp_data_objects: temp_data_objects[template_needed_data_type.domain_data_type] =[]
                            #     temp_data_objects[template_needed_data_type.domain_data_type].append(data_type)
            if len(temp_data_objects) == len(template_needed_data_types):
                holder_data_objects = copy.deepcopy(temp_data_objects)
                for data_objects in temp_data_objects:
                    data_type_temp_data_object = copy.deepcopy(temp_data_objects[data_objects])
                    for supperted_data_types in temp_data_objects[data_objects]:
                        if supperted_data_types.subject_name in domain_data_types_found_using_transformations and outpout_type in domain_data_types_found_using_transformations[supperted_data_types.subject_name]:
                            data_type_temp_data_object.remove(supperted_data_types)
                    if len(data_type_temp_data_object) > 0:
                        temp_data_objects[data_objects] = data_type_temp_data_object
                    else:
                        holder_data_objects.pop(data_objects)
                if len(holder_data_objects) == len(template_needed_data_types):
                    usefull_data_input[context] = temp_data_objects
                elif len(holder_data_objects) == 0:
                    continue
                else:
                    reusered_streams = temp_data_objects.keys() - holder_data_objects.keys()
                    new_temp_data = {}
                    for reusered_stream in reusered_streams:
                        new_temp_data[reusered_stream] = temp_data_objects[reusered_stream]
                    reusered_streams = temp_data_objects.keys() & holder_data_objects.keys()
                    for reusered_stream in reusered_streams:
                        new_temp_data[reusered_stream] = temp_data_objects[reusered_stream]
                    usefull_data_input[context] = new_temp_data
            elif len(temp_data_objects) > 0:
                missing_streams = template_needed_data_dict.keys() - temp_data_objects.keys()
                if context not in context_structure:
                    continue
                context_has_base = True
                context_objet = context_structure[context]
                context_name = context_objet.super_subject
                while context_has_base:
                    for missing_stream in missing_streams:
                        stream = template_needed_data_dict[missing_stream]
                        if len(stream.spatial_resolutions) > 0:
                            spatial_resolution_match = False
                            for spatial_resolutions in stream.spatial_resolutions:
                                if self._context_match(spatial_resolutions, context_objet.super_domain_class_type):
                                    spatial_resolution_match = True
                                    break
                        else:
                            spatial_resolution_match = True
                        if spatial_resolution_match and context_name in context_data_types:
                            for data_type in context_data_types[context_name]:
                                if data_type.domain_data_type == missing_stream:
                                    data_type.spatial_resolutions = data_type.context
                                    data_type.template_name = template_name
                                    if stream.temporal_resolutions is None or stream.temporal_resolutions >= data_type.temporal_resolutions:
                                        if stream.domain_data_type not in temp_data_objects: temp_data_objects[stream.domain_data_type] =[]
                                        temp_data_objects[stream.domain_data_type].append(data_type)
                                    # elif stream.temporal_resolutions >= stream.temporal_resolutions:
                                    #     if stream.domain_data_type not in temp_data_objects: temp_data_objects[stream.domain_data_type] =[]
                                    #     temp_data_objects[stream.domain_data_type].append(data_type)
                    if context_name not in context_structure:
                        context_has_base = False
                        break
                    context_objet = context_structure[context_name]
                    context_name = context_objet.super_subject

                if len(temp_data_objects) == len(template_needed_data_types):
                    holder_data_objects = copy.deepcopy(temp_data_objects)
                    for data_objects in temp_data_objects:
                        data_type_temp_data_object = copy.deepcopy(temp_data_objects[data_objects])
                        for supperted_data_types in temp_data_objects[data_objects]:
                            if supperted_data_types.subject_name in domain_data_types_found_using_transformations and outpout_type in domain_data_types_found_using_transformations[supperted_data_types.subject_name]:
                                data_type_temp_data_object.remove(supperted_data_types)
                            elif supperted_data_types.subject_name in data_creates_from_data_types  and outpout_type in data_creates_from_data_types[supperted_data_types.subject_name]:
                                data_type_temp_data_object.remove(supperted_data_types)
                        if len(data_type_temp_data_object) > 0:
                            temp_data_objects[data_objects] = data_type_temp_data_object
                        else:
                            holder_data_objects.pop(data_objects)
                    if len(holder_data_objects) == len(template_needed_data_types):
                        usefull_data_input[context] = temp_data_objects
                    elif len(holder_data_objects) == 0:
                        continue
                    else:
                        reusered_streams = temp_data_objects.keys() - holder_data_objects.keys()
                        new_temp_data = {}
                        for reusered_stream in reusered_streams:
                            new_temp_data[reusered_stream] = temp_data_objects[reusered_stream]
                        reusered_streams = temp_data_objects.keys() & holder_data_objects.keys()
                        for reusered_stream in reusered_streams:
                            new_temp_data[reusered_stream] = temp_data_objects[reusered_stream]
                        usefull_data_input[context] = new_temp_data
        return usefull_data_input


