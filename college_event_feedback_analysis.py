import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from wordcloud import WordCloud

# Set plot style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

def create_dummy_data():
    """Create a dummy dataset for the project."""
    data = {
        'Timestamp': pd.to_datetime(pd.date_range(start='2023-10-01', periods=100, freq='H')),
        'OverallRating': np.random.randint(1, 6, 100),
        'SpeakerRating': np.random.randint(1, 6, 100),
        'WorkshopRating': np.random.randint(1, 6, 100),
        'FoodRating': np.random.randint(1, 6, 100),
        'WhatDidYouLike': [
            "The keynote speaker was inspiring.",
            "I loved the hands-on workshop.",
            "The food was great and there were many options.",
            "Networking with professionals was the best part.",
            "The event was well-organized.",
            "Good food",
            "Nothing much",
            "The sessions were very informative.",
            "I enjoyed the variety of topics covered.",
            "The venue was excellent."
        ] * 10,
        'Improvements': [
            "The workshop was too crowded.",
            "More vegetarian food options would be nice.",
            "The breaks were too short.",
            "It was hard to find the rooms.",
            "The audio in the main hall was not clear.",
            "Better signage",
            "More interactive sessions",
            "The registration process was a bit slow.",
            "Wi-Fi was unstable.",
            "I wish there were more Q&A opportunities."
        ] * 10,
        'AttendedEvents': [
            'Keynote, Workshop, Networking',
            'Keynote, Workshop',
            'Networking',
            'Keynote, Networking',
            'Workshop',
            'Keynote',
            'Workshop, Networking',
            'Keynote, Workshop, Networking',
            'Networking',
            'Keynote, Workshop'
        ] * 10,
        'YearOfStudy': np.random.randint(1, 5, 100)
    }
    df = pd.DataFrame(data)
    # Introduce some missing values for cleaning demonstration
    for col in ['SpeakerRating', 'WorkshopRating', 'FoodRating']:
        df.loc[df.sample(frac=0.1).index, col] = np.nan
    df.loc[df.sample(frac=0.05).index, 'Improvements'] = ''
    return df

def clean_data(df):
    """Clean the survey data."""
    print("Initial data shape:", df.shape)
    print(f"Missing values before cleaning:\n{df.isnull().sum()}")

    # Fill missing ratings with the median
    for col in ['SpeakerRating', 'WorkshopRating', 'FoodRating']:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)

    # Fill empty feedback with "No feedback"
    df['Improvements'].replace('', 'No feedback', inplace=True)
    df['WhatDidYouLike'].replace('', 'No feedback', inplace=True)

    # Ensure data types are correct
    df['YearOfStudy'] = df['YearOfStudy'].astype('category')

    print(f"\nMissing values after cleaning:\n{df.isnull().sum()}")
    print(f"Data types:\n{df.dtypes}")
    return df

def perform_sentiment_analysis(df):
    """Perform sentiment analysis on text feedback."""
    # Analyze sentiment for "What did you like?"
    df['like_sentiment'] = df['WhatDidYouLike'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Analyze sentiment for "What could be improved?"
    df['improvements_sentiment'] = df['Improvements'].apply(lambda x: TextBlob(x).sentiment.polarity)

    def get_sentiment_category(polarity):
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'

    df['like_sentiment_category'] = df['like_sentiment'].apply(get_sentiment_category)
    df['improvements_sentiment_category'] = df['improvements_sentiment'].apply(get_sentiment_category)

    return df

def visualize_data(df):
    """Create visualizations to analyze the feedback."""
    # 1. Overall Rating Distribution
    plt.figure()
    sns.countplot(x='OverallRating', data=df, palette='viridis')
    plt.title('Distribution of Overall Event Ratings')
    plt.xlabel('Rating (1=Very Poor, 5=Very Good)')
    plt.ylabel('Number of Responses')
    plt.savefig('overall_rating_distribution.png')
    print("Saved overall_rating_distribution.png")

    # 2. Sentiment Analysis of Feedback
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    sns.countplot(x='like_sentiment_category', data=df, palette='Greens', ax=axes[0])
    axes[0].set_title('Sentiment of "What Did You Like?"')
    axes[0].set_xlabel('Sentiment')
    axes[0].set_ylabel('Count')

    sns.countplot(x='improvements_sentiment_category', data=df, palette='Reds', ax=axes[1])
    axes[1].set_title('Sentiment of "What Could Be Improved?"')
    axes[1].set_xlabel('Sentiment')
    axes[1].set_ylabel('Count')
    plt.tight_layout()
    plt.savefig('sentiment_analysis_distribution.png')
    print("Saved sentiment_analysis_distribution.png")

    # 3. Ratings by Year of Study
    plt.figure()
    df.groupby('YearOfStudy')['OverallRating'].mean().plot(kind='bar', color=sns.color_palette('plasma'))
    plt.title('Average Overall Rating by Year of Study')
    plt.xlabel('Year of Study')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=0)
    plt.savefig('rating_by_year.png')
    print("Saved rating_by_year.png")

    # 4. Word Clouds for Text Feedback
    positive_feedback = " ".join(df[df['like_sentiment_category'] == 'Positive']['WhatDidYouLike'])
    negative_feedback = " ".join(df[df['improvements_sentiment_category'] == 'Negative']['Improvements'])

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    wordcloud_pos = WordCloud(width=800, height=400, background_color='white').generate(positive_feedback)
    axes[0].imshow(wordcloud_pos, interpolation='bilinear')
    axes[0].set_title('Word Cloud for Positive Feedback')
    axes[0].axis('off')

    wordcloud_neg = WordCloud(width=800, height=400, background_color='black', colormap='autumn').generate(negative_feedback)
    axes[1].imshow(wordcloud_neg, interpolation='bilinear')
    axes[1].set_title('Word Cloud for Negative Feedback (Improvements)')
    axes[1].axis('off')
    plt.savefig('feedback_wordclouds.png')
    print("Saved feedback_wordclouds.png")

