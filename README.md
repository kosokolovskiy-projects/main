# Table of Contents

## Content: 

   - Different
   - [Jupyter Notebooks](#jupyter-notebooks)
     - [Bank Marketing](#bank-marketing)
     - [Predicting Emojis in Tweets](#predicting-emojis-in-tweets)
     - [Stocks Price Analysis](#stock-price-analysis)
     - [Recommendations Pandas](#recommendation-model-pandas-version)
   - [Recommendations](#recommendations)
   - [Tutor App](#tutor-app)
   - [Video Summarizer](#video-summarizer)

------------------------------------------------------------------------------------------------------------------------------------------------

## Tutor App: 

If you are interested how Tutor App looks like and works, you are welcome to visit [*Tutor App Website*](https://tasks-app.streamlit.app) with:
- *username*: demo
- *password*: demo_user_2024Q

**What could be interesting here?:**

1) Two data scrapers have been developed to extract tasks from various sources, enhancing our database of assignments. The raw data gathered is processed and formatted, ensuring it's ready for subsequent uploads to the relevant databases.

2) Scripts for uploading data to various databases have been created:
- **MySQL on Amazon RDS**: a serverless setup optimized for MySQL operations.
- **MongoDB on AWS EC2**, providing scalable and efficient database management.
- As a precautionary measure, **local database replicas** have been established. These replicas are updated simultaneously with AWS to prevent data loss in the event of an unforeseen incident.

3) Utilization of **Google APIs** for the following purposes:
- Automatic upload of files with updated homework assignments (the file itself is modified in LaTeX, the raw LaTeX code is not provided here).
- Command-line-based upload of complete new versions in a single command. A script has been written that allows for the automatic uploading and numbering of versions with just one command.

4) Utilization of AWS SDK boto3:
- When dealing with images, it was necessary to store them on a remote server -> an S3 bucket was chosen. For each assignment involving images, a request is made to the bucket, and the image is downloaded.

***IMPORTANT***: In this application, all confidential information, including links, access keys, logins, passwords, and student information, has been removed or anonymized.

------------------------------------------------------------------------------------------------------------------------------------------------

## Video Summarizer

The app is embedded into my *Streamlit* App hosted on *EC2* instance AWS that is available by the [***Summarizer App***](http://18.159.209.91:8501).

#### Overview

This project develops a _Streamlit_ application designed to offer users the capability to process YouTube videos by extracting transcripts and generating concise summaries. The application seamlessly combines Python programming with a suite of tools and APIs, including _PyTube_, _OpenAI_, _moviepy_, and _Boto3_, to deliver a comprehensive solution for video content analysis and summarization.

#### Objectives

The primary objectives of the project include:

- Providing an easy-to-use interface for users to input YouTube video links.
- Extracting and processing video and audio data from YouTube videos.
- Generating accurate transcripts for the audio content in the selected language.
- Producing concise summaries of the video content using advanced AI models.
- Storing processed data securely on _AWS S3_ for persistence and ease of access.
- Offering users the ability to download both the transcripts and summaries.

#### Key Features

The application encompasses several key features to achieve the project objectives:

1. ***YouTube Video Processing***: Utilizes the PyTube library to download YouTube videos given a valid URL. It supports filtering for video quality and file format.

2. ***Audio Extraction***: Employs the moviepy library to extract audio tracks from downloaded videos for transcription purposes.

3. ***Transcription and Summarization***: Leverages OpenAI's GPT models for transcribing the audio content and generating summaries. This process involves segmenting the audio to handle longer content effectively and ensuring the summaries are concise and informative.

4. ***AWS S3 Integration***: Implements _Boto3_ to interact with _AWS S3_, allowing for the uploading, storing, and managing of videos, audio files, transcripts, and summaries. This ensures data is securely managed and easily retrievable.

5. ***Streamlit Application***: The entire process is encapsulated within a _Streamlit_ application, providing a user-friendly interface for inputting video links, selecting languages, and downloading outputs.

#### Implementation

The project implementation is structured around two main classes:

- ***File_Proccessor***: Handles the downloading of YouTube videos, extraction of audio, and segmentation for transcription. It ensures videos are processed efficiently and prepared for transcription and summarization.

- ***Summarizer***: Utilizes OpenAI's API to generate summaries from the transcribed text. It is designed to create concise summaries that capture the essence of the video content.

Additionally, the project integrates _AWS S3_ for data storage, using _Boto3_ to upload, download, and manage files on the cloud. Also _CDK_ of AWS was used to introduce _lambda_ function. This allows for a scalable and reliable storage solution.

#### Challenges and Solutions

Several challenges were encountered during the project, including handling large video files, processing audio for transcription, and generating meaningful summaries. These were addressed through efficient data handling techniques, segmenting audio files for better processing, and fine-tuning the summarization process to improve output quality.

#### Conclusion

This Streamlit application provides a comprehensive solution for YouTube video processing, offering users an easy way to extract transcripts and generate summaries of video content. By leveraging cutting-edge technologies and APIs, the project successfully meets its objectives, demonstrating a practical application of video content analysis and summarization.

------------------------------------------------------------------------------------------------------------------------------------------------

## MovieLens Recommendation System Documentation

### Overview

This document provides a comprehensive overview of a recommendation system developed to suggest movies to users based on their preferences and interactions. The application leverages advanced data processing and machine learning techniques, implemented on the Databricks platform, to provide personalized movie recommendations.

### Architecture

The system is built upon a multi-layered data architecture consisting of Bronze, Silver, and Gold tables, facilitating data ingestion, transformation, and analysis stages, respectively. It employs Delta Lake for robust data management and Spark for distributed data processing.

#### Personalized Recommendation Algorithm

Utilizing the Alternating Least Squares (ALS) algorithm for Collaborative Filtering, the system predicts user preferences for movies they haven't interacted with. The ALS model optimizes latent factors for users and movies, enabling the identification of similar movies based on cosine similarity.

### Implementation

#### Widgets for User Interaction

- Streamlit widgets facilitate user input, allowing selection of specific movies for which recommendations are sought.

### Data Caching

- Strategic caching of frequently accessed tables enhances performance by reducing read operations from disk.

#### Recommendation Generation

- The application identifies similar movies to a user-selected title, ranking them based on similarity scores. This list is then presented to the user as recommendations.

### Usage

The application interface, built with Streamlit, guides users through the process of selecting a movie and receiving personalized recommendations. It provides a seamless experience, from data input to visualization of suggested movies.

### Conclusion

The MovieLens Recommendation System represents a sophisticated application of machine learning and data engineering principles to provide personalized content recommendations. By leveraging the power of Databricks, Delta Lake, and Spark, it offers a scalable, efficient, and user-friendly solution for movie enthusiasts.

------------------------------------------------------------------------------------------------------------------------------------------------

## Jupyter Notebooks

If you are not interested in Jupyter Notebooks and want to get acquainted with my work you are welcome to visit [*Projects Website*](https://kosokolovskiy-projects.streamlit.app)

------------------------------------------------------------------------------------------------------------------------------------------------

### Bank Marketing

### Predicting Emojis in Tweets

The goal of the project is to predict emoji for a given piece of text - tweet.

**What is interesting here:**

1) Utilization of various deep learning models:
- LSTM (Long Short-Term Memory)
- Bidirectional LSTM
- Conv1D + Bidirectional LSTM
- LSTM with **Attention Mechanism**

2) Adoption of general-purpose models from Hugging Face, with subsequent fine-tuning for the specific task at hand, using TensorFlow

------------------------------------------------------------------------------------------------------------------------------------------------

### Stock Price Analysis

#### Introduction
The Stock Price Analysis application is a comprehensive tool designed to perform detailed analysis and forecasting on stock prices. Utilizing a robust set of Python libraries and tools, including NumPy, pandas, Matplotlib, Seaborn, scikit-learn, XGBoost, and TensorFlow, the application offers a blend of statistical and machine learning techniques to understand stock market trends, make predictions, and analyze stock behavior.

#### Key Features and Functions

##### Data Processing and Analysis
- The application starts with data exploration, focusing on OCLHV data for stocks like INFY and TCS over specified periods. Essential features include volume shocks, price shocks, and the distinction between pricing shocks with and without volume changes.
- Various utility functions are introduced for visualizations, data windowing, making predictions, and evaluating model performance, enhancing the analytical capabilities of the application.

##### Modeling and Prediction
- Different models, including dense neural networks, convolutional networks (Conv1D), and traditional machine learning algorithms (Ridge, Lasso, XGBoost), are employed to forecast stock prices based on historical data.
- The application emphasizes the importance of feature engineering, demonstrating the impact of adding features like volume shocks and price shocks on model performance.
- Each model's predictions are evaluated using metrics such as MAE, MSE, RMSE, and R2 score, providing insights into their forecasting accuracy.

##### AWS Integration
- The application integrates AWS services for storing and managing datasets and generated plots, ensuring a streamlined workflow and easy access to outputs.

##### Implementation Highlights

- **Utility Functions**: The suite of utility functions for plotting, loss curve visualization, and performance evaluation are pivotal for iterative model development and analysis.
- **Modeling Approach**: The application's layered approach, starting from simple dense models to more complex machine learning algorithms, showcases a structured method to stock price forecasting.
- **Feature Importance**: By leveraging XGBoost, the application not only predicts future stock prices but also identifies the most influential features, offering valuable insights into stock price movements.

#### Challenges and Solutions

- **Data Preprocessing**: Managing varying stock market holidays and ensuring consistent data for analysis required careful data windowing and preprocessing, addressed through custom windowing functions.
- **Model Complexity vs. Performance**: Balancing model complexity and computational efficiency, especially with larger window sizes and feature sets, was managed through efficient coding practices and leveraging cloud computing resources.

#### Conclusion

The Stock Price Analysis application represents a robust tool for financial analysts and enthusiasts to dive deep into stock market analysis. Through a combination of data exploration, feature engineering, and advanced modeling techniques, it offers a detailed perspective on stock price behaviors and predictions, backed by a solid computational and theoretical framework. Integration with cloud services further enhances its practicality, making it a versatile solution for real-world financial analysis.

------------------------------------------------------------------------------------------------------------------------------------------------

### Bank Marketing Classification Task: Final Report

#### Introduction
The Bank Marketing project is centered on the analysis of direct marketing campaigns by a Portuguese banking institution. Utilizing data from phone calls made to clients, the objective is to predict whether a client will subscribe to a term deposit. This binary classification task involves processing, analyzing, and modeling complex datasets to uncover patterns that indicate a client's likelihood to subscribe.

#### Key Features and Functions

##### Data Preparation and Analysis
- **Data Importation**: Initial steps involve importing essential Python libraries and the dataset, followed by preliminary data examination.
- **Utility Functions Creation**: To streamline processes such as AWS data uploading, data visualization, statistical analysis, and machine learning modeling, a suite of utility functions was developed.
- **Exploratory Data Analysis (EDA)**: Through EDA, insights into numerical and categorical variables were gleaned. This included the identification of outliers, skewed distributions, and the relationship between variables and the target outcome.

##### Modeling and Optimization
- **Baseline Modeling**: Initial models without feature engineering were deployed, including Logistic Regression, Random Forest, XGBoost, and SVC, to establish baseline performances.
- **Feature Engineering**: Insights from EDA informed the engineering of features to enhance model predictions. Techniques included data transformation and categorization.
- **Model Optimization**: Utilizing Optuna for hyperparameter tuning, particularly with the XGBoost classifier, to refine models for improved prediction precision.

##### Challenges and Solutions

- **Data Skewness and Outliers**: Certain numerical features exhibited skewness and outliers, potentially impacting model accuracy.
  
  **Solution**: Data transformation techniques, such as logarithmic scaling, and the removal of extreme outliers, were applied.
  
- **Feature Selection for Categorical Variables**: The presence of numerous categorical variables required careful selection to ensure model relevance.

  **Solution**: Chi-squared tests were conducted to evaluate the independence of categorical features, informing their inclusion or exclusion in the model.
  
- **Hyperparameter Tuning**: Finding the optimal set of hyperparameters for models, especially for complex ones like XGBoost, presented a challenge.

  **Solution**: Optuna was employed for systematic and efficient hyperparameter optimization, significantly enhancing model performance.

#### Conclusion
The Bank Marketing Classification Task demonstrates the power of a structured data science approach in tackling predictive modeling challenges. Through comprehensive data analysis, strategic feature engineering, and sophisticated model optimization techniques, the project achieved its goal of predicting client subscription outcomes effectively. The methodologies and insights derived from this project can serve as a valuable reference for similar marketing analytics endeavors in the banking sector and beyond.

------------------------------------------------------------------------------------------------------------------------------------------------

### Recommendation Model: Pandas Version

#### Introduction

The project develops a recommendation model utilizing Pandas, NumPy, Matplotlib, Seaborn, and Scikit-learn libraries, focusing on collaborative filtering principles to recommend movies based on user ratings. The model aims to enhance user experience by suggesting films similar to those they have previously enjoyed.

#### Key Features and Functions

##### Data Preparation and Analysis

- **Exploratory Data Analysis (EDA)**: The initial phase involved understanding the dataset's structure, contents, and distributions, identifying patterns, anomalies, or interesting correlations between variables such as user ratings and movie genres.

- **Data Reading and Cleaning:** Data is sourced either locally from a designated folder or fetched from an S3 Bucket, followed by comprehensive cleaning and preprocessing.
Useful Information Extraction and Dataframe Merging: Key insights, including the number of unique movies, users, tags, genres, and ratings, were extracted. This included merging various datasets to form a consolidated view of the data.
Modeling and Optimization

- **Recommendation Model Creation:** A collaborative filtering model is developed, focusing on item similarities based on user rating patterns. It calculates similarities between movies using the dot product of their rating vectors in a sparse matrix.

- **Similar Movies Function:** Implements a function to find movies similar to a given movie based on user ratings, enhancing personalized recommendations.

- **Movies for User Function:** Introduces a "90th Percentile Strategy" for recommending a diverse array of movies to users based on their top-rated movies.

#### Challenges and Solutions

- **Data Skewness and Outliers:** Identified extreme rating behaviors and high-frequency rating activities that could skew recommendations.

**Solution**: Implemented methods to exclude outliers and refine data quality, such as filtering users based on their rating patterns and frequency.
  
- **Feature Selection for Categorical Variables**: Addressed the challenge of integrating categorical variables like genres into the recommendation system.

**Solution**: Utilized genre-based analysis and user preferences mapping to enhance the recommendation model's accuracy and personalization.

#### Conclusion

The project successfully demonstrates the development of a movie recommendation system using Pandas and collaborative filtering. Through meticulous data preparation, analysis, and model optimization, the system can offer personalized movie suggestions, thereby improving user engagement and satisfaction. Future improvements could include incorporating more sophisticated algorithms and addressing the nuances of user behavior and data quality for even more refined recommendations.
