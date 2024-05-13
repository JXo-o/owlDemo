from util.util import MyUtil
from ner.ner_util import NERUtil
from ontology.data_insert import DataInsert
from ontology.standard_builder import StandardOntology
from ontology.convert_to_rule import ConvertToRule


def main():
    # 命名实体识别部分，示例
    ner_util = NERUtil()
    ner_util.train_model()
    label_list = MyUtil.correct_labels(MyUtil.print_label(ner_util))

    # 标准规范本体生成，示例
    ontology = StandardOntology()
    ontology.build_logic()

    # 知识图谱abox生成，示例
    data_insert = DataInsert()
    for element in label_list:
        data_insert.insert_data(element)
    data_insert.save_file()

    # 本体与数据融合部分，示例
    StandardOntology.merge_tbox_abox()

    # 知识图谱转Jena规则
    ConvertToRule.convert()


def main1():
    # 标准规范本体生成，示例
    ontology = StandardOntology()
    ontology.build_logic()


if __name__ == "__main__":
    main1()
