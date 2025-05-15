import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    skills_db = ['python', 'machine learning', 'data analysis', 'sql', 'deep learning', 'nlp', 'excel', 'communication']
    extracted_skills = []
    doc = nlp(text.lower())
    for token in doc:
        if token.text in skills_db:
            extracted_skills.append(token.text)
    return list(set(extracted_skills))

def load_job_descriptions(file_path):
    return pd.read_csv(file_path)

def recommend_jobs(resume_text, job_df):
    corpus = job_df['Job_Description'].tolist()
    corpus.append(resume_text)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)

    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    job_df['Similarity_Score'] = cosine_sim.flatten()
    recommended_jobs = job_df.sort_values(by='Similarity_Score', ascending=False).head(5)
    return recommended_jobs[['Job_Title', 'Company', 'Similarity_Score']]
