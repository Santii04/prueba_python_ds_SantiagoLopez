import pandas as pd;
import matplotlib as mplt;
import seaborn as sbn;
import re;

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

        mplt.figure(figSize=(10, 6));
        sbn.countplot(data=data, y='category', order=data['category'].value_counts().index);
        mplt.title("Categories Distribution");
        mplt.xlabel("# News");
        mplt.ylabel("Category");
        mplt.show();

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
        data['headline_clean'] = data['headline'].apply(cleanText);
        data['short_description_clean'] = data['short_description'].apply(cleanText);
        data['combinedInfo'] = data['headline_clean'] + ";" + data['short_description_clean'];
        return data;
