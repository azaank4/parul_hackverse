import os
import fitz
import google.generativeai as genai
import datetime
import re
import shutil

# Define folder paths
input_resumes = "input_resumes"
history = "history"
accepted_resumes = "accepted_resumes"

# Create folders if they don't exist
os.makedirs(input_resumes, exist_ok=True)
os.makedirs(history, exist_ok=True)
os.makedirs(accepted_resumes, exist_ok=True)  # Create accepted folder

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")  # Extract text from each page
    return text

# Configure API key
GOOGLE_API_KEY = "YOUR-API-KEY"
genai.configure(api_key=GOOGLE_API_KEY)
print("Google API Key: ", GOOGLE_API_KEY)
# Set the default model to "models/gemini-1.5-flash"
MODEL_NAME = "models/gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)
print("Model name: ", MODEL_NAME)

# Function to construct prompt and get response from the model
def construct_prompt_and_get_response(instructions, combined_text):
    prompt = f"{instructions}: {combined_text}"
    response = model.generate_content(prompt)
    return response.text

# Function to move files to the accepted_resumes folder
def move_files_to_accepted(file_names):
    for file_name in file_names:
        # Check if the file exists in the input folder
        source_path = os.path.join(input_resumes, file_name)
        destination_path = os.path.join(accepted_resumes, file_name)
        
        if os.path.exists(source_path):
            # Move the file to the accepted_resumes folder
            shutil.move(source_path, destination_path)
            print(f"Moved {file_name} to accepted_resumes.")
        else:
            print(f"File {file_name} not found in input_resumes.")

# Function to process the documents with 3 iterations
def process_documents():
    try:
        # Get all PDF files in the input_resumes folder
        filenames = [f for f in os.listdir(input_resumes) if f.lower().endswith('.pdf')]
        
        if not filenames:
            print("No PDF documents found in the input folder.")
            return
        
        combined_text = ""
        for index, filename in enumerate(filenames):
            filepath = os.path.join(input_resumes, filename)
            text = extract_text_from_pdf(filepath)
            combined_text += f"[Document #{index + 1} = {filename}]\n{text}\n"
        
        # Define the instruction
        instruction = "Review the following list of PDF documents. Identify and highlight the filenames of the documents that have skills as Python or Java. Strictly follow this criterion and only highlight filenames that match. Do not include any filenames that do not meet the specified requirements and also don't mention them in the response as well."
        
        # Perform 3 iterations
        iterations = 3
        for i in range(iterations):
            print(f"\n--- Iteration {i+1} ---")
            # Get the response from the model
            response = construct_prompt_and_get_response(instruction, combined_text)
            
            if not response:
                print("No response received from the model.")
            else:
                print("Response received.")
            
            # Log the response for this iteration
            today = datetime.date.today().strftime("%Y-%m-%d")
            log_file = os.path.join(history, f"{today}.log")
            with open(log_file, 'a') as f:
                f.write(f"Iteration {i+1}:\n")
                f.write(f"Instructions: {instruction}\n")
                f.write(f"Response: {response}\n")
            
            # Extract and process filenames only for the 3rd iteration
            if i == iterations - 1:  # Check if it's the last iteration (3rd)
                print("\n--- Extracting filenames for the 3rd iteration ---")
                file_names = re.findall(r'\b[\w.-]+\.pdf\b', response)
                
                if not file_names:
                    print("No file names extracted in the 3rd iteration.")
                else:
                    print("Highlighted files in the 3rd iteration:", file_names)
                    
                    # Move the highlighted files to the accepted_resumes folder
                    move_files_to_accepted(file_names)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_documents()
