# Main:
- different
  - c_plus_plus
  - OO_FEM_with_tkinter
- jupyter_notebooks
  - bank_marketing
  - predicting_emojis_in_tweets
  - stocks_price_analysis
- tutor_app
  - files
  - tutor_streamlit
 

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



## Jupyter Notebooks

If you are not interested in Jupyter Notebooks and want to get acquainted with my work you are welcome to visit [*Projects Website*](https://kosokolovskiy-projects.streamlit.app)


