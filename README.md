Compact Media Searcher  
---

A REST API that simulates the behavior of a real-world search engine by integrating multiple external data sources and applying Linear Algebra to compute relevance.

This project combines:

* Asynchronous integration with 4 external APIs  
* Automatic document generation  
* TF-IDF vectorization  
* Cosine similarity ranking  
* Temporary persistence for result ordering in MySQL  
* JWT-based authentication

More than just a backend project, this is an exploration of applied mathematics in information retrieval systems.

## **Overview**

When a search request is made (title \+ content creator), the system:

1. Dispatches asynchronous requests to 4 external media APIs:

   * Movies

   * Music

   * Games

   * Books

2. Consolidates the returned data

3. Automatically generates documents from metadata

4. Vectorizes both query and documents using TF-IDF

5. Computes cosine similarity

6. Filters and ranks the most relevant results

7. Temporarily persists data in MySQL for final ordering  
   

   ##  **Mathematical Foundation**

The relevance engine is based on:

* Term Frequency (TF)  
* Inverse Document Frequency (IDF)  
* TF-IDF weighting  
* Cosine similarity

The mathematical logic was implemented manually, including:

* Vocabulary construction  
* Frequency calculation  
* Vector generation  
* Dot product computation  
* Vector norm calculation

NumPy is used to support vectorization and matrix operations.

![](https://raw.githubusercontent.com/ErickDevPereira/CompactMediaSearcher/refs/heads/main/src/imgs/tf-idf.png)

Description: main idea behind TF-IDF

## **Architecture**

The system was designed with clear separation of responsibilities.

Each component acts as a well-defined unit within the search engine

![](https://raw.githubusercontent.com/ErickDevPereira/CompactMediaSearcher/refs/heads/main/src/imgs/api_schema.png)

Description: API endpoints

## **Asynchronous Orchestration**

External API calls are executed using `asyncio`, allowing concurrent requests to reduce total response time.

Even with multiple external integrations, the system maintains efficient performance through asynchronous orchestration.

##  **Authentication**

The project includes:

* User registration  
* Login system  
* JWT generation  
* Temporary tokens for authenticated requests  
  Each logged-in user receives a JWT to access protected endpoints securely.

## **Persistence Strategy**

After TF-IDF filtering:

* Results are temporarily stored in MySQL  
* Ranked by similarity score  
* Returned in order of relevance

##  **Technologies Used**

* Python: main language  
* Flask: framework to build APIs  
* MySQL: RDBMS used to store data  
* NumPy: library that allows vectorization