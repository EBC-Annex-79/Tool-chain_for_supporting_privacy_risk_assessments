from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugin
import Framework.namespace_util as NSUtil
from Framework.Input.InputData  import Util as InputUtil

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

    def _get_domain_supported_data_types(self):
        if self.domain_supported_data_types is None:
            self.domain_supported_data_types = self.__find_domain_supported_data_types()
        return self.domain_supported_data_types

    def _get_domain_supported_contexts(self):
        if self.domain_supported_contexts is None:
            self.domain_supported_contexts = self.__find_domain_supported_contexts()
        return self.domain_supported_contexts

    def __find_domain_supported_contexts(self):
        model = Graph()
        model.parse(self.domain_path)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT ?individualData
                WHERE {
                    ?individualData rdfs:subClassOf* pv2:Context .
                }
                """,
                initNs = NSUtil.get_binding_namespaces()
                # ,
                # initNs = {}
            )

        ro = model.query(q)

        supported_contexts = []

        for row in ro:
            supported_contexts.append(row[0])
        return supported_contexts

    def __find_domain_supported_data_types(self):
        model = Graph()
        model.parse(self.domain_path)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT ?individualData
                WHERE {
                    ?individualData rdf:type owl:NamedIndividual .
                    # ?individualData rdf:type/rdfs:subClassOf* pv:Data
                }
                """,
                initNs = NSUtil.get_binding_namespaces()
                # ,
                # initNs = {}
            )

        ro = model.query(q)

        supported_data_types = []

        for row in ro:
            supported_data_types.append(row[0])
        return supported_data_types

    def _find_template_name(self):
         pass

    def validate(self,template,class_name=None):
        pass

    def _validate_constraint(self, template, template_name, class_name):
        if not (None,  self.RDF.type, self.PRIVVULNV2.Constraint) in template:
            print("Template: %s most have a constraint triple"%template_name)
            return False
        domain_types = self._get_domain_supported_data_types()
        output_results = True
        for subject in template.subjects(self.RDF.type, self.PRIVVULNV2.Constraint):
            if not (subject,  self.PRIVVULN.feeds, None) in template:
                print("Constraint: %s"%subject, " most have defined a data input type, in class %s"%class_name)
                output_results = False
            else:
                found_supported_data_type = False
                for object in template.objects(subject, self.PRIVVULN.feeds):
                    if object in domain_types:
                        if not found_supported_data_type:
                            found_supported_data_type = True
                        else:
                            print("Constraint: %s"%subject, " most only defined a one domain datatype, in class %s"%class_name)
                            output_results = False
                if not found_supported_data_type:
                    print("Constraint: %s"%subject, " most defined a one domain datatype, in class %s"%class_name)
                    output_results = False
                if not (subject,  self.PRIVVULN.feeds, template_name) in template:
                    print("Constraint: %s does not ref to the template model"%subject, " in template %s"%template_name, "in class %s"%class_name)
                    output_results = False
        return output_results

    def _get_constraint_triple(self):
        return (None,  self.RDF.type, self.PRIVVULNV2.Constraint)

