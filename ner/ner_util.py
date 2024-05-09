from ner.ner_trainer import NERTrainer
import spacy
import os


class NERUtil:
    def __init__(self):
        self.nlp = None
        self.doc = None

    def train_model(self, data_path=os.path.join("data", "train_data.json"),
                    model_path=os.path.join("model", "model_1")):
        if not os.path.exists(model_path):
            trainer = NERTrainer(data_path, model_path)
            trainer.train_model()
        self.nlp = spacy.load(model_path)

    def process_sentence(self, sentence):
        self.doc = self.nlp(sentence)
        return self.doc

    def get_entities(self, label):
        if self.doc is None:
            raise ValueError("No document processed yet. Call process_sentence() first.")

        for ent in self.doc.ents:
            if ent.label_ == label:
                return ent.text
        return "nil"