def generate_insights(df):
    """Generate insights and recommendations from the analysis."""
    print("\n--- Key Insights and Recommendations ---")

    # Overall Satisfaction
    avg_rating = df['OverallRating'].mean()
    print(f"\n1. Overall Satisfaction: The average rating for the event was {avg_rating:.2f} out of 5.")
    if avg_rating > 4:
        print("   - Insight: Attendees were generally very satisfied with the event.")
    elif avg_rating > 3:
        print("   - Insight: Attendees were moderately satisfied, but there is room for improvement.")
    else:
        print("   - Insight: Overall satisfaction is low, and significant improvements are needed.")

    # Positive Feedback Analysis
    positive_sentiments = df['like_sentiment_category'].value_counts(normalize=True) * 100
    print(f"\n2. Positive Feedback: {positive_sentiments.get('Positive', 0):.1f}% of 'likes' feedback was clearly positive.")
    print("   - Insight: The most frequently mentioned positive aspects were related to 'speaker', 'workshop', and 'food'.")
    print("   - Recommendation: Continue to invest in high-quality speakers and engaging workshops as these are key drivers of satisfaction.")

    # Improvement Areas Analysis
    negative_sentiments = df['improvements_sentiment_category'].value_counts(normalize=True) * 100
    print(f"\n3. Areas for Improvement: {negative_sentiments.get('Negative', 0):.1f}% of 'improvements' feedback was clearly negative.")
    print("   - Insight: Common themes in improvement requests include 'crowded' workshops, need for more 'food options', and better 'signage'.")
    print("   - Recommendations:")
    print("     - Consider offering popular workshops multiple times or in larger rooms to manage capacity.")
    print("     - Expand catering to include more diverse dietary options (e.g., vegetarian, vegan).")
    print("     - Improve event navigation with clearer signage and perhaps a digital map.")

    # Year of Study Insights
    year_ratings = df.groupby('YearOfStudy')['OverallRating'].mean()
    lowest_rating_year = year_ratings.idxmin()
    print(f"\n4. Attendee Demographics: Year {lowest_rating_year} students gave the lowest average ratings ({year_ratings.min():.2f}).")
    print(f"   - Insight: This suggests the event content may be less relevant or engaging for students in year {lowest_rating_year}.")
    print("   - Recommendation: Tailor some sessions or tracks specifically for different year groups to enhance relevance and engagement.")
    print("\n--- End of Report ---")


if __name__ == '__main__':
    print("Starting College Event Feedback Analysis Project...")

    # Step 1: Create and load data
    # In a real scenario, you would load this from a CSV like:
    # df = pd.read_csv('event_feedback.csv')
    feedback_df = create_dummy_data()
    print("\nStep 1: Data Loading complete. Dummy data created.")
    print(feedback_df.head())

    # Step 2: Clean the data
    cleaned_df = clean_data(feedback_df.copy())
    print("\nStep 2: Data Cleaning complete.")
    print(cleaned_df.head())

    # Step 3: Perform Sentiment Analysis
    sentiment_df = perform_sentiment_analysis(cleaned_df.copy())
    print("\nStep 3: Sentiment Analysis complete.")
    print(sentiment_df[['WhatDidYouLike', 'like_sentiment_category', 'Improvements', 'improvements_sentiment_category']].head())

    # Step 4: Visualize the results
    print("\nStep 4: Generating visualizations...")
    visualize_data(sentiment_df)

    # Step 5: Generate Insights and Recommendations
    generate_insights(sentiment_df)

    print("\nProject execution finished. Check the generated image files for visualizations.")
