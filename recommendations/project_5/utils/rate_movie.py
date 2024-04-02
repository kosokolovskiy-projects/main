import streamlit as st
import requests
import json
import boto3
from botocore.exceptions import ClientError
import os
import logging
from databricks import sql
import numpy as np

# Setup logging
logging.basicConfig(filename="databricks_streamlit.log",
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

# Configuration
DATABRICKS_SERVER_HOSTNAME = st.secrets['DATABRICKS_INSTANCE']
DATABRICKS_HTTP_PATH = st.secrets["DATABRICKS_HTTP_PATH"]
DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]

# Define queries
queries_dict = {
    'user_rating': lambda user_id, movie_id: f"SELECT rating FROM movies_db.user_movie_title_rating WHERE userid = {user_id} AND movieId = {movie_id}",
    'movie_names': "SELECT title FROM movies_db.movies_bronze",
    'user_ids': "SELECT DISTINCT userId FROM movies_db.ratings_bronze",
    'movie_id_from_title': lambda title: f"SELECT movieId FROM movies_db.user_movie_title_rating WHERE title = '{title}' LIMIT 1",
    'insert_rating': lambda data: f"INSERT INTO df_ratings VALUES {data} ON DUPLICATE KEY UPDATE rating = VALUES(rating)",
    'test_query': "SELECT 1"
}

def execute_query(query):
    try:
        with sql.connect(server_hostname=DATABRICKS_SERVER_HOSTNAME,
                                 http_path=DATABRICKS_HTTP_PATH,
                                 access_token=DATABRICKS_TOKEN) as connection:

            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    except Exception as e:
        st.error(f"Failed to execute query: {e}")
        return []

@st.cache_data
def query_databricks_user_ids():
    """Query Databricks for user ids."""
    results = execute_query(queries_dict['user_ids'])
    return sorted([int(id[0]) for id in results])

@st.cache_data
def query_databricks_movie_names():
    """Query Databricks for movie names."""
    results = execute_query(queries_dict['movie_names'])
    return [title[0] for title in results]


def query_databricks_rating(user_id, movie_id):
    """Query Databricks for a specific movie rating by user."""
    query = queries_dict['user_rating'](user_id, movie_id)
    results = execute_query(query)
    return results[0][0]

def query_databricks_movie_id_from_title(title):
    """Query Databricks for movie ID by title."""
    query = queries_dict['movie_id_from_title'](title)
    results = execute_query(query)
    return results[0][0] if results else "No ID found."

def check_already_rated(user_id, movie_id):
    if rating := query_databricks_rating(user_id, movie_id):
        st.warning(f'You have already rated this movie. Your rating was: {rating}')



def send_new_rating(user_id, movie_id, rating):
     with sql.connect(server_hostname=DATABRICKS_SERVER_HOSTNAME,
                                 http_path=DATABRICKS_HTTP_PATH,
                                 access_token=DATABRICKS_TOKEN) as connection:

        with connection.cursor() as cursor:
            data = (user_id, movie_id, rating)
            values = ",".join(data)
            cursor.execute(queries_dict['insert_rating'](values))


def give_new_rating():
    rating = st.number_input('Choose your grade: ', min_value=0.5, max_value=5.0, step=0.5)
    submit_rating_buttom = st.button('Submit Your Rating', key='submit_rating_buttom')
    if submit_rating_buttom:
        send_new_rating(rating)
        st.info('Rating Successfully submited!')

def with_connection():
    user_id = st.selectbox('Choose User Id: ', query_databricks_user_ids(), index=None)
    movie_title = st.selectbox('Choose Movie Name: ', query_databricks_movie_names(), index=None)
    if user_id and movie_title:
        movie_id = query_databricks_movie_id_from_title(movie_title)
        check_already_rated(user_id, movie_id)
        give_new_rating()


def demo_without_connection():
    st.info('''
            Unfortunately, there is no connection to Databricks at this moment. 
        
            Please try later!
        
            With the source of project you can go to [*Link 1*](https://github.com/kosokolovskiy/projects) or [*Link 2*](https://github.com/kosokolovskiy-projects/main) and know the project from inside.

            Below is demo version of how it should look like: 
                ''')
    user_id = st.selectbox('Choose User Id: ', list(range(1, 100)), index=None)
    movie_title = st.selectbox('Choose Movie Name: ', list(range(1, 100)), index=None)
    if user_id and movie_title:
        st.warning(f'This Movie is already rated by you: {np.random.choice(np.arange(0.5, 5.5, 0.5))}')
        rating = st.number_input('Choose your grade: ', min_value=0.5, max_value=5.0, step=0.5)
        submit_rating_buttom = st.button('Submit Your Rating', key='submit_rating_buttom')
        if submit_rating_buttom:
            st.success('Rating Successfully submited!') 

def check_connection():
    return 0 



def rate_movie_main():  # sourcery skip: use-named-expression

    if check_connection():
        with_connection()
    else:
        demo_without_connection()

    