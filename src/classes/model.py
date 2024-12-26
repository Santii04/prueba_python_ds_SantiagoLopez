from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf;
from tensorflow import keras;
from classes.dataManager import DataManager;
import numpy as np;
import matplotlib.pyplot as mplt;
import seaborn as sbn;

class MLModel:

    def setLearningData(file):
        """Load the data file, vectorize the information and set the training and test data

        Args:
            file (str): The path to the data file

        Returns:
            train_dataset: TF dataset for the selected train data
            test_dataset: TF dataset for the selected test data
            binary_categories: The values of the categories in binary format
            categories: The values of the categories in str
            vocabulary: The vocabulary learned by the vectorizer
            vectorize: The vectorizer generated by the DataManager with the configuration defined
        """
        
        data = DataManager.loadData(file);
            
        dataCleaned = DataManager.cleanRelativeData(data);
        
        x, binary_categories, categories, vocabulary, vectorize = DataManager.vectorizeText(dataCleaned);
    
        dataset = tf.data.Dataset.from_tensor_slices((x, binary_categories))

        # Shuffle the information for an random order
        dataset = dataset.shuffle(buffer_size=10000)

        # Split on train and test data (80% - 20%)
        train_size = int(0.8 * len(data))  # 80% for training
        train_dataset = dataset.take(train_size)
        test_dataset = dataset.skip(train_size)

        # Make batches for optimize the training
        batch_size = 32
        train_dataset = train_dataset.batch(batch_size).prefetch(buffer_size=tf.data.AUTOTUNE)
        test_dataset = test_dataset.batch(batch_size).prefetch(buffer_size=tf.data.AUTOTUNE)

        return train_dataset, test_dataset, binary_categories, categories, vocabulary, vectorize
        
    def createModel(categories):
        
        """Construct the convulational based model

        Returns:
            model: The model to be trained
        """
        
        max_features = 15000
        sequence_length = 50
        
        model = keras.Sequential();
        
        # Embedding Layer
        model.add(keras.layers.Embedding(input_dim=max_features, output_dim=128, input_length=sequence_length))

        # Convolutional Layers
        model.add(keras.layers.Conv1D(filters=128, kernel_size=3, activation='relu'))
        model.add(keras.layers.MaxPooling1D(pool_size=2))

        model.add(keras.layers.Conv1D(filters=128, kernel_size=3, activation='relu'))
        model.add(keras.layers.MaxPooling1D(pool_size=2))

        # Flatten layer
        model.add(keras.layers.Flatten())

        # Fully Connected Layer
        model.add(keras.layers.Dense(128, activation='relu'))
        model.add(keras.layers.Dropout(0.5))  # Regularization for the adjust

        # Output Layer
        model.add(keras.layers.Dense(len(categories), activation='softmax'))  # Amount of categories like output

        # Compilation
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        return model
    
    def trainModel(model, train_data, test_data, epochs):
        """Train a given model using the train and test data, and defining the number of epochs

        Args:
            model (keras model): The model to be trained
            train_data (TF dataset): the training information
            test_data (TF dataset): The testing information
            epochs (number): The number of epochs

        Returns:
            history: The history of the training
        """
        
        history = model.fit(
            train_data,
            validation_data=test_data,
            epochs=epochs)
        
        return history;
    
    def evaluateModel(model, test_data):
        
        """Evaluate a model based in a testing data given
        
        Args:
            model
            test_data

        Returns:
            test_loss: The loss value
            test_accuracy: The accuracy value
        """
        
        test_loss, test_accuracy = model.evaluate(test_data);
        
        return test_loss, test_accuracy
    
    def predictCategory(text, vectorizer, model, category_mapping):
        
        """Get a model predict for a text given
        
        Args:
            text: The text to been predicted
            vectorizer: The same vectorizer used for the train data vectorization
            model: The model that predict
            category_mapping: A map of the possible categories to be given by the model

        Returns:
            The category predicted by the model
        """
        
        # Clean the given text
        cleaned_text = DataManager.cleanText(text)

        # Set the text like a one element list
        text_list = [cleaned_text]
        
        # Vectorize the text given (like a list)
        text_vectorized = vectorizer(text_list)
        
        # Make the prediction
        prediction = model.predict(text_vectorized)
        
        # Get the most viable category (with better possibilities)
        predicted_category_idx = np.argmax(prediction)
        
        # Get the predicted category using the category mapping given
        predicted_category = category_mapping[predicted_category_idx]
        
        return predicted_category

    def evaluateModel(model, test_data, category_mapping):
        """
        Evaluate the model on the test data using classification metrics
        and visualize the confusion matrix.

        Args:
            model: The trained model.
            test_data: The TF dataset with the test data.
            category_mapping: A dictionary that maps indices to category names.
        """
        true_labels = []
        predictions = []
    
        for x_batch, y_batch in test_data:
            true_labels.extend(np.argmax(y_batch, axis=1))  # Get the real tags
            pred_batch = model.predict(x_batch)  # Model predictions
            pred_labels = np.argmax(pred_batch, axis=1)  # Select the class with the better probability
            predictions.extend(pred_labels)
    
        true_labels = np.array(true_labels)
        predictions = np.array(predictions)

        unique_categories = np.unique(true_labels)
        
        predicted_categories = [category_mapping[idx] for idx in predictions]
        true_categories = [category_mapping[idx] for idx in true_labels]

        # Generate the classification_report (precisión, recall, F1-score)
        print("Classification Report:\n")
        print(classification_report(true_labels, predictions, target_names=[category_mapping[idx] for idx in unique_categories], labels=unique_categories))

        # Generate the confussion matrix
        cm = confusion_matrix(true_labels, predictions)
    
        mplt.figure(figsize=(10, 8))
        sbn.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=category_mapping.values(), yticklabels=category_mapping.values())
        mplt.title("Confusion Matrix")
        mplt.xlabel("Predicted Category")
        mplt.ylabel("True Category")
        mplt.savefig("docs/graphs/model_evaluation.png")  # Save the graphic
        mplt.close()  # Close the figure

    def historyLearning(history):
        """Generate a graphic for the learning history of the model trained (loss based)

        Args:
            History of the model learning
        """
        mplt.figure(figsize=(10,8))
        mplt.title("Learning Historial")
        mplt.xlabel("# Epoch")
        mplt.ylabel("Loss magnitude")
        mplt.plot(history.history["loss"])
        mplt.savefig("docs/graphs/history_learning.png")
        mplt.close()