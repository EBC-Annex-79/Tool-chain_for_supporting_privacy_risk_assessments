from rdflib import Graph, Namespace, URIRef, Literal, exceptions
import rdflib
import rdflib.plugin
from Framework.Data.SpatialRelation import SpatialRelation
from Framework.Data.ResolutionForTransformation import ResolutionForTransformation
from Framework.Data.Data import Data
import Framework.namespace_util as NSUtil

class Transformation:
    def __init__(self,transformation, domain_path, base_ontology_path, extention_ontology_path, domain_supported_data_streams):
        self.domain_path = domain_path
        self.base_ontology_path =base_ontology_path
        self.extention_ontology_path = extention_ontology_path
        self.spatial_relations = None
        self.time_relations = None
        self.transformation = transformation
        self.model_requeued_data_types = None
        self.RDF  = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        self.PRIVVULN = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunl.ttl#')
        self.PRIVVULNV2 = Namespace('https://ontology.hviidnet.com/2020/01/03/privacyvunlV2.ttl#')
        self.domain_supported_data_streams = domain_supported_data_streams
        self.template_name = None
        self.template_output_subject = None
        self.template_output_data_type = None
        self.template_output_domain_data_type = None


    def get_template_output_subject(self):
        if self.template_output_subject is None:
            self.template_output_subject, self.template_output_data_type, self.template_output_domain_data_type =  self._find_output_for_template()
        return self.template_output_subject

    def get_template_template_output_data_type(self):
        if self.template_output_data_type is None:
            self.template_output_subject, self.template_output_data_type, self.template_output_domain_data_type =  self._find_output_for_template()
        return self.template_output_data_type

    def get_template_output_domain_data_type(self):
        if self.template_output_domain_data_type is None:
            self.template_output_subject, self.template_output_data_type, self.template_output_domain_data_type =  self._find_output_for_template()
        return self.template_output_domain_data_type

    def get_spatial_relations_for_transformation(self):
        if self.spatial_relations is None:
            self.spatial_relations = self._find_spatial_resolution_for_transformation()
        return self.spatial_relations

    def get_time_relations_for_transformation(self):
        if self.time_relations is None:
            self.time_relations = self._find_time_resolution_for_transformation()
        return self.time_relations

    def get_model_requeued_data_types(self):
        if self.model_requeued_data_types is None:
            self.model_requeued_data_types = self._find_data_types_for_template()
        return self.model_requeued_data_types

    def get_template_name(self):
        if self.template_name is None:
            self.template_name = self._find_template_name()
        return self.template_name

    def _find_spatial_resolution_for_transformation(self):
        transformation_temp = self.transformation
        transformation_temp.parse(self.domain_path)
        transformation_temp.parse(self.extention_ontology_path)

        transformation_temp.parse(self.base_ontology_path)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT   ?data ?transformationName ?input ?output
                WHERE {
                    ?dataTypes rdfs:subClassOf pv:Data .
                    ?data rdf:type ?dataTypes .
                    ?req pv:feeds ?data .
                    ?req rdf:type pv2:Constraint .
                    ?req pv:feeds ?transformationName .
                    ?transformationName rdf:type pv:Transformation .

                    ?srTypes rdf:type pv2:SpatialResolution .
                    ?srTypes pv2:spatialInput ?input .
                    ?srTypes pv2:spatialOutput ?output .
                    ?req pv:feeds ?srTypes
                }
                """
                ,
                initNs = NSUtil.get_binding_namespaces()
            )
        ro = transformation_temp.query(q) #, initBindings={'transformation': transformation_name}
        spatial_relations = {}

        for row in ro:
            if not row[0] in spatial_relations : spatial_relations[row[0]] = []
            spatial_relations[row[0]].append(SpatialRelation(row[0],row[1], row[2],row[3]))
        return spatial_relations

    def _find_time_resolution_for_transformation(self):
        transformation_temp = self.transformation
        transformation_temp.parse(self.domain_path)
        transformation_temp.parse(self.extention_ontology_path)

        transformation_temp.parse(self.base_ontology_path)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT   ?req ?data ?temporalResolution ?spatialResolution ?transformationName ?trTypes ?input ?output ?trName
                WHERE {
                    ?dataTypes rdfs:subClassOf pv:Data .
                    ?data rdf:type ?dataTypes .
                    ?req pv:feeds ?data .
                    ?req rdf:type pv2:Constraint .
                    ?req pv2:TemporalResolution ?temporalResolution .
                    # ?req pv2:SpatialResolution ?spatialResolution .
                    ?req pv:feeds ?transformationName .
                    ?transformationName rdf:type pv:Transformation .

                    ?trTypes rdfs:subClassOf pv2:TimeResolution .
                    ?trName rdf:type ?trTypes .
                    ?trName pv2:TimeInput ?input .
                    ?trName pv2:TimeOutput ?output .
                    ?req pv:feeds ?trName
                }
                """
                ,
                initNs = NSUtil.get_binding_namespaces()
            )
        ro = transformation_temp.query(q) #, initBindings={'transformation': transformation_name}
        dataTypes = []

        for row in ro:
            dataTypes.append(ResolutionForTransformation(row[0],row[1],float(row[2].value),row[3],row[4],row[5],float(row[6].value),float(row[7].value),row[8]))
        return dataTypes

    def _find_data_types_for_template(self):
        constraint_List = self._find_constraints_data_types_for_template(self.transformation)
        model_data_types = []
        for cName in constraint_List:
            data_type  = self._find_used_data_input_for_constraints(self.transformation,cName)
            if data_type.domain_data_type:
                model_data_types.append(data_type)
        return model_data_types

    def _find_constraints_data_types_for_template(self,template):
        constraint_List = []
        for s in template.subjects(self.RDF.type, self.PRIVVULNV2.Constraint):
            if (s,  self.PRIVVULN.feeds, self.get_template_name()) in template:
                constraint_List.append(s)
            else:
                print("Constraint element %s does not ref to the template model"%s, " in template %s"%self.template_name)
        return constraint_List

    def _find_used_data_input_for_constraints(self,template,name_of_constraint):
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
        transformationName = ""
        try:
            #Only one transformation
            transformationName = self.transformation.value(predicate = self.RDF.type, object = self.PRIVVULN.Transformation , any = False, default="")
        except rdflib.exceptions.UniquenessError:
            return None
        return transformationName

    def _find_output_for_template(self):
        model_temp = self.transformation
        model_temp.parse(self.domain_path)

        model_temp.parse(self.base_ontology_path)

        q = rdflib.plugins.sparql.prepareQuery("""
                SELECT ?outputSubject ?dataType ?outputDataType
                WHERE {
                    ?dataType rdfs:subClassOf pv:Data .
                    ?outputSubject rdf:type ?dataType .

                    ?transformationName rdf:type pv:Transformation .
                    ?transformationName pv:feeds ?outputSubject .
                    ?outputSubject rdf:type ?outputDataType .
                    ?outputDataType rdf:type ?dataType .
                }
                """,
                initNs = NSUtil.get_binding_namespaces())

        ro = model_temp.query(q)
        dataTypes = []

        for row in ro:
            return row[0], row[1], row[2]