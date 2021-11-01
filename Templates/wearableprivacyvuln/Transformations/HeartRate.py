
from Templates.ITemplate import ITransformation
from rdflib import Graph, Namespace, URIRef, Literal

# https://arxiv.org/abs/2106.11900
class HeartRate(ITransformation):

    def __init__(self):
