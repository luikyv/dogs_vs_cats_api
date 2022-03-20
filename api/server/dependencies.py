"""API Dependencies"""
from ..utils.image_classifier import ImageClassifier
from ..utils.image_classifier import TransferLearningModel

#################### Initialization ####################

transfer_learning_model: TransferLearningModel = TransferLearningModel()

image_classifier: ImageClassifier = ImageClassifier(prediction_model=transfer_learning_model)
