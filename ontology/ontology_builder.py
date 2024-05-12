from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import FOAF, OWL, RDF, RDFS, XSD
from util.util import MyUtil
import os


class Ontology:
    def __init__(self):
        self.g = Graph()
        self.ns = None
        self._namespace_bind()

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

    def add_triple(self, subject, predicate, obj):
        self.g.add((subject, predicate, obj))

    def set_namespace(self, namespace):
        self.ns = namespace

    def parse_ontology(self, rpath, rformat):
        self.g.parse(rpath, rformat)
        self.ns = Namespace(self.g.store.namespace(""))

    def build_ontology(self, path=os.path.join("data", "ontology")):
        util = MyUtil()
        clazz = util.parse_ontology(path, "CLASS")
        properties = util.parse_ontology(path, "PROPERTIES")
        for c in clazz:
            c_lst = c.split("#").reverse()
            self._create_class(*c_lst)
        for p in properties:
            p_lst = p.split("#")
            if len(p_lst) == 2:
                self._create_property(p_lst[1], OWL.DatatypeProperty, p_lst[0], XSD.string, OWL.topDataProperty)
            else:
                self._create_property(p_lst[1], OWL.ObjectProperty, p_lst[0], p_lst[2])

    def serialise(self, save_url=None, save_format=None, is_print=False):
        res = self.g.serialize(destination=save_url, format=save_format)
        if is_print:
            print(res)
