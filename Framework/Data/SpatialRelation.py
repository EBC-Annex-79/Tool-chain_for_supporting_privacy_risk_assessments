class SpatialRelation:
    def __init__(self, domain_data_type, transformation_name,input_spatial_resolution, output_spatial_resolution):
        self.domain_data_type = domain_data_type
        self.transformation_name = transformation_name
        self.input_spatial_resolution = input_spatial_resolution
        self.output_spatial_resolution = output_spatial_resolution

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()