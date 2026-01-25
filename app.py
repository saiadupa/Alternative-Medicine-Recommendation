import streamlit as st
import pickle
import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_medicine_usage(medicine_name):
    try:
        prompt = f"Usage of {medicine_name} medicine in 15 words in single line \n\n"
        output = openai.Completion.create(
            engine='gpt-3.5-turbo-instruct',
            prompt=prompt,
            max_tokens=150
        )
        return output['choices'][0]['text']
    except Exception as e:
        return f"An error occurred: {e}"

def recommend(medicine):
    medicines_dict = pickle.load(open('medicine_dict.pkl','rb'))
    medicines = pd.DataFrame(medicines_dict)
    similarity = pickle.load(open('similarity.pkl','rb'))
    
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_medicines = []
    for i in medicines_list:
        recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
    return recommended_medicines

def get_medicines_for_disease(disease):
    try:
        prompt = f"Recommended 2 medicine names for {disease} disease\n\n"
        output = openai.Completion.create(
            engine='gpt-3.5-turbo-instruct',
            prompt=prompt,
            max_tokens=150
        )
        return output['choices'][0]['text']
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    st.set_page_config(page_title="Medicine Recommendation & Usage", page_icon="💊", layout="wide")

    st.title('Medicine Recommender System')

    page = st.sidebar.radio("Navigation", ["Recommend Medicine", "Medicine Usage Information", "Medicines for Disease"])

    if page == "Recommend Medicine":
        medicines_dict = pickle.load(open('medicine_dict.pkl','rb'))
        medicines = pd.DataFrame(medicines_dict)
        similarity = pickle.load(open('similarity.pkl','rb'))
        
        selected_medicine_name = st.selectbox(
            'Type your medicine name whose alternative is to be recommended',
            medicines['Drug_Name'].values)

        if st.button('Recommend Medicine'):
            recommendations = recommend(selected_medicine_name)
            j=1
            for i in recommendations:
                st.write(j,i)                      
                #st.write("Click here -> "+" https://pharmeasy.in/search/all?name="+i) 
                j+=1
    
    elif page == "Medicine Usage Information":
        st.title('Medicine Usage Information')
        st.write("Enter the name of the medicine to get its usage information:")
        medicine_name = st.text_input("Medicine Name")
        if st.button('Get Usage'):
            if medicine_name:
                usage_info = get_medicine_usage(medicine_name)
                st.write("Usage Information:")
                st.write(usage_info)
            else:
                st.warning("Please enter a medicine name.")
    
    elif page == "Medicines for Disease":
        st.title('Medicines for Disease')
        st.write("Enter the name of the disease to get recommended medicines:")
        disease_name = st.text_input("Disease Name")
        if st.button('Get Medicines'):
            if disease_name:
                medicine_recommendations = get_medicines_for_disease(disease_name)
                st.write("Recommended Medicines:")
                st.write(medicine_recommendations)
            else:
                st.warning("Please enter a disease name.")

if __name__ == "__main__":
    main()
