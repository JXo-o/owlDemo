from util.util import MyUtil
from ner.ner_util import NERUtil
from ontology.data_insert import DataInsert
from ontology.standard_builder import StandardOntology
from ontology.convert_to_rule import ConvertToRule
from ontology.bridge_builder import BridgeBuilder
from ontology.ontology_builder import Ontology
from ifc.kg_completer import KnowledgeGraphCompleter
from rdflib import Namespace
import os


def main():
    # 命名实体识别部分，示例
    ner_util = NERUtil()
    ner_util.train_model()
    label_list = MyUtil.correct_labels(
        MyUtil.print_label(
            ner_util,
            os.path.join("data", "ner_label")
        )
    )

    # 标准规范本体生成，示例
    StandardOntology(
        os.path.join("data", "standard_ontology"),
        os.path.join("owl", "standard_ontology.owl")
    ).build_logic()

    # 桥梁本体生成，示例
    BridgeBuilder(
        os.path.join("data", "bridge_ontology"),
        os.path.join("owl", "bridge_ontology.owl")
    ).build_logic()

    # 知识图谱数据插入，示例
    data_insert = DataInsert()
    for element in label_list:
        data_insert.insert_data(element)
    data_insert.save_file()

    # 本体与数据融合部分，示例
    # kg = Ontology.merge_kg(
    #     os.path.join("owl", "standard_ontology.owl"),
    #     os.path.join("owl", "standard_data.owl"),
    #     namespace=Namespace(
    #         MyUtil.parse_ontology(
    #             os.path.join("data", "standard_ontology"),
    #             "NAMESPACE"
    #         )[0]
    #     )
    # )
    # Ontology.serialise(kg, os.path.join("owl", "standard_final.owl"), "xml")

    # 解析IFC，在桥梁图谱中添加数据
    KnowledgeGraphCompleter(
        os.path.join("model", "railing_test.ifc"),
        os.path.join("owl", "bridge_ontology.owl")
    ).data_insert().save_file(
        os.path.join("owl", "bridge.owl"),
        "xml"
    )

    # 知识图谱转Jena规则
    ConvertToRule.convert(
        os.path.join("owl", "standard.owl")
    )


if __name__ == "__main__":
    main()