class Transforamtion_validator(Validator):
    def __init__(self,  domain_path,base_ontology_path, extention_ontology_path):
        super().__init__(domain_path,base_ontology_path, extention_ontology_path)

    def _find_template_name(self, transformation):
        transformationName = ""
        try:
            #Only one transformation
            transformationName = transformation.value(predicate = self.RDF.type, object = self.PRIVVULN.Transformation , any = False, default="")
        except rdflib.exceptions.UniquenessError:
            return None
        return transformationName

    def _validate_spatial_resolution(self, template, template_name, class_name):
        output_results = True
        domain_supported_contexts = self._get_domain_supported_contexts()
        output_subject = None
        for subject in template.subjects(self.RDF.type, self.PRIVVULNV2.SpatialResolution):
            if not (subject,  self.PRIVVULNV2.spatialInput, None) in template:
                print("SpatialResolution: %s"%subject, "most have defined a spatialInput, in class %s"%class_name)
                output_results = False
            else:
                found_supported_context = False
                for object in template.objects(subject,  self.PRIVVULNV2.spatialInput):
                    if object in domain_supported_contexts:
                        if not found_supported_context:
                            found_supported_context = True
                        else:
                            print("SpatialResolution: %s"%subject, " most only have one defined a spatialInput supported for domain,in class %s"%class_name)
                            output_results = False
                    else:
                        print("SpatialResolution: %s"%subject, " most have defined a spatialInput supported for domain, found context set to %s"%object," in class %s"%class_name)
                        output_results = False
            if not (subject,  self.PRIVVULNV2.spatialOutput, None) in template:
                print("SpatialResolution: %s"%subject, " most have defined a spatialOutput, in class %s"%class_name)
                output_results = False
            else:
                found_supported_context = False
                for object in template.objects(subject,  self.PRIVVULNV2.spatialOutput):
                    if object in domain_supported_contexts:
                        if not found_supported_context:
                            found_supported_context = True
                            if output_subject is None:
                                output_subject = object
                            elif not output_subject == object:
                                print("spatialOutput: must be the same of all SpatialResolution,in class %s"%class_name)
                                output_results = False
                        else:
                            print("SpatialResolution: %s "%subject, "most only have one defined a spatialOutput supported for domain,in class %s"%class_name)
                            output_results = False
                    else:
                        print("SpatialResolution: %s "%subject, " most have defined a spatialOutput supported for domain, found context set to %s,"%object," in class %s"%class_name)
                        output_results = False
            if not (None,  self.PRIVVULN.feeds, subject) in template:
                print("SpatialResolution: %s "%subject, " most have defined a feeds relation to a Constraint class, in class %s"%class_name)
                output_results = False
        return output_results

    def __validate_time_resolution_internal(self,template, subject, class_name, time_resolution_name):
        output_results = True
        if not (subject,  self.PRIVVULNV2.TimeInput, None) in template:
                print("%s: "%time_resolution_name, " %s "%subject," most have defined a TimeInput, in class %s"%class_name)
                output_results = False
        if not (subject,  self.PRIVVULNV2.TimeOutput, None) in template:
            print("%s: "%time_resolution_name, "%s "%subject," most have defined a TimeOutput, in class %s"%class_name)
            output_results = False
        if not (None,  self.PRIVVULN.feeds, subject) in template:
                print("%s: "%time_resolution_name, "%s "%subject," most have defined a feeds relation to a Constraint class, in class %s"%class_name)
                output_results = False
        return output_results

    def _validate_time_resolution(self, template, template_name, class_name):
        output_results = True
        for subject in template.subjects(self.RDF.type, self.PRIVVULNV2.TimeResolutionLinear):
            output_results = output_results & self.__validate_time_resolution_internal(template, subject, class_name ,"TimeResolutionLinear")
        for subject in template.subjects(self.RDF.type, self.PRIVVULNV2.TimeResolutionPair):
            output_results = output_results & self.__validate_time_resolution_internal(template, subject, class_name ,"TimeResolutionPair")
        return output_results

    def _validate_transformation(self, template, template_name, class_name):
        output_results = True
        domain_types = self._get_domain_supported_data_types()
        for subject in template.subjects(self.RDF.type, self.PRIVVULN.Transformation):
            found_output = False
            for object in template.objects(subject,self.PRIVVULN.feeds):
                for output_object in template.objects(object,self.RDF.type):
                    if output_object in domain_types:
                        if not found_output:
                            found_output = True
                        else:
                            print(("Transformation: "+subject+" most have defined only one relation to a domain supported data class, in class " + class_name ))
                            output_results = False
            if not found_output:
                print(("Transformation: "+subject+" most have defined a feeds relation to a domain supported data class, in class "+ class_name))
                output_results = False
        return output_results

    def validate(self, template, class_name):
        template_name = self._find_template_name(template)
        validate_results = True
        if template_name == "":
            print("Template most have one transformation, in class %s"%class_name)
            validate_results = False
        elif template_name is None:
            print("Template can not have more then one transformation, in class %s"%class_name)
            validate_results = False
        else:
            if not super()._validate_constraint(template, template_name, class_name):
                validate_results = False
            if not self._validate_spatial_resolution(template, template_name, class_name):
                validate_results = False
            if not self._validate_time_resolution(template, template_name, class_name):
                validate_results = False
            if not self._validate_transformation(template, template_name, class_name):
                validate_results = False
        return validate_results

    def _get_template_triple(self):
        return (None,  self.RDF.type, self.PRIVVULN.Transformation)

