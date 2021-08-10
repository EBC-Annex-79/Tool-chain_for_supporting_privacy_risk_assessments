from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugin
from Framework.Data.SpatialRelation import SpatialRelation
from Framework.Data.ResolutionForTransformation import ResolutionForTransformation
from Framework.Data.Data import Data
import Framework.namespace_util as NSUtil

class PrivacyAttack:
    def __init__(self,privacy_attack, domain_path, base_ontology_path, extention_ontology_path, domain_supported_data_streams):
        self.domain_path = domain_path
        self.base_ontology_path =base_ontology_path
        self.extention_ontology_path = extention_ontology_path
        self.privacy_attack = privacy_attack
        self.RDF  = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        self.PRIVVULN = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#')
        self.PRIVVULNV2 = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunlV2.ttl#')
        self.domain_supported_data_streams = domain_supported_data_streams
        self.model_requeued_data_types = None
        self.template_name = None
        self.template_subject = None
        self.output_data_type = None
        self.output_subject = None
        self.risk_description = None
        self.privacy_risk_score = None
        self.privacy_Strategies = None


    def get_privacy_risk_score(self):
        if self.privacy_risk_score is None:
            self.template_subject, self.output_data_type, self.output_subject, self.risk_description, self.privacy_risk_score, self.privacy_Strategies  = self._find_output_for_template()
        return self.privacy_risk_score

    def get_template_subject(self):
        if self.template_subject is None:
            self.template_subject, self.output_data_type, self.output_subject, self.risk_description, self.privacy_risk_score, self.privacy_Strategies  = self._find_output_for_template()
        return self.template_subject

    def get_output_data_type(self):
        if self.output_data_type is None:
            self.template_subject, self.output_data_type, self.output_subject, self.risk_description, self.privacy_risk_score, self.privacy_Strategies  = self._find_output_for_template()
        return self.output_data_type

    def get_output_subject(self):
        if self.output_subject is None:
            self.template_subject, self.output_data_type, self.output_subject, self.risk_description, self.privacy_risk_score, self.privacy_Strategies  = self._find_output_for_template()
        return self.output_subject

    def get_risk_description(self):
        if self.risk_description is None:
            self.template_subject, self.output_data_type, self.output_subject, self.risk_description, self.privacy_risk_score, self.privacy_Strategies  = self._find_output_for_template()
        return self.risk_description

    def get_privacy_Strategies(self):
        if self.privacy_Strategies is None:
            self.template_subject, self.output_data_type, self.output_subject, self.risk_description, self.privacy_risk_score, self.privacy_Strategies  = self._find_output_for_template()
        return self.privacy_Strategies

    def get_model_requeued_data_types(self):
        if self.model_requeued_data_types is None:
            self.model_requeued_data_types = self._find_data_types_for_template()
        return self.model_requeued_data_types

    def get_template_name(self):
        if self.template_name is None:
            self.template_name = self._find_template_name()
        return self.template_name

    def _find_data_types_for_template(self):
        constraintsList = self._find_Constraint_data_types_for_template(self.privacy_attack)
        model_data_types = []
        for rqName in constraintsList:
            data_type  = self._find_used_data_input_for_constraint(self.privacy_attack,rqName)
            if data_type.domain_data_type:
                model_data_types.append(data_type)
        return model_data_types

    def _find_Constraint_data_types_for_template(self,template):
        constraintsList = []
        for s in template.subjects(self.RDF.type, self.PRIVVULNV2.Constraint):
            if (s,  self.PRIVVULN.feeds, self.get_template_name()) in template:
                constraintsList.append(s)
            else:
                print("Constraint element %s does not ref to the template model"%s, " in template %s"%self.template_name)
        return constraintsList

    def _find_used_data_input_for_constraint(self,template,name_of_constraint):
        dataType = None
        temporalResolution = None
        spatialResolution = None
        for o in template.objects(name_of_constraint,self.PRIVVULN.feeds):
            if o in self.domain_supported_data_streams:
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

    def _find_template_name(self):
        privacyAttackName = ""
        try:
            #Only one transformation
            privacyAttackName = self.privacy_attack.value(predicate = self.RDF.type, object = self.PRIVVULN.PrivacyAttack , any = False, default="")
        except rdflib.exceptions.UniquenessError:
            return None
        return privacyAttackName

    def _find_output_for_template(self):
        model_temp = self.privacy_attack
        model_temp.parse(self.domain_path)

        model_temp.parse(self.base_ontology_path)

        # import pdb; pdb.set_trace()
        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT ?templateSubject ?outputSubject ?description ?privacyRiskScore ?privacyStrategy
                WHERE {
                    ?templateSubject rdf:type pv:PrivacyAttack .
                    ?templateSubject pv:creates ?outputSubject .
                    ?outputSubject rdf:type pv:PrivacyRisk .
                    OPTIONAL {
                         ?outputSubject pv2:description ?description .
                    } .
                    OPTIONAL {
                         ?outputSubject pv2:privacyRiskScore ?privacyRiskScore .
                    }
                    OPTIONAL {
                         ?outputSubject pv2:privacyStrategy ?privacyStrategy .
                    }

                }
                """,
                initNs = NSUtil.get_binding_namespaces()
                )
        ro = model_temp.query(q)
        privacyStrategies = []

        for row in ro:
            privacy_risk_score = 1
            if row[3] is not None:
                privacy_risk_score = row[3].value
            if row[4] is not None:
                privacyStrategies.append(row[4].value)
        if row is not None:
            return row[0], self.PRIVVULN.PrivacyRisk, row[1], row[2], privacy_risk_score, privacyStrategies