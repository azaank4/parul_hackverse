import os
import pathlib
import google.generativeai as genai
import json
import fitz
import PyPDF2

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyAmmJdR44ByOvMT9oUnH3e2GGbSXaxpUEw"
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "models/gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# Define the function to query Gemini model for generating personalized interview questions
def query_gemini_model(md_contents):
    # Define hardcoded prompt
    hardcoded_prompt = """You are tasked with generating personalized interview questions for a candidate based on the information provided in their resume, particularly focusing on their skills, academic achievements, and overall intelligence. Follow these guidelines to create a tailored set of questions:

1. Academic Performance (CGPA or GPA):
- High CGPA (e.g., 9.0 or above): Ask challenging and in-depth questions that test their problem-solving ability, theoretical knowledge, and ability to apply concepts. Focus on higher-level concepts related to their field of study.
- Average CGPA (e.g., 7.0 - 8.9): Ask questions that balance between theoretical knowledge and practical problem-solving. These should assess both their understanding of core concepts and their real-world application.
- Low CGPA (e.g., below 7.0): Ask foundational and practical questions that test basic knowledge and real-world problem-solving skills. Focus on their ability to learn and apply knowledge.

2. Skills and Expertise:
- Technical Skills (e.g., Programming Languages, Frameworks): For candidates with strong technical skills (e.g., Python, Java, C++), ask questions related to problem-solving, algorithm design, and technical concepts such as data structures and design patterns. If a candidate has experience in specific tools (e.g., TensorFlow, React), ask them to explain their experience and how they've applied these skills in real-world scenarios.
- Soft Skills (e.g., Leadership, Communication): For candidates emphasizing soft skills, ask behavioral questions that test their leadership, communication, and teamwork abilities. Ask them to provide examples of challenges they've faced and how they've resolved them.
- Experience Level: Tailor the complexity of questions to their experience level. For instance, a candidate with 5+ years of experience should be asked more strategic and management-related questions, while someone with less experience should be asked more hands-on and role-specific questions.

3. Problem-Solving Ability:
- For candidates with exceptional academic performance or technical skills, include a few problem-solving scenarios or case studies related to their field. Test their ability to break down complex problems into manageable parts and propose practical solutions.
- For those with moderate or average performance, focus on how they approach typical challenges in their field. Ask them to describe a situation where they had to solve a problem and the steps they took to address it.

4. Overall Intelligence:
- Sharp, High Intelligence: For candidates who demonstrate high potential through their academic records or specialized skills, ask questions that require critical thinking, abstract reasoning, and the application of advanced concepts in real-life scenarios.
- Moderate Intelligence: For candidates with average intelligence or mixed skill sets, ask questions that assess how well they can think logically and apply concepts in practical settings.
- Potential for Growth: If the candidate shows potential for growth but lacks some technical depth, ask them questions that test their ability to learn quickly, adapt, and think on their feet.

5. General Guidelines:
- Always consider the candidate's field of study and expertise. Tailor questions to reflect their area of specialization (e.g., software engineering, finance, marketing).
- Use the language of the resume to craft questions that feel relevant to the candidate. Reference specific projects, tools, or technologies they've worked with.
- For academic-based questions, always include the candidate's major or specific coursework mentioned in their resume.

Example Scenario:

Candidate 1: 
CGPA: 9.6, Skills: Advanced Python, AI/ML (TensorFlow), Data Structures, 2 years of research in Deep Learning.
Questions: Advanced algorithm design, deep learning concepts, hands-on coding problems in Python, TensorFlow use cases, etc.

Candidate 2:
CGPA: 7.2, Skills: Java, Web Development (React), 1 year of internship in full-stack development.
Questions: Basic algorithms, web development concepts, problem-solving scenarios, React components, etc.

Please ensure the questions you generate are personalized, challenging (or foundational depending on the candidate's profile), and directly relevant to their qualifications and experience."""

    # Process each resume
    for index, md_content in enumerate(md_contents):
        print(f"\nAnalyzing resume {index + 1}...")
        try:
            # Construct prompt and get response
            prompt = f"Analyze the following resume content: {md_content}\n\n{hardcoded_prompt}"
            response = model.generate_content(prompt)
            
            # Generate filename and save response
            filename = f"personalized_interview_{index + 1}.md"
            output_path = os.path.join("personalized_interviews", filename)
            
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(f"# Personalized Interview Questions\n\n{response.text}")
            
            print(f"Personalized interview questions saved at {output_path}")
            
        except Exception as e:
            print(f"Error processing resume {index + 1}: {str(e)}")

# Part 1: Read already converted markdown files from the 'resume' folder
def read_markdown_files(data_dir="data"):
    md_contents = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".md"):  # Only process markdown files
            md_path = os.path.join(data_dir, filename)
            print(f"Processing: {md_path}")
            with open(md_path, 'r', encoding='utf-8') as file:
                md_contents.append(file.read())
    return md_contents

# Create 'personalized_interviews' folder if it doesn't exist
os.makedirs("personalized_interviews", exist_ok=True)

# Read PDF files from accepted_resumes folder
pdf_folder = r"D:\MyCoding\Parul Hackathon\Resume Scanner\accepted_resumes"
md_contents = []
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Processing: {pdf_path}")
        try:
            # Open and read PDF file
            with fitz.open(pdf_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                md_contents.append(text)
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

# Now analyze all resumes using Gemini model
print(f"\nAnalyzing all resumes with Gemini AI model...")
query_gemini_model(md_contents)
