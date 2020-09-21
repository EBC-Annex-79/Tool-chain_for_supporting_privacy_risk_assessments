class PrivacyRisk:
    def __init__(self, context, input_data_context, privacy_attack_name, privacy_risk_name, template_count,description):
        self.context = context
        self.input_data_context =input_data_context
        self.privacy_attack_name = privacy_attack_name
        self.privacy_risk_name = privacy_risk_name
        self.template_count = template_count
        self.description = description

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()