
    1 # College Event Feedback Analysis
    2 
    3 This project analyzes feedback from a college event to derive insights and provide actionable recommendations. It
      processes survey data, performs sentiment analysis on textual feedback, and generates visualizations to highlight
      key findings.
    4 
    5 ## Project Overview
    6 
    7 The analysis pipeline consists of the following steps:
    8 
    9 1.  **Data Loading and Cleaning**: A dummy dataset is generated, and then cleaned to handle missing values and
      ensure data quality.
   10 2.  **Sentiment Analysis**: Textual feedback is analyzed to determine the sentiment (positive, negative, or
      neutral) of the comments.
   11 3.  **Data Visualization**: Several plots are generated to visualize the distribution of ratings, sentiment
      analysis results, and other insights.
   12 4.  **Insight Generation**: Based on the analysis, key insights and recommendations are formulated to help improve
      future events.
   13 
   14 ## Files
   15 
   16 -   `college_event_feedback_analysis.py`: The main Python script that runs the entire analysis pipeline.
   17 -   `overall_rating_distribution.png`: A bar chart showing the distribution of overall event ratings.
   18 -   `sentiment_analysis_distribution.png`: Bar charts showing the sentiment distribution for positive and negative
      feedback.
   19 -   `rating_by_year.png`: A bar chart showing the average overall rating by the year of study of the attendees.
   20 -   `feedback_wordclouds.png`: Word clouds that visualize the most frequent words in positive and negative
      feedback.
   21 
   22 ## How to Run
   23 
   24 1.  **Prerequisites**: Make sure you have Python and the following libraries installed:
   25     -   pandas
   26     -   numpy
   27     -   matplotlib
   28     -   seaborn
   29     -   textblob
   30     -   wordcloud
   31 
   32     You can install them using pip:
      pip install pandas numpy matplotlib seaborn textblob-de wordcloud
   1 
   2 2.  **Run the script**: Execute the following command in your terminal:
      python college_event_feedback_analysis.py

    1 
    2 3.  **View the output**: The script will print the analysis results to the console and save the visualizations as
      PNG images in the project directory.
    3 
    4 ## Key Insights
    5 
    6 The analysis provides insights into:
    7 
    8 -   Overall attendee satisfaction.
    9 -   The most liked aspects of the event.
   10 -   The main areas for improvement.
   11 -   How satisfaction varies across different student year groups.


