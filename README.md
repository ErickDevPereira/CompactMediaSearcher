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

## **How to use the API**

* Step 1: Create a .env file inside the root of the project.
* Step 2: Get your keys and secret keys at last.fm, twitch, google books api and omdb api.
* Step 3: Install and create a MySQL account on your local machine.
* Step 4: Fill the variables BOOKS_KEY, CLIENT_ID_GAMES, SECRET_KEY_GAMES, MOVIES_KEY, SONG_KEY, MYSQL_USER, MYSQL_PW, DATABASE_NAME with your keys and MySQL credentials inside the .env file.
* Step 5: Create a virtual environment on your machine
* Step 6: Inside the virtual environment, do pip install -r requirements.txt to install the dependencies
* Step 7: Run the main.py file

## **How to consume**

* Step 1: Do a post request to /register with the json {'email': ..., 'first_name': ..., 'last_name': ....} to register an account. Save the token on the response.
* Step 2: Access the endpoint GET /login with the json {'token': ..., 'email': ...}. Here you should use your email and token. The response will give you a JWT token that lasts for 1 hour.
* Step 3: Access the endpoint GET /search, at which you can give the parameters 'title' and 'creator' with the title and author name of your research. You must povide the json {'X-Access-Token': ...} with the JWT token as the value to the header of the request. The response will be what you asked for.

## **Screenshot example**
The endpoint GET /search?title=title=Texas Chainsaw Massacre&creator=Tope will return the following on the screenshot:
![](https://raw.githubusercontent.com/ErickDevPereira/CompactMediaSearcher/refs/heads/main/src/imgs/screenshot.png)