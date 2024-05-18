from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import FOAF, OWL, RDF, RDFS, XSD
from utility_scripts.util import MyUtil
import os


class DataInsert:
    def __init__(self):

        self.g = Graph().parse(source=os.path.join("owl", "standard_ontology.owl"), format="xml")
        self.ns = Namespace(MyUtil.parse_ontology(os.path.join("input_data", "standard_ontology"), "NAMESPACE")[0])
        self.output_path = os.path.join("owl", "standard.owl")
        self.output_format = "xml"

    # 插入不同类实例
    def _insert_instance(self, key, instance, data=None):
        ins = URIRef(self.ns + instance)
        self.g.add((ins, RDF.type, key))
        if data:
            self.g.add((ins, self.ns.threshold, Literal(data)))

    #
    # # 插入hasProperty、btoComponent关系
    # def _insert_has_property(self, component, m_property):
    #     key = URIRef(self.ns + component)
    #     value = URIRef(self.ns + m_property)
    #     self.g.add((key, self.ns.hasProperty, value))
    #     self.g.add((value, self.ns.btoComponent, key))
    #
    # # 插入hasThreshold关系
    # def _insert_has_threshold(self, spatial, component):
    #     key = URIRef(self.ns + spatial)
    #     value = URIRef(self.ns + component)
    #     self.g.add((key, self.ns.hasThreshold, value))
    #
    # # 插入meetsNumericConstraint关系
    # def _insert_meets_num_constraint(self, component, numerical):
    #     key = URIRef(self.ns + component)
    #     value = URIRef(self.ns + numerical)
    #     self.g.add((key, self.ns.meetsNumericConstraint, value))
    #
    # # 插入meetsSpatialConstraint关系
    # def _insert_meets_spa_constraint(self, component, spatial):
    #     key = URIRef(self.ns + component)
    #     value = URIRef(self.ns + spatial)
    #     self.g.add((key, self.ns.meetsSpatialConstraint, value))

    # 插入关系
    def _insert_property(self, k, v, p):
        key = URIRef(self.ns + k)
        value = URIRef(self.ns + v)
        self.g.add((key, p, value))

    # 以列表形式插入数据
    def insert_data(self, label):
        print(label)
        self._insert_instance(self.ns.Component, label[0])
        self._insert_instance(self.ns.Property, label[1])
        self._insert_instance(self.ns.NumericalConstraint, label[2], label[3])
        self._insert_property(label[0], label[1], self.ns.hasProperty)
        self._insert_property(label[1], label[0], self.ns.btoComponent)
        self._insert_property(label[1], label[2], self.ns.meetsNumericConstraint)

    # 保存图谱abox
    def save_file(self):
        self.g.bind("", self.ns)
        self.g.serialize(destination=self.output_path, format=self.output_format)
        print("标准规范图谱已存至" + str(self.output_path))

    def test(self):
        self.insert_data(["泄水孔", "直径", "不小于", "50mm"])
        self.save_file()
