from classes.dataManager import DataManager;
from classes.model import MLModel;
import numpy as np;
from fastapi import FastAPI;
from pydantic import BaseModel;

# Using the DataManager Explorer

# data = DataManager.loadData("Data/News_Category_Dataset_v2.json");

# DataManager.exploreData(data);

# dataCleaned = DataManager.cleanRelativeData(data);

# DataManager.exploreMultivariateAnalysis(dataCleaned);

#--------------------------------------------------------------

train, test, y, categories, vocabulary, vectorize =  MLModel.setLearningData("Data/News_Category_Dataset_v2.json");
    
category_mapping = {index: category for index, category in enumerate(categories)}
    
model = MLModel.createModel(categories)
    
history = MLModel.trainModel(model, train, test, 10);

#History Graphic

# MLModel.historyLearning(history);

#--------------------------------------------------------------

#Evaluate the model

#MLModel.evaluateModel(model, test, category_mapping);

#---------------------------------------------------------------

class NewInformation(BaseModel):
    headLine: str
    shortDescription: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server is running!"}

@app.post("/predictCategory")
async def predictCategory(newInfo:NewInformation):

    info = newInfo.headLine + ";" + newInfo.shortDescription;

    prediction = MLModel.predictCategory(info, vectorize, model, category_mapping);

    return {"The predicted Category": prediction}
