from classes.dataManager import DataManager;
from classes.model import MLModel;
import numpy as np;

if __name__ == "__main__":
    
    ##Testing
    
    train, test, y, categories, vocabulary, vectorize =  MLModel.setLearningData("Data/News_Category_Dataset_v2.json");
    
    category_mapping = {index: category for index, category in enumerate(categories)}
    
    model = MLModel.createModel()
    
    history = MLModel.trainModel(model, train, test, 10);
    
    test_text = "The latest tech developments in AI are changing industries across the globe."
    
    prediction = MLModel.predictCategory(test_text, vectorize, model, category_mapping)
    
    print("Prediction: ", prediction)