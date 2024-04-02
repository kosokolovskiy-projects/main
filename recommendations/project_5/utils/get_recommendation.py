import streamlit as st
import logging
import pandas as pd
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from databricks import sql
from time import time

# Setup logging
logging.basicConfig(filename="databricks_streamlit.log",
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

# Configuration
DATABRICKS_SERVER_HOSTNAME = st.secrets['DATABRICKS_INSTANCE']
DATABRICKS_HTTP_PATH = st.secrets["DATABRICKS_HTTP_PATH"]
DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]

queries_dict = {
    'user_rating': lambda user_id, movie_id: f"SELECT rating FROM movies_db.user_movie_title_rating WHERE userid = {user_id} AND movieId = {movie_id}",
    'movie_names': "SELECT title FROM movies_db.movies_bronze",
    'user_ids': "SELECT DISTINCT userId FROM movies_db.ratings_bronze",
    'movie_id_from_title': lambda title: f"SELECT movieId FROM movies_db.user_movie_title_rating WHERE title = '{title}' LIMIT 1",
    'test_query': "SELECT 1"
}


def select_user_id():  # sourcery skip: inline-immediately-returned-variable
    user_id = st.selectbox('Choose User Id: ', list(range(1, 100)), index=None)
    return user_id

def select_movie_id():  # sourcery skip: inline-immediately-returned-variable
    movie_id = st.selectbox('Choose Movie Id: ', list(range(1, 100)), index=None)
    return movie_id

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


def query_databricks_movie_id_from_title(title):
    """Query Databricks for movie ID by title."""
    query = queries_dict['movie_id_from_title'](title)
    results = execute_query(query)
    return results[0][0] if results else "No ID found."

def show_instruction():
    st.markdown('''
        ***Instruction:*** 

        1) Please choose the "*User Id*" that corresponds yours

        2) Choose the name of film you want to get recommendation to

        3) Choose one of the recommended movies and enjoy!

    ''')

def with_connection():
    show_instruction()
    user_id = st.selectbox('Choose User Id: ', query_databricks_user_ids(), index=None)
    movie_title = st.selectbox('Choose Movie Name: ', query_databricks_movie_names(), index=None)
    if user_id and movie_title:
        movie_id = query_databricks_movie_id_from_title(movie_title)
        get_similar_movies(user_id)



def get_similar_movies(user_id):
    output_path =  f"s3a://kosokolovskiy_bucket/results/similar_movies_{user_id}.parquet"
    similar_movies_df.write.format("parquet").mode("overwrite").option("path", output_path).save()
    similar_movies_df = pd.read_csv(output_path)
    st.write(similar_movies_df)

def read_parquet_from_s3(bucket_name, file_path):
    try:
        return pd.read_parquet(f's3://{bucket_name}/{file_path}', engine='pyarrow')
    except NoCredentialsError:
        st.error("AWS credentials not found.")
        return pd.DataFrame()



def demo_without_connection():  # sourcery skip: use-named-expression
    st.info('''
            Unfortunately, there is no connection to Databricks at this moment. 
        
            Please try later!
        
            With the source of project you can go to [*Link 1*](https://github.com/kosokolovskiy/projects) or [*Link 2*](https://github.com/kosokolovskiy-projects/main) and know the project from inside.

            Below is demo version of how it should look like: 
                ''')

    
    show_instruction()

    user_id = st.selectbox('Choose User Id: ', list(range(1, 100)), index=None)
    movie_title = st.selectbox('Choose Movie Name: ', list(range(1, 100)), index=None)

    if user_id and movie_title:
        with st.expander(label='These are Recommendations for You: '):
            st.markdown('''
                - Movie 1 - [*Link 1*]()
                - Movie 2 - [*Link 2*]()
                - Movie 3 - [*Link 3*]()
                - Movie 4 - [*Link 4*]()
                - Movie 5 - [*Link 5*]()
                - Movie 6 - [*Link 6*]()
                - Movie 7 - [*Link 7*]()
                - Movie 8 - [*Link 8*]()
                - Movie 9 - [*Link 9*]()
                - Movie 10 - [*Link 10*]()
            ''')

        refresh_recommendations_buttom = st.button('Press me for new Recommendations', key='refresh_recommendations_buttom')
        if refresh_recommendations_buttom:
            st.info('These are new Movies for You!') 


def check_connection():
    return 0 

def show_recommended_movie():
    if check_connection():
        with_connection()
        st.markdown('Our Recommendations to You: ')
    else:
        demo_without_connection()


def wait_for_file(bucket, key, timeout=300):
    """Wait for a specific file to be available in an S3 bucket."""
    elapsed_time = 0
    s3_client = boto3.client('s3')
    while elapsed_time < timeout:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=key)
        for obj in response.get('Contents', []):
            if obj['Key'] == key:
                return True
        time.sleep(10)
        elapsed_time += 10
    return False

def read_parquet_from_s3(bucket, key):
    """Read a Parquet file from S3 into a Pandas DataFrame."""
    file_path = f"s3://{bucket}/{key}"
    try:
        return pd.read_parquet(file_path, engine='pyarrow')
    except Exception as e:
        st.error(f"Failed to read data from S3: {e}")
        return pd.DataFrame()



def get_recommendation_main():
    show_recommended_movie()


if __name__ == '__main__':
    get_recommendation_main()