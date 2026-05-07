from langgraph.graph import StateGraph, END, START
from typing import TypedDict, List, Dict, Any
from groq import Groq
from dotenv import load_dotenv
import os
from nodes.jd_structuring import JDStructurer
from nodes.resume_structuring import ResumeStructurer
from nodes.validation import ValidationNode
from nodes.normalization import NormalizationNode
from nodes.matching import MatchingNode
from nodes.scoring import ScoringNode
from nodes.explainability import ExplainabilityNode
from nodes.recommendation import RecommendationNode
from nodes.gap_analysis import GapAnalysisNode
from nodes.output import OutputNode

load_dotenv(override=True)

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)


# Initialize nodes
jd_structuring_node = JDStructurer()
resume_structuring_node = ResumeStructurer()
validation_node = ValidationNode()
normalization_node = NormalizationNode()
matching_node = MatchingNode()
scoring_node = ScoringNode()
gap_analysis_node = GapAnalysisNode()
recommendation_node = RecommendationNode()
explainability_node = ExplainabilityNode()
output_node = OutputNode()



# STATE (shared memory)
class ResumeState(TypedDict):
    resume_text: str
    jd_text: str
    resume_json: Dict[str, Any]
    jd_json: Dict[str, Any]
    matched: List[str]
    missing: List[str]
    score: int
    explanation: str


class ResumeAnalyzerAgent:
    def __init__(self):
        self.client = Groq(api_key=groq_api_key)

        self.graph = self.build_graph()

    def run(self, resume: str, jd: str):
        self.initial_state: ResumeState = {
            "resume_text": resume,
            "jd_text": jd,
            "resume_json": {},
            "jd_json": {},
            "matched": [],
            "missing": [],
            "score": 0,
            "explanation": ""
        }
        
        return self.graph.invoke(self.initial_state)

    def build_graph(self):
        graph = StateGraph(ResumeState)

        # Nodes
        graph.add_node("resume_structuring", resume_structuring_node)
        graph.add_node("jd_structuring", jd_structuring_node)
        graph.add_node("validation", validation_node)
        graph.add_node("normalization", normalization_node)
        graph.add_node("matching", matching_node)
        graph.add_node("scoring", scoring_node)
        graph.add_node("gap_analysis", gap_analysis_node)
        graph.add_node("recommendation", recommendation_node)
        graph.add_node("explainability", explainability_node)
        graph.add_node("output", output_node)

        # FLOW
        graph.add_edge(START, "resume_structuring")
        graph.add_edge("resume_structuring", "jd_structuring")

        graph.add_edge("jd_structuring", "validation")
        graph.add_edge("validation", "normalization")

        graph.add_edge("normalization", "matching")
        graph.add_edge("matching", "scoring")

        graph.add_edge("scoring", "gap_analysis")
        graph.add_edge("gap_analysis", "recommendation")

        graph.add_edge("recommendation", "explainability")
        graph.add_edge("explainability", "output")

        graph.add_edge("output", END)

        return graph.compile()

        


