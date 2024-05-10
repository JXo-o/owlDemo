from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import FOAF, OWL, RDF, RDFS, XSD
import os


class Ontology:
    def __init__(self, url=None, rformat="xml", namespace=""):
        self.g = Graph()
        self.g.parse(url, rformat) if url else None
        self.ns = Namespace(self.g.store.namespace(namespace) if namespace else namespace)

    def _create_class(self, c_name, parent=OWL.Thing):
        cname = URIRef(self.ns + c_name)
        self.g.add((cname, RDF.type, OWL.Class))
        self.g.add((cname, RDFS.subClassOf, parent))

    def _create_property(self, key, key_type, key_domain, key_range, parent=OWL.topObjectProperty):
        self.g.add((key, RDF.type, key_type))
        self.g.add((key, RDFS.domain, key_domain))
        self.g.add((key, RDFS.range, key_range))
        self.g.add((key, RDFS.subPropertyOf, parent))

    def _namespace_bind(self):
        self.g.bind("owl", OWL)
        self.g.bind("xsd", XSD)
        self.g.bind("rdf", RDF)
        self.g.bind("rdfs", RDFS)
        self.g.bind("foaf", FOAF)
        self.g.bind("", self.ns)

    def _serialise(self, save_url=None, save_format=None, is_print=False):
        res = self.g.serialize(destination=save_url, format=save_format)
        if is_print:
            print(res)

    def add_triple(self, subject, predicate, obj):
        self.g.add((subject, predicate, obj))