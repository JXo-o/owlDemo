from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import FOAF, OWL, RDF, RDFS, XSD
from util.util import MyUtil
import os


class Ontology:

    def __init__(self):

        self.g = Graph()
        self.ns = None
        self._namespace_bind()

    def _create_class(self, c_name, parent=OWL.Thing):

        c_name = self._wrap_str(c_name)
        parent = self._wrap_str(parent)
        self.g.add((c_name, RDF.type, OWL.Class))
        self.g.add((c_name, RDFS.subClassOf, parent))

    def _create_property(self, key, key_type, key_domain, key_range, parent=OWL.topObjectProperty):

        key = self._wrap_str(key)
        key_type = self._wrap_str(key_type)
        key_domain = self._wrap_str(key_domain)
        key_range = self._wrap_str(key_range)
        parent = self._wrap_str(parent)

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

    def _wrap_str(self, key):

        if not key.startswith("http://"):
            key = URIRef(self.ns + key)
        return key

    def add_triple(self, subject, predicate, obj):

        subject = self._wrap_str(subject)
        predicate = self._wrap_str(predicate)
        obj = self._wrap_str(obj)

        self.g.add((subject, predicate, obj))

    def set_namespace(self, namespace):

        self.ns = namespace

    def parse_ontology(self, rpath, rformat):

        self.g.parse(rpath, rformat)
        self.ns = Namespace(self.g.store.namespace(""))

    def build_ontology(self, path=os.path.join("data", "ontology")):

        util = MyUtil()
        ns = util.parse_ontology(path, "NAMESPACE")
        clazz = util.parse_ontology(path, "CLASS")
        properties = util.parse_ontology(path, "PROPERTIES")
        self.set_namespace(ns[0])

        for c in clazz:
            c_lst = c.split("#")[::-1]
            print(c_lst)
            self._create_class(*c_lst)

        for p in properties:
            p_lst = p.split("#")
            print(p_lst)
            if len(p_lst) == 2:
                self._create_property(p_lst[1], OWL.DatatypeProperty, p_lst[0], XSD.string, OWL.topDataProperty)
            else:
                self._create_property(p_lst[1], OWL.ObjectProperty, p_lst[0], p_lst[2])

    def get_ns(self):
        return self.ns

    def get_kg(self):
        return self.g

    @staticmethod
    def merge_kg(*paths, rformat="xml"):

        kg = Graph()
        for path in paths:
            kg += Graph().parse(path, rformat)

        return kg

    @staticmethod
    def serialise(kg, save_url=None, save_format=None, is_print=False):

        res = kg.serialize(destination=save_url, format=save_format)
        if is_print:
            print(res)
