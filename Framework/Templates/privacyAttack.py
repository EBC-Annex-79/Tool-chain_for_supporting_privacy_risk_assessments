from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugin
import uuid
from Framework.Templates.template import Util as BaseUtil
from Framework.Data.ResolutionForTransformation import ResolutionForTransformation
from Framework.Data.Data import Data
from Framework.Data.PrivacyAttack import PrivacyAttack
import Framework.namespace_util as NSUtil
import Framework.Domain.util as DataUtil
import itertools

# from Templates.template.util import Util as BaseUtil
class Util(BaseUtil):
    def __init__(self, domain_path, base_ontology_path, extention_ontology_path):
        super().__init__(domain_path, base_ontology_path, extention_ontology_path)
        self.loaded_privacy_attack = {}

    def get_loaded_privacy_attack(self,template):
        if not template in self.loaded_privacy_attack:
            self.loaded_privacy_attack[template] = PrivacyAttack(template, self.domain_path,self.base_ontology_path, self.extention_ontology_path, self.get_domain_supported_data_streams())
        return self.loaded_privacy_attack[template]

    def _get_domain_types_from_input_data(self, inputModel):
        if self.domain_types_from_input_data is None:
            self.domain_types_from_input_data = self.inputUtil.find_all_domain_types_from_input_data(inputModel)
        return self.domain_types_from_input_data

    def combind_using_template(self,inputModel,template, used_data_inputs, context=None):
        stored_privacy_attack = self.get_loaded_privacy_attack(template)
        user_data_input_list =used_data_inputs.values()

        template_name = stored_privacy_attack.get_template_name()

        combination_of_user_inputs = list(itertools.product(*user_data_input_list))
        for combination_of_user_input in combination_of_user_inputs:
            template_rand_nr = uuid.uuid4().__str__()

            used_data_input = []

            for data_obj in combination_of_user_input:
                inputModel.add((data_obj.subject_name, self.PRIVVULN.feeds, data_obj.template_name+template_rand_nr))
                inputModel.add((data_obj.domain_data_type, self.PRIVVULN.feeds, data_obj.template_name+template_rand_nr))

            inputModel.add((data_obj.template_name+template_rand_nr, self.RDF.type, self.PRIVVULN.PrivacyAttack))
            inputModel.add((data_obj.template_name+template_rand_nr, self.PRIVVULNV2.name, data_obj.template_name))

            template_subject = stored_privacy_attack.get_template_subject()
            output_data_type = stored_privacy_attack.get_output_data_type()
            output_subject = stored_privacy_attack.get_output_subject()
            risk_description  = stored_privacy_attack.get_risk_description()
            privacy_risk_score  = stored_privacy_attack.get_privacy_risk_score()
            privacy_Strategies  = stored_privacy_attack.get_privacy_Strategies()

            inputModel.add((output_subject+template_rand_nr, self.RDF.type, output_data_type))
            inputModel.add((data_obj.template_name+template_rand_nr, self.PRIVVULN.creates, output_subject+template_rand_nr))

            template_count = self._find_template_count(combination_of_user_input)
            inputModel.add((output_subject+template_rand_nr, self.PRIVVULNV2.TemplateCount, rdflib.Literal(template_count)))
            inputModel.add((output_subject+template_rand_nr, self.PRIVVULNV2.name, output_subject))
            inputModel.add((output_subject+template_rand_nr, self.PRIVVULNV2.description, rdflib.Literal(risk_description)))
            inputModel.add((output_subject+template_rand_nr, self.PRIVVULNV2.privacyRiskScore, rdflib.Literal(privacy_risk_score)))
            for privacy_Strategy in privacy_Strategies:
                inputModel.add((output_subject+template_rand_nr, self.PRIVVULNV2.privacyStrategy, rdflib.Literal(privacy_Strategy)))

        return inputModel

    def get_template_name(self, template):
        privacyAttackName = ""
        try:
            #Only one privacy attack
            privacyAttackName = template.value(predicate = self.RDF.type, object = self.PRIVVULN.PrivacyAttack , any = False, default="")
        except rdflib.exceptions.UniquenessError:
            return None
        return privacyAttackName

    def _get_template_triple(self):
        return (None,  RDF.type, PRIVVULN.PrivacyAttack)

    def validate_template(self, template):
        template_name = self.get_template_name(template)
        if template_name == "":
            #Does not have any privacy attack
            return None
        elif template_name is None:
            print("template can not have more then one privacy attack")
            return False
        elif template_name is not None:
            return True
        if not super()._get_constraint_triple() in template:
            print("template:%s most have a constraint triple", template_name)
            return False
        return False

    def can_template_be_used(self,inputModel, template):
        stored_privacy_attack = self.get_loaded_privacy_attack(template)
        template_needed_data_types = stored_privacy_attack.get_model_requeued_data_types()
        template_needed_data_dict = DataUtil.find_domain_data_in_data_list_dict(template_needed_data_types)

        context_data_types = self._get_context_data_types(inputModel)

        #import pdb; pdb.set_trace()

        context_structure = self._get_input_context_structure(inputModel)

        output_type = stored_privacy_attack.get_output_data_type()

        template_name = stored_privacy_attack.get_template_name()

        usered_data_subjects = []

        usefull_data_input = {}
        for context in context_data_types.keys():
            context_data_type = context_data_types[context]
            template_can_be_used_in_context = False
                # template_can_be_used_in_data_context = True
            temp_data_objects = {}
            for template_data_type in template_needed_data_types:
                context_data_objects = []
                for elem in context_data_type:
                    if elem.domain_data_type == template_data_type.domain_data_type:
                        context_data_objects.append(elem)
                if len(context_data_objects) > 0:
                    for context_data_object in context_data_objects:
                        spatial_resolution_match = False
                        if len(template_data_type.spatial_resolutions) > 0:
                            for spatial_resolutions in template_data_type.spatial_resolutions:
                                if self._context_match(spatial_resolutions, context_data_object.context):
                                    spatial_resolution_match = True
                                    break
                        else:
                            spatial_resolution_match = True
                        if spatial_resolution_match:
                            if context_data_object.temporal_resolutions is None:
                                print(context_data_object)
                            if template_data_type.temporal_resolutions is None or context_data_object.temporal_resolutions <= template_data_type.temporal_resolutions:
                                if template_data_type.domain_data_type not in temp_data_objects: temp_data_objects[template_data_type.domain_data_type] = []
                                temp_data_objects[template_data_type.domain_data_type].append(Data(template_data_type.domain_data_type, context_data_object.temporal_resolutions,template_name = template_name, subject_name = context_data_object.subject_name, template_count = context_data_object.template_count, base_subject_name=context_data_object.base_subject_name,description=template_data_type.description, spatial_resolutions=template_data_type.context))
            if len(temp_data_objects.keys()) == len(template_needed_data_types):
                usefull_data_input[context] = temp_data_objects
            elif len(temp_data_objects.keys()) > 0:
                #look for data stream at a higher level in the context strucktor to find missing sources
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
                                    if stream.temporal_resolutions is None or data_type.temporal_resolutions <= stream.temporal_resolutions:
                                        data_type.spatial_resolutions = data_type.context
                                        data_type.template_name = template_name
                                        if stream.temporal_resolutions is None or stream.temporal_resolutions >= stream.temporal_resolutions:
                                            if stream.domain_data_type not in temp_data_objects: temp_data_objects[stream.domain_data_type] = []
                                            temp_data_objects[stream.domain_data_type].append(data_type)
                                        # elif stream.temporal_resolutions >= stream.temporal_resolutions:
                                        #     if stream.domain_data_type not in temp_data_objects: temp_data_objects[stream.domain_data_type] = []
                                        #     temp_data_objects[stream.domain_data_type].append(data_type)
                    if context_name not in context_structure:
                        context_has_base = False
                        break
                    context_objet = context_structure[context_name]
                    context_name = context_objet.super_subject
                if len(temp_data_objects) == len(template_needed_data_types):
                    # temp_subject_names = [x.subject_name for x in temp_data_objects]
                    # if len(set(temp_subject_names) & set(usered_data_subjects)) == 0:
                        # usered_data_subjects.extend(temp_subject_names)
                    usefull_data_input[context] = temp_data_objects
        return usefull_data_input