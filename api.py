import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Api:
    def __init__(self):
        # Reading the CSV file, you can change the path to your CSV file by replacing 
        # "data/BX-Books.csv" to what ever you'd like.
        self.df = pd.read_csv("data/BX-Books.csv", on_bad_lines='skip', encoding="latin-1", sep=";")

        ## Cleaning the data
        self.df = self.df.drop_duplicates(subset="Book-Title")

        # Sample the data to make it more manageable
        sample_size = 15000
        self.df = self.df.sample(n=sample_size, replace=False, random_state=490)

        self.df = self.df.reset_index()
        self.df = self.df.drop('index',axis=1)

        # Clean text in the 'Book-Author' column
        self.df['Book-Author'] = self.df['Book-Author'].str.lower().str.replace(' ', '')

        # Clean text in the 'Book-Title' and 'Publisher' columns
        self.df['Book-Title'] = self.df['Book-Title'].str.lower()
        self.df['Publisher'] = self.df['Publisher'].str.lower()

        # Combine all relevant columns into one 'data' column
        self.df2 = self.df.drop(['ISBN','Image-URL-S','Image-URL-M','Image-URL-L','Year-Of-Publication'],axis=1)
        self.df2['data'] = self.df2[self.df2.columns[1:]].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)

        # Use CountVectorizer to create a vectorized representation of the 'data' column
        vectorizer = CountVectorizer()
        vectorized  = vectorizer.fit_transform(self.df2['data'])

        # Use cosine similarity to find the similarity between the books
        similarities = cosine_similarity(vectorized)

        # Create a dataframe from the similarities, with the book titles as the columns and index
        self.df = pd.DataFrame(similarities, columns=self.df['Book-Title'], index=self.df['Book-Title']).reset_index()

        # Find the top 10 most similar books to the input book
    def run(self, text):
        """A function used to run the AI, this is accessed via Main"""
        
        input_book = text
        recommendations = pd.DataFrame(self.df.nlargest(11,input_book)['Book-Title'])

        # Remove the input book from the recommendations
        recommendations = recommendations[recommendations['Book-Title']!=input_book]

        # Print the recommendations
        print("Top 10 book recommendations for '{}':".format(input_book))
        
        # Creating a empty list and storing all the recommendations in it, then return it.
        recommendations_list = []
        recommendations_list.append(recommendations)
        return recommendations_list
