import streamlit as st
import pickle
import re
# import nltk

# nltk.download('punkt')
# nltk.download('stopwords')


clf=pickle.load(open("clf.pkl","rb"))
tfidf=pickle.load(open("tfidf.pkl","rb"))

import re  # re library is used for working with regular expressions to search, replace, or modify strings

def CleanResume(txt):
    # Removing URLs from the text (any string starting with 'http' and followed by any characters)
    cleantxt = re.sub('http\S+\s', ' ', txt)  # Replace URLs with a space
    
    # Removing mentions (words starting with '@', usually for usernames in social media)
    cleantxt = re.sub('@\S+', ' ', cleantxt)  # Replace mentions with a space
    
    # Removing hashtags (words starting with '#')
    cleantxt = re.sub('#\S+', ' ', cleantxt)  # Replace hashtags with a space
    
    # Removing the terms 'RT' (Retweet) and 'CC' (Carbon Copy) which are common in social media text
    cleantxt = re.sub('RT|CC', ' ', cleantxt)  # Replace 'RT' or 'CC' with a space
    
    # Removing all special characters like punctuation (e.g., !, @, #, $, etc.)
    cleantxt = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_'{|}~"""), ' ', cleantxt)
    
    # Removing non-ASCII characters (characters not in the range of standard English letters and symbols)
    cleantxt = re.sub(r'[^\x00-\x7f]', ' ', cleantxt)  # Replace non-ASCII characters with a space
    
    # Removing extra spaces (sequences of multiple spaces) and replacing them with a single space
    cleantxt = re.sub('\s+', ' ', cleantxt)  # Normalize spaces by replacing multiple spaces with a single space
    
    return cleantxt


category_mapping = {
    6: 'Data Science',
    12: 'HR',
    0: 'Advocate',
    1: 'Arts',
    24: 'Web Designing',
    16: 'Mechanical Engineer',
    22: 'Sales',
    14: 'Health and fitness',
    5: 'Civil Engineer',
    15: 'Java Developer',
    4: 'Business Analyst',
    21: 'SAP Developer',
    2: 'Automation Testing',
    11: 'Electrical Engineering',
    18: 'Operations Manager',
    20: 'Python Developer',
    8: 'DevOps Engineer',
    17: 'Network Security Engineer',
    19: 'PMO',
    7: 'Database',
    13: 'Hadoop',
    10: 'ETL Developer',
    9: 'DotNet Developer',
    3: 'Blockchain',
    23: 'Testing'
}

def main():
# mamking web 
    st.title("Resume Screening App")
    uploades_res=st.file_uploader("upload resume",type=['txt','csv','pdf'])
    # to check uploaded resume is empty
    if uploades_res is not None:
        try:
            resume_bites=uploades_res.read()
            resume_text=resume_bites.decode("utf-8")
        except UnicodeDecodeError:
            resume_text=resume_bites.decode("latin-1")
        cleaned_resume=CleanResume(resume_text)


        #  now my resume is cleaned  after decoding 

        # now i transform it 
        input_features=tfidf.transform([cleaned_resume])
        predict_id=clf.predict(input_features)[0]  # 0 for category 1 for  resume 
        # st.write(predict_id)
        category_name=category_mapping.get(predict_id,"unknown")
        st.write(category_name)
        
       
if __name__ == "__main__":
    main()
