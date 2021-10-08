from ITemplate import ITransformation


# https://dl.acm.org/doi/pdf/10.1145/3309074.3309076

class SleepPattern(ITransformation):
    def _build_model(self):
        input1 = self.MODELS['inputRequirement1']
        self.graph.add((input1, self.RDF.type, self.PRIVVULNV2.Constraint))
        self.graph.add((input1, self.PRIVVULN.feeds, self.__DOMAINNAMESPACE__.Accelerometer))