class Privacy_attack_validator(Validator):
    def __init__(self,domain_path,base_ontology_path, extention_ontology_path):
        super().__init__(domain_path,base_ontology_path, extention_ontology_path)

    def _find_template_name(self, privacy_attack):
        privacyAttackName = ""
        try:
            #Only one transformation
            privacyAttackName = privacy_attack.value(predicate = self.RDF.type, object = self.PRIVVULN.PrivacyAttack , any = False, default="")
        except rdflib.exceptions.UniquenessError:
            return None
        return privacyAttackName

    def _validate_privacy_risk(self, template, template_name, class_name,privacy_risk_subject):
        output_results = True
        found_privacyRiskScore = False
        for privacyRiskScore in template.objects(privacy_risk_subject, self.PRIVVULNV2.privacyRiskScore):
            if not found_privacyRiskScore:
                found_privacyRiskScore = True
            else:
                output_results = False
                print("PrivacyRisk: %s"%privacy_risk_subject," most only have defined a privacyRiskScore, in class %s"%class_name)
        if not found_privacyRiskScore:
                output_results = False
                print("PrivacyRisk: %s"%privacy_risk_subject," most have defined a privacyRiskScore, in class %s"%class_name)
        return output_results

    def _validate_privacy_attacks(self, template, template_name, class_name):
        output_results = True
        domain_types = self._get_domain_supported_data_types()
        for subject in template.subjects(self.RDF.type, self.PRIVVULN.PrivacyAttack):
            found_output = False
            for privacy_risk_subject in template.objects(subject,self.PRIVVULN.creates):
                if (privacy_risk_subject,  self.RDF.type, self.PRIVVULN.PrivacyRisk) in template:
                    output_results = output_results & self._validate_privacy_risk(template, template_name, class_name, privacy_risk_subject)
                    if not found_output:
                        found_output = True
                    else:
                        output_results = False
                        print("PrivacyAttack: %s"%subject," most only have defined a creates relation to a PrivacyRisk, in class %s"%class_name)
            if not found_output:
                print("PrivacyAttack: %s"%subject," most have defined a creates relation to a PrivacyRisk, in class %s"%class_name)
                output_results = False
        return output_results

    def validate(self, template, class_name):
        template_name = self._find_template_name(template)
        validate_results = True
        if template_name == "":
            print("Template most have one Privacy attack, in class %s"%class_name)
            validate_results = False
        elif template_name is None:
            print("Template can not have more then one Privacy attack, in class %s"%class_name)
            validate_results = False
        else:
            if not super()._validate_constraint(template, template_name, class_name):
                validate_results = False
            if not self._validate_privacy_attacks(template, template_name, class_name):
                validate_results = False
        return validate_results

    def _get_template_triple(self):
        return (None,  self.RDF.type, self.PRIVVULN.PrivacyAttack)



class Input_validator(Validator):
    def __init__(self,domain_path,base_ontology_path, extention_ontology_path):
        super().__init__(domain_path,base_ontology_path, extention_ontology_path)

    def validate(self, template, class_name=None):
        input_util = InputUtil(self.domain_path, self.base_ontology_path, self.extention_ontology_path)
        data_inputs = input_util.find_used_data_types(template)
        contexts = input_util.find_used_contexts(template)
        validate = True
        for key,v in contexts.items():
            found_relation = False
            for subject in template.objects(key,self.PRIVVULNV2.has):
                if subject in data_inputs.keys():
                    found_relation = True
                else:
                    # import pdb; pdb.set_trace()
                    print("%s used a none supported datatype"%subject)
                    validate = False
                    break
            for subject in template.objects(key,self.PRIVVULN.star):
                if subject in contexts.keys():
                    found_relation = True
                else:
                    import pdb; pdb.set_trace()
                    print("%s has no relation to other type"%subject)
                    validate = False
                    break
            if not found_relation:
                import pdb; pdb.set_trace()
                validate = False
                break
        for key,v in data_inputs.items():
            found_relation = False
            for subject in template.subjects(self.PRIVVULNV2.has, key):
                if not found_relation:
                    found_relation = True
                else:
                    #may only have one
                    import pdb; pdb.set_trace()
                    validate = False
                    break
            if not found_relation:
                import pdb; pdb.set_trace() 
                validate = False
                break
            if (key, self.RDF.type, self.PRIVVULN.TimeSeries) in template:
                value = None
                try:
                    #Only one transformation
                    value = template.value(subject=key, predicate = self.PRIVVULNV2.TemporalResolution, any = False, default=None)
                except rdflib.exceptions.UniquenessError:
                    import pdb; pdb.set_trace()
                    validate = False
                if value is None or type(value) != rdflib.term.Literal or value.datatype != rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#double') or value.value < 0:
                    import pdb; pdb.set_trace()
                    validate = False
        return validate