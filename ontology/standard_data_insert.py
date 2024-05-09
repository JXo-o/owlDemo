from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import FOAF, OWL, RDF, RDFS, XSD
import os


class StandardDataInsert:
    def __init__(self):
        self.g = Graph()
        # 创建一个命名空间
        self.ns = Namespace("http://example.org/standards#")

    def _namespace_bind(self):
        self.g.bind("owl", OWL)
        self.g.bind("xsd", XSD)
        self.g.bind("rdf", RDF)
        self.g.bind("rdfs", RDFS)
        self.g.bind("foaf", FOAF)
        self.g.bind("", self.ns)

    def _serialise(self, save_url=None, is_print=False, save_format="xml"):
        res = self.g.serialize(destination=save_url, format=save_format)
        if is_print:
            print(res)

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
        self._insert_instance(self.ns.Component, label[0])
        self._insert_instance(self.ns.Property, label[1])
        self._insert_instance(self.ns.NumericalConstraint, label[2], label[3])
        self._insert_property(label[0], label[1], self.ns.hasProperty)
        self._insert_property(label[1], label[0], self.ns.btoComponent)
        self._insert_property(label[1], label[2], self.ns.meetsNumericConstraint)

    # 保存图谱abox
    def save_file(self, save_url=os.path.join("owl", "data.owl"), save_format="xml"):
        self._namespace_bind()
        self._serialise(save_url=save_url, save_format=save_format)
        print("图谱abox数据部分已存至" + str(save_url))

    def test(self, save_url=os.path.join("owl", "data.owl"), save_format="xml"):
        self.insert_data(["泄水孔", "直径", "不小于", "50mm"])
        self.save_file(save_url, save_format)
