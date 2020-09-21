class Data:
    def __init__(self, domain_data_type, temporal_resolutions, spatial_resolutions = None, subject_name = None, template_name = None, template_count = 0, base_subject_name =None, description = None, context = None, context_subject= None):
        self.subject_name = subject_name
        self.template_name =template_name
        self.domain_data_type = domain_data_type
        self.temporal_resolutions = temporal_resolutions
        self.spatial_resolutions = spatial_resolutions
        self.template_count = template_count
        self.base_subject_name = base_subject_name
        self.description = description
        self.context = context
        self.context_subject = context_subject

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash(self.x)
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Data):
            return (
                self.subject_name == other.subject_name and
                self.template_name ==other.template_name and
                self.domain_data_type ==other.domain_data_type and
                self.temporal_resolutions ==other.temporal_resolutions and
                self.spatial_resolutions ==other.spatial_resolutions and
                self.template_count ==other.template_count and
                self.base_subject_name ==other.base_subject_name and
                self.description ==other.description and
                self.context ==other.context and
                self.context_subject ==other.context_subject
            )
        return False
    # def __repr__(self):
    #     return "Data obj. subject_name:%s domain_data_type:%s temporal_resolutions:%s spatial_resolutions:%s template_name:%s template_count:%s" % (self.subject_name if self.subject_name else "None", self.domain_data_type, self.temporal_resolutions, self.spatial_resolutions if self.spatial_resolutions else "None", self.template_name if self.template_count else "None", self.template_count)

    # def __str__(self):
    #     return self.__repr__()

