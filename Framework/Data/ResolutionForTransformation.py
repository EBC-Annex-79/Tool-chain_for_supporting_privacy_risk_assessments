class ResolutionForTransformation:
    def __init__(self, constraint_subject, domain_data_type, input_temporal_resolution, input_spatial_resolution, transformation_name, time_resolution_type, time_resolution_input, time_resolution_output, time_resolution_name ):
        self.constraint_subject = constraint_subject
        self.domain_data_type = domain_data_type
        self.input_temporal_resolution = input_temporal_resolution
        self.input_spatial_resolution = input_spatial_resolution
        self.transformation_name = transformation_name
        self.time_resolution_type = time_resolution_type
        self.time_resolution_input = time_resolution_input
        self.time_resolution_output = time_resolution_output
        self.time_resolution_name = time_resolution_name

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()