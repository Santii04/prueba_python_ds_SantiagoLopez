import pandas as pd;
import matplotlib.pyplot as mplt;
import seaborn as sbn;
import re;
from tensorflow.keras.layers import TextVectorization;

class DataManager:

    def loadData(filePath: str):
        """
        Load data from a file (or get Nonen if the file does not exist)
        Args:
            filePath (string): Path to the file

        Returns:
            data: The file content
            None (If the file does not exist)
        """
        try:
            data = pd.read_json(filePath, lines=True);
            return data;
        except Exception as e:
            print("An error was ocurred during the file loading: ", e);
            return None;

    def exploreData(data):
        """Do a data exploration focused on the news categorization

        Args:
            data (pandas dataFrame readed): The data to be explored
        """
        print("Data Resume:\n");
        print(data.info);
        print("First Rows: \n");
        print(data.head());
        print("Last Rows: \n");
        print(data.tail());

        print("Categories Distribution: \n");
        print(data['category'].value_counts());

        mplt.figure(figsize=(10, 6));
        sbn.countplot(data=data, y='category', order=data['category'].value_counts().index);
        mplt.title("Categories Distribution");
        mplt.xlabel("# News");
        mplt.ylabel("Category");
        mplt.savefig("docs/graphs/category_distribution.png")  # Save the graphic
        mplt.close()  # Close the figure

    def exploreMultivariateAnalysis(data):

        """Do a data exploration focused on the relation betwwen the headline lenght and the categories, and the short_description length and the categories

        Args:
            data (pandas dataFrame readed): The data to be explored
        """
        
        mplt.figure(figsize=(12, 8))
        sbn.boxplot(x='category', y='headline_clean', data=data)
        mplt.title('Distribution of Headline Length by Category')
        mplt.xlabel('Category')
        mplt.ylabel('Headline Length')
        mplt.xticks(rotation=45)
        mplt.savefig("docs/graphs/category_headline_distribution.png")  # Save the graphic
        mplt.close()  # Close the figure

        mplt.figure(figsize=(12, 8))
        sbn.boxplot(x='category', y='short_description_clean', data=data)
        mplt.title('Distribution of Short Description Length by Category')
        mplt.xlabel('Category')
        mplt.ylabel('Short Description Length')
        mplt.xticks(rotation=45)
        mplt.savefig("docs/graphs/category_description_distribution.png")  # Save the graphic
        mplt.close()  # Close the figure

        
    #Exportable function
    def cleanText(text: str):
            """Clean a text, deleting not wanted chars

            Args:
                text (string): The string to be cleaned

            Returns:
                string: The text cleaned
            """
            text = text.lower();
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text);
            return text;

    def cleanRelativeData(data):
        """Using apply. clean the relative columns for this data analysis

        Args:
            data (pandas dataFrame readed):The dataframe to be clean

        Returns:
            dataFrame: The dataFrame with new columns for the cleaned data
        """
        #Local Function
        def cleanText(text: str):
            """Clean a text, deleting not wanted chars

            Args:
                text (string): The string to be cleaned

            Returns:
                string: The text cleaned
            """
            text = text.lower();
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text);
            return text;
        
        
        data['headline_clean'] = data['headline'].apply(cleanText);
        data['short_description_clean'] = data['short_description'].apply(cleanText);
        data['combinedInfo'] = data['headline_clean'] + ";" + data['short_description_clean'];
        return data;

    def vectorizeText(data):
        
        """Construct a vectorizer and converts the data strings in numbers ascii based

        Returns:
            x: The important data vectorized
            y: The possible categories in binary
            categories: The possible categories in an array for post data management
            vocabulary: Summary of the words learned by the vectorizer
            vectorize: The vectorizer with the configuration defined
        """
        max_features = 15000
        sequence_length = 50
        
        vectorize = TextVectorization(
            max_tokens = max_features,
            output_mode = 'int',
            output_sequence_length = sequence_length
        )
        
        texts = data['combinedInfo'].tolist()
        vectorize.adapt(texts)
        
        x = vectorize(texts)
        y = pd.get_dummies(data['category']).values
        categories = pd.get_dummies(data['category']).columns
        
        return x,y, categories, vectorize.get_vocabulary(), vectorize
    
    