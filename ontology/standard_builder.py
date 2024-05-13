from rdflib.namespace import OWL
from ontology.ontology_builder import Ontology
import os


class StandardOntology:

    @staticmethod
    def merge_tbox_abox(t_path=os.path.join("owl", "ontology.owl"),
                        a_path=os.path.join("owl", "data.owl"),
                        o_path=os.path.join("owl", "final.owl"),
                        rformat="xml"):

        Ontology.merge_kg(t_path, a_path).serialize(o_path, rformat)
        print("融合本体和数据后的图谱已存至" + str(o_path))

    @staticmethod
    def build_logic(save_url=os.path.join("owl", "ontology.owl"), save_format="xml"):
        ontology_builder = Ontology()
        ontology_builder.build_ontology()

        # ontology_builder.add_triple("Component", OWL.disjointWith, "Property")
        # ontology_builder.add_triple("Component", OWL.disjointWith, "Constraint")
        # ontology_builder.add_triple("Property", OWL.disjointWith, "Constraint")
        # ontology_builder.add_triple("NumericalConstraint", OWL.disjointWith, "SpatialConstraint")

        ontology_builder.add_triple("hasProperty", OWL.inverseOf, "btoComponent")
        Ontology.serialise(ontology_builder.get_kg(), save_url, save_format)
        print("标准规范本体已存至" + str(save_url))
