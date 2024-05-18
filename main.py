#!/usr/bin/env python3
import pandas as pd
from typing import Dict, List
import os
import re
from collections import Counter
import sqlite3
from sqlite3 import Connection
import json

class WordFrequencyCounter:
    """ Class to count the word frequency"""

    @staticmethod
    def split_string(input_string:str) -> List[str]:
        """
        This function will accept the string and split it into three fields such as 'id', 'source', 'original_text'

        @@params input_string: The string to be splitted into three fields.
        """
        # Each field in the string are separated by ',\s“'. Based on this pattern, split the sentences.
        parts = re.split(r',\s“', input_string)

        # Strip any remaining “” characters in the string 
        cleaned_parts = [part.strip().strip('“”') for part in parts]
        return cleaned_parts
    
    @staticmethod
    def read_multiline_csv(file_path:str) -> List[List[str]]:
        """
        This function will accept the file, read line by line, make sure all the fields in the csv
        file are represented without any discrepancies. This is to prevent the csv files that are not correctly formatted.
        """
        records = [] # to store all parsed records
        current_record = None #current working record

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip() # remove leading/trailing whitespace

                # check if the lines are starting with numeric characters followed by commas
                if line and ',' in line:
                    first_field = line.split(',')[0]  #get the first set of characters before the comma

                    # check using regex if first field is just digits and the previous record ended with '”'
                    if re.match(r'^\d+$', first_field) is not None and (not current_record or re.search(r'.”$', current_record) is not None):
                        # start a new record
                        if current_record is not None: 
                            records.append(current_record) # append the completed record
                        current_record = line #start a new record
                    else:
                        # continuation of the last field in the current record
                        if current_record:
                            current_record += " " + line # add the line to the last field
                else:
                    # handle case where there's no coma in the line
                    if current_record:
                        current_record += " " + line # continue appending to the current record

            if current_record: # append the last record
                records.append(current_record)
                
        # apply split string function to clean out remaining smart quotes
        records = [WordFrequencyCounter.split_string(item) for item in records]
        return records

    @staticmethod
    def sentence_cleaner(sentence:str) -> List[str]:
        """
        This function will remove any emojis, numbers in the integer/float format, convert into lowercases.

        @@params sentence: the sentence to be cleaned.
        """
        COMMON_WORDS = {
            'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 
            'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can\'t', 'cannot', 
            'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during', 'each', 
            'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 
            'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 
            'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it', 'it\'s', 'its', 
            'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 
            'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shan\'t', 
            'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 
            'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 
            'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 
            'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 
            'when\'s', 'where', 'where\'s', 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 
            'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 
            'yourselves'
        }

        # remove the numbers 
        sentence = re.sub(r'\b\d+\.\d+\b\.?|\b\d+\b\.?', '', sentence)

        # remove the emojis  -> THIS NEEDS TESTING
        sentence = re.sub(r'[^\w\s,]', '', sentence)

        # convert it into lower cases split
        sentence = sentence.lower().split()

        # filter out common words
        common_words = [word.lower() for word in COMMON_WORDS]
        words = [word for word in sentence if word not in common_words]

        return words
    
    @staticmethod
    def word_freq_counter(words:List[str]) -> Dict[str, int]:
        """
        This function will count the word occurences in the given list of words.

        @@params words:  list of words to be counted.
        """

        # Instantiate the counter object from the collections library
        word_counts = Counter()

        # update the counter and convert it into json object
        word_counts.update(words)
        word_counts = json.dumps(dict(word_counts))
        return word_counts
    
    @staticmethod
    def move_file(source_path:str,
                  destination_path:str) -> None:
        """
        Moves the file from source to destination folder

        @@params source_path: The source path for the file.
        @@params destination_path: The destination where the file to be moved.
        """
        # Get the destintion directory
        destination_dir = os.path.dirname(destination_path)

        # Create the directory if it does not exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # move the file to the destination path
        os.rename(source_path, destination_path)
    
    @staticmethod
    def connect_db(db_name:str,
                   table_name:str) -> Connection:
        """
        Method to connect to the database and to the table.

        @@params db_name: The name of the database.
        @@params table_name: The name of the table in the database.
        """
        # The sqlite database is the module that provides lightweight disk-based database that 
        # doesn't require a separate server process. 

        # Establis a connection to the databse
        conn = sqlite3.connect(db_name)

        # create a cursor object to execute sql commands
        curr = conn.cursor()

        # create the new table if it doesn't exists
        curr.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id TEXT, source TEXT, original_text TEXT, word_counts TEXT)')

        #commit the current transaction
        conn.commit()
        return conn
    
    @staticmethod
    def fectch_db_data(db_name:str,
                       query:str) -> None:
        """
        Fetches the data from the database based on the SQL query provided.
        """
        # try connect to the database and fetch all the information 
        try:
            conn = sqlite3.connect(db_name)
            curr = conn.cursor()
            curr.execute(query)
            rows = curr.fetchall()

            for row in rows:
                print('\n')
                print(row)

        # when exceptions happens
        except Exception as e:
            print(f'Error occurered: {e}')

        # close the connection finally
        finally:
            conn.close()
    
    @staticmethod
    def run(source_folder:str,
            dest_folder:str,
            db_name:str,
            table_name:str) -> None:
        """
        Main function to run. Connects to database, Takes all the csv files in the input directory, process it
        and moves to the processed directory and finally updates the database table.

        @@params source_folder: Folder where all the csv files to be analysed are kept.
        @@params dest_folder: Folder where all the processed csv files are moved.
        @@params db_name: The database name to be connected.
        @@params table_name: The table name in the database.
        """
        # Establish a connection to the database
        conn = WordFrequencyCounter.connect_db(db_name=db_name, table_name=table_name)

        # Get the list of csv files in the source fodler
        files = os.listdir(source_folder)
        csv_files = [file for file in files if file.endswith(".csv")]

        # iterate through each csv files
        for file in csv_files:

            # get the source filepath and destination file path to store after processing
            source_file = os.path.join(source_folder, file)
            dest_file = os.path.join(dest_folder, file)

            # get the records from the file
            records = WordFrequencyCounter.read_multiline_csv(source_file)

            # set the fiels name and create a pandas dataframe
            fields = ['id', 'source', 'original_text']
            df = pd.DataFrame(records, columns=fields)

            # do the cleaning and frequency counting in the original text field
            df['word_counts'] = df['original_text'].apply(lambda x: WordFrequencyCounter. sentence_cleaner(x))
            df['word_counts'] = df['word_counts'].apply(lambda x: WordFrequencyCounter. word_freq_counter(x))

            # move the file to destination folder
            WordFrequencyCounter.move_file(source_file, dest_file)

            # update the database
            df.to_sql(table_name, conn, if_exists='append', index=False)
        
        # close the database
        conn.close()

def main():
    # List the parameters to run the word frequency program
    input_folder = "./input_files"  #location of the input folder
    processed_folder = "./processed_files" #location of the processed folder
    db_name = "word_frequency.db" # name of the database
    table_name = "word_frequency" # name of the table to create in the database
    
    # Run the application
    WordFrequencyCounter.run(
        source_folder=input_folder, 
        dest_folder=processed_folder, 
        db_name=db_name, 
        table_name=table_name
        )
    
    # Optional to view the items in the database
    sql_query = f'SELECT * from {table_name}'
    WordFrequencyCounter.fectch_db_data(db_name=db_name, query=sql_query)

if __name__ == '__main__':
    main()