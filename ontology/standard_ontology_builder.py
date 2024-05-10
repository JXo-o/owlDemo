from rdflib import Graph, Namespace
from rdflib.namespace import FOAF, OWL, RDF, RDFS, XSD
import os


class StandardOntology:
    def __init__(self):
        self.g = Graph()
        # 创建一个命名空间
        self.ns = Namespace("http://example.org/standards#")

    def create_ontology(self, save_url=os.path.join("owl", "ontology.owl"), save_format="xml"):
        self.__create_industry()
        self.__standard_onto_create()
        self.__obj_property_create()
        self.__class_disjoint()
        self._namespace_bind()
        self._serialise(save_url=save_url, save_format=save_format)
        print("标准规范本体已存至" + str(save_url))

    @staticmethod
    def merge_tbox_abox(t_path=os.path.join("owl", "ontology.owl"),
                        a_path=os.path.join("owl", "data.owl"),
                        o_path=os.path.join("owl", "final.owl"),
                        rformat="xml"):
        tbox = Graph()
        tbox.parse(t_path, rformat)
        abox = Graph()
        abox.parse(a_path, rformat)
        kg = tbox + abox
        kg.serialize(o_path, rformat)
        print("融合本体和数据后的图谱已存至" + str(o_path))

    def _insert_property(self, key, key_type, key_domain, key_range, parent=OWL.topObjectProperty):
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

    def __create_industry(self):
        # 创建标准规范相关的顶层基类
        standard_relevant = self.ns.StandardRelevant
        self.g.add((standard_relevant, RDF.type, OWL.Class))
        # 所有的顶层基类都应该归属于Thing
        self.g.add((standard_relevant, RDFS.subClassOf, OWL.Thing))

    def __standard_onto_create(self):
        # 如果不认为自己创建的类全部属于一个基类下，可以创建其他类做替代，StandardRelevant属于Thing
        # 创建Component类，即构件类
        component = self.ns.Component
        self.g.add((component, RDF.type, OWL.Class))
        self.g.add((component, RDFS.subClassOf, self.ns.StandardRelevant))

        # 创建Property类，即属性类
        m_property = self.ns.Property
        self.g.add((m_property, RDF.type, OWL.Class))
        self.g.add((m_property, RDFS.subClassOf, self.ns.StandardRelevant))

        # 创建Constraint类，即约束关系类
        constraint = self.ns.Constraint
        self.g.add((constraint, RDF.type, OWL.Class))
        self.g.add((constraint, RDFS.subClassOf, self.ns.StandardRelevant))

        # 创建NumericalConstraint类，即数值约束关系类
        numerical_constraint = self.ns.NumericalConstraint
        self.g.add((numerical_constraint, RDF.type, OWL.Class))
        self.g.add((numerical_constraint, RDFS.subClassOf, self.ns.Constraint))
        threshold = self.ns.threshold
        self._insert_property(threshold, OWL.DatatypeProperty, numerical_constraint, XSD.string, OWL.topDataProperty)

        # 创建SpatialConstraint类，即空间约束关系类
        spatial_constraint = self.ns.SpatialConstraint
        self.g.add((spatial_constraint, RDF.type, OWL.Class))
        self.g.add((spatial_constraint, RDFS.subClassOf, self.ns.Constraint))

    def __obj_property_create(self):
        # 创建hasProperty关系
        has_property = self.ns.hasProperty
        self._insert_property(has_property, OWL.ObjectProperty, self.ns.Component, self.ns.Property)

        # 创建btoComponent关系
        belong_to_component = self.ns.btoComponent
        self._insert_property(belong_to_component, OWL.ObjectProperty, self.ns.Property, self.ns.Component)

        # 添加反转属性
        self.g.add((has_property, OWL.inverseOf, belong_to_component))

        # 创建hasThreshold关系
        has_threshold = self.ns.hasThreshold
        self._insert_property(has_threshold, OWL.ObjectProperty, self.ns.SpatialConstraint, self.ns.Component)

        # 创建meetsNumericConstraint关系
        meets_num_constraint = self.ns.meetsNumericConstraint
        self._insert_property(meets_num_constraint, OWL.ObjectProperty, self.ns.Property, self.ns.NumericalConstraint)

        # 创建meetsSpatialConstraint关系
        meets_spa_constraint = self.ns.meetsSpatialConstraint
        self._insert_property(meets_spa_constraint, OWL.ObjectProperty, self.ns.Component, self.ns.SpatialConstraint)

    def __class_disjoint(self):
        # 创建类之间的互斥关系
        self.g.add((self.ns.Component, OWL.disjointWith, self.ns.Property))
        self.g.add((self.ns.Component, OWL.disjointWith, self.ns.Constraint))
        self.g.add((self.ns.Property, OWL.disjointWith, self.ns.Constraint))
        self.g.add((self.ns.NumericalConstraint, OWL.disjointWith, self.ns.SpatialConstraint))
