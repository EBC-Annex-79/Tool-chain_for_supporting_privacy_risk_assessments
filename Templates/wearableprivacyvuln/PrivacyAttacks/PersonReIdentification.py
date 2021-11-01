from rdflib import Namespace
from rdflib.term import Literal

from ITemplate import IPrivacyAttack

# https://arxiv.org/abs/2106.11900
class PersonReIdentification(IPrivacyAttack):

    def __init__(self):
