class ContextInput:
    def __init__(self, domain_class_type, subject, super_domain_class_type, super_subject):
        self.domain_class_type =domain_class_type
        self.subject = subject
        self.super_domain_class_type = super_domain_class_type
        self.super_subject = super_subject

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()