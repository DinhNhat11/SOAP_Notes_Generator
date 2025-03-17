from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

groq_api_key = os.getenv("groq_api_key")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


# llm2 = ChatGroq(groq_api_key=groq_api_key, temperature=0)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    #max_tokens = 500,
    temperature=0,
)


prompt_s = """You are a good SOAP note generator who specicailly generate Subjective, 'S' part. 
                  You will recieve a conversation between a family physician and a patient.
                  You will generate the Subjective part of the SOAP note based on that. Prioritize accuracy and precision. 
                  Do not make up any information. Use format language"""
template_s = ChatPromptTemplate.from_messages([
    ("system", prompt_s),
    ("human", "{conversation}"),
])
generate_subjective = template_s | llm
    
    
    

prompt_o = """You are a good SOAP note generator who specifically generate Objective / 'O' part. 
                  You will recieve a conversation between a family physician and a patient and a Subjective session of the SOAP notes.
                  You will generate the Objective part of the SOAP note based on the received information. Prioritize accuracy and precision. 
                  If there is no objective information in the input, you cannot return 'No objective information'. Make this part short and simple 
                  Do not make up any information. Use format language. Finally, make the output final version of Objective part that the physician
                  do not need to change anything"""
template_o = ChatPromptTemplate.from_messages([
    ("system", prompt_o),
    ("human", "{conversation}" + 
     "\n {subjective}")
])
generate_objective = template_o | llm





prompt_a = """You are a good SOAP note generator who specifically generate Assessment / 'A' part. 
                  You will recieve a conversation between a family physician and a patient, the Subjective and the Objective sessions of the SOAP notes.
                  You will generate the Assessment part of the SOAP note based on the received information. Prioritize accuracy and precision. 
                  Do not make up any information. Use format language. Finally, make the output final version of Objective part that the physician
                  do not need to change anything"""
template_a = ChatPromptTemplate.from_messages([
    ("system", prompt_a),
    ("human", "{conversation}"
     "\n {subjective}" +
     "\n {objective}")
])
generate_assessment = template_a | llm




prompt_p = """You are a good SOAP note generator who specifically generate Plan / 'P' part. 
                  You will recieve a conversation between a family physician and a patient, the Subjective, the Objective and the Assessment sessions of the SOAP notes.
                  You will generate the Plan part of the SOAP note based on the received information. Prioritize accuracy and precision. 
                  Do not make up any information. Use format language. Finally, make the output final version of Objective part that the physician
                  do not need to change anything"""

template_p = ChatPromptTemplate.from_messages([
    ("system", prompt_p),
    ("human", "{conversation}" + 
     "\n {subjective}" + 
     "\n {objective}" + 
     "\n {assessment}")
])

generate_plan = template_p | llm




if __name__ == "__main__":
    with open("conver.txt", "r") as file:
        conversation = file.read()
        print(conversation)

        print(type(conversation))

        response = generate_subjective.invoke({"conversation": conversation})
        
        print(response.content)
    
    
    # messages = [
    #     (
    #         "system",
    #         "You are a helpful assistant that answer my question. Answer in 2 sentences.",
    #     ),
    #     ("human", "What is the capital of Japan."),
    # ]
    # ai_msg = llm.invoke(messages)
    # print(ai_msg)


