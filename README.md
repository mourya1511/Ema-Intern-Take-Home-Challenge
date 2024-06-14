# Ema-Intern-Take-Home-Challenge

import os
from elasticsearch import Elasticsearch
import csv

# Function to preprocess lecture notes
def preprocess_lecture_notes(directory):
    lectures = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                doc_id = filename.split('.')[0]  # Extract document ID from filename
                content = file.read()
                lectures[doc_id] = content
    return lectures

# Indexer class to handle Elasticsearch operations
class Indexer:
    def __init__(self):
        try:
            # Initialize Elasticsearch connection with correct options
            self.es = Elasticsearch(
                hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}]
            )
            if not self.es.ping():
                raise ValueError("Connection failed")
            print("Elasticsearch connection established.")
        except Exception as e:
            print(f"Failed to connect to Elasticsearch: {e}")
            self.es = None

    def create_index(self, index_name):
        if self.es:
            try:
                self.es.indices.create(index=index_name, ignore=400)
                print(f"Index '{index_name}' created successfully.")
            except Exception as e:
                print(f"Index creation failed: {e}")
        else:
            print("Elasticsearch is not connected. Cannot create index.")

    def index_document(self, index_name, doc_id, doc_content):
        if self.es:
            try:
                self.es.index(index=index_name, id=doc_id, document={"content": doc_content})
                print(f"Indexed document {doc_id} into index '{index_name}'.")
            except Exception as e:
                print(f"Failed to index document {doc_id}: {e}")
        else:
            print("Elasticsearch is not connected. Cannot index documents.")

    def search(self, index_name, query):
        if self.es:
            try:
                res = self.es.search(index=index_name, query={"match": {"content": query}})
                return res['hits']['hits']
            except Exception as e:
                print(f"Search failed: {e}")
                return []
        else:
            print("Elasticsearch is not connected. Cannot perform search.")
            return []

# QueryHandler class (placeholder for demonstration)
class QueryHandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_response(self, query):
        # Placeholder logic to generate response based on query
        if "milestone model architectures" in query.lower():
            return "Some milestone model architectures include Transformer, BERT, and GPT-3."
        elif "transformer block layers" in query.lower():
            return "A Transformer block typically consists of self-attention, feedforward neural network, and normalization layers."
        elif "datasets for LLMs" in query.lower():
            return "Datasets used to train LLMs include Wikipedia, Common Crawl, and BooksCorpus."
        else:
            return "Sorry, I don't have information on that specific topic."

def main():
    # Step 1: Preprocess lecture notes
    lectures_directory = r'C:\Users\Admin\OneDrive\Desktop\notes'  # Adjust directory as needed
    lectures = preprocess_lecture_notes(lectures_directory)

    # Step 2: Initialize Indexer and create index
    indexer = Indexer()
    index_name = "lecture_notes_index"
    indexer.create_index(index_name)

    # Step 3: Index each lecture note
    for doc_id, content in lectures.items():
        indexer.index_document(index_name, doc_id, content)

    # Step 4: Load architecture information from CSV
    architecture_file_path = r'C:\Users\Admin\OneDrive\Desktop\notes\notes.csv'  # Adjust file path as needed
    architectures = {}
    try:
        with open(architecture_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                architecture_name = row['Model Name']
                architectures[architecture_name] = row
    except FileNotFoundError:
        print("Architecture CSV file not found.")
    except KeyError as e:
        print(f"KeyError: {e}. Make sure the CSV file has a 'Model Name' column.")
    except Exception as e:
        print(f"Error reading architecture CSV file: {e}")

    # Step 5: Initialize QueryHandler
    query_handler = QueryHandler(api_key="your_openai_api_key")  # Replace with your actual API key

    # Step 6: Handle user queries
    while True:
        query = input("Enter your question (type 'exit' to quit): ")
        if query.lower() == 'exit':
            break

        # Generate response based on the query
        response = query_handler.generate_response(query)
        print("Response:", response)

def generate_answer(query, lectures, indexer):
    # Function to generate answers based on search results
    results = indexer.search("lecture_notes_index", query)
    if results:
        relevant_doc_id = results[0]['_id']
        relevant_text = lectures[relevant_doc_id]
        return relevant_text
    else:
        return "Sorry, I couldn't find any relevant information."

if __name__ == "__main__":
    main()