# if __name__ == "__main__":
#     agent = ResumeAnalyzerAgent()
#     resume = """MONISH S
# ASPIRING MACHINE LEARNING &
# DEEP LEARNING ENGINEER
# CAREER OBJECTIVE EDUCATION
# Aspiring AI Engineer with hands-on B.Tech Information Technology
# experience in Machine Learning, Deep
# Gnanamani College of Technology | 2022 – 2026
# Learning, and NLP, building end-to-end
# Namakkal, Tamil Nadu.
# applications using FastAPI and Docker; strong
# HSC
# in Python and neural networks, with basic
# Marutham Matric Hr Sec School | 2021 – 2022
# JavaScript and applied data analysis. Familiar
# Morappur.
# with Generative AI, RAG workflows, and
# frameworks like LangChain and LlamaIndex, AREA OF INTEREST
# with a strong interest in AI Agents.
# Machine Learning and Deep Learning
# CONTACT DETAILS
# Generative AI
# +91 6383775271
# AI Agents & Agentic AI
# monishsasi2004@gmail.com
# Large Language Models (LLMs)
# Dharmapuri, Tamil Nadu.
# Data Analysis & Predictive Modeling
# Monish Sasikumar
# PROJECTS
# Monishsasi
# SKILLS Coffee Shop Revenue Prediction
# Programming: Python, JavaScript, SQL. Built a Linear Regression model (Python,
# Frontend: HTML5, CSS3, React.js Scikit-learn) with data cleaning, feature
# Machine Learning & Data Analysis: engineering, and scaling.
# Scikit-learn, Pandas, NumPy, Feature Achieved R² ~0.89, accurately forecasting daily
# Engineering, Model Evaluation. revenue.
# Deep Learning & NLP : TensorFlow, Developed a FastAPI backend and Streamlit UI,
# Keras, Neural Networks, NLP. containerized with Docker, and deployed
# Generative AI & Large Language locally using Docker Compose.
# Models (LLMs): Prompt Engineering,
# Gold Price Prediction
# Transformer Architecture (Attention,
# Developed a Random Forest Regressor (Python,
# Encoder/Decoder), HuggingFace
# Scikit-learn) using financial and time-series
# Transformers, Embeddings, Vector
# features.
# Databases (Chroma), RAG Workflow,
# Reached R² ~0.99, significantly improving
# LangChain, LlamaIndex (Basics).
# forecasting accuracy.
# Backend & Deployment:FastAPI,
# Docker. Retail Sales Forecasting Model
# Tools & Database: Git/GitHub, Jupyter Implemented a Decision Tree Regressor (Python,
# Notebook, Google Colab, PostgreSQL. GridSearchCV) with data preprocessing and feature
# CERTIFICATIONS selection.
# Attained R² ~0.6, demonstrating predictive
# Learn Python by Unstop
# capability for retail sales.
# Data Analysis and Data Visualization by
# pencilbitz
# Machine Learning & Deep Learning
# Internship at Icore Software Technologies"""

#     jd = """"
# Job Title: Junior AI/ML Engineer (0–1 Year Experience)Location: Bangalore/Hyderabad/Remote (India)Employment Type: Full-timeAbout the Role:We are looking for a passionate and technically sound Junior AI Engineer to join our Applied AI team. You will focus on building, testing, and deploying production-ready AI applications—specifically LLM-driven chatbots and recommendation systems—that solve real-world customer problems. This is an opportunity to learn the full AI lifecycle, from data prep to deployment, under the guidance of senior engineers.Key Responsibilities:Data Preprocessing: Clean, transform, and structure raw datasets (text, image, or tabular) for model training and retrieval pipelines.LLM Application Development: Implement Retrieval-Augmented Generation (RAG) pipelines, design prompts, and integrate LLM APIs (OpenAI, Claude, or Hugging Face) into our products.Model Training & Evaluation: Assist in fine-tuning open-source models (e.g., Llama 3) and evaluate model performance metrics such as accuracy, precision, and recall.API Development & Deployment: Package models into REST APIs using Flask/FastAPI and containerize them using Docker for deployment on AWS/Azure.Monitoring & Optimization: Monitor deployed models for data drift and latency issues in production environments.Required Skills & Qualifications:Education: Bachelor’s or Master’s degree in Computer Science, AI, Machine Learning, or related field.Programming: Strong proficiency in Python (Pandas, NumPy, Scikit-learn).AI Frameworks: Hands-on experience with PyTorch or TensorFlow.Tools: Familiarity with Git (version control) and Jupyter Notebooks.Knowledge: Understanding of foundational machine learning algorithms (Supervised/Unsupervised) and basic NLP techniques.Good to Have (Nice-to-Haves):Experience with Vector Databases (Pinecone, ChromaDB, Weaviate).Prior experience with LangChain or LlamaIndex.Projects showcasing deployment of AI models on GitHub.Why Apply?Hands-on mentorship on production-level MLOps.Competitive compensation (Approx. ₹6–10 Lakhs per annum for freshers).Opportunity to work with cutting-edge Generative AI tools.Key Differences in a "Real" 2026 Fresher RoleLess Math, More APIs: While understanding theory is required, the day-to-day is about integrating existing technologies (LLMs) rather than deriving backpropagation.Production Over Theory: Even as a fresher, you must know how to use Docker and Git to deploy a model, not just run it in a notebook.RAG is Essential: Knowledge of Retrieval-Augmented Generation (RAG) is the top-demanded skill in 2026 job descriptions.
# 
# """    
#     # result = agent.run(resume, jd)
    
#     print(agent.graph.get_graph().draw_mermaid())
    
#     print(result["resume_json"])