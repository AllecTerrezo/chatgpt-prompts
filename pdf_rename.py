import os
import PyPDF2
import re
import openai
import warnings

warnings.simplefilter("ignore", category=UserWarning) #supress warnings from incompatible PDFs

openai.api_key = "" #use your chatgpt api key

def get_page(pdf_file): #get the first 400 characters from the first page of a PDF, remove newlines and special characters
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    page_obj = pdf_reader.pages[0]
    page_1 = page_obj.extract_text()
    page_1_top = page_1[0:400].replace("\n", " ") 
    page_1_top = re.sub('[^a-zA-Z0-9 \n\.]', '', page_1_top)
    return page_1_top

def get_title(prompt): #Use chatgpt in order to get article title
    prompt =  re.sub("[:;,()\-]", "", prompt)
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role":"user", "content": "You will receive the text of the first words of a scientfic paper. You will reply only with the title at any cost, you will pass a title even if confused, do not include any punctuation or special characters in your response."},
                {"role":"assistant", "content": "OK, I understand. I am ready for the transcript."},
                {"role":"user", "content": "In this paper we focused on practical method to perform tolerance analysis of analog circuits. Any circuit is the combination of passive, controlled and independentsources. The characteristics of analog circuit is totally depends upon the values of components used. So this paper give detailed analysis of circuit parameter variation. To execute this analysis we use sensitivity method. Using this method we can analyze any analog circuit component tolerance. Tolerance is one of the most important parameter which is considered during the design of analog VLSI circuit."},
                {"role":"assistant", "content": "TOLERANCE ANALYSIS OF ANALOG VLSI CIRCUITS USING SENSITIVITY"},
                {"role":"user", "content": "We describe the design of the analog portion of an electronics system to process signals from the photomultiplier tubes of the ATLAS Tile Calorimeter. The system has a 16-bit dynamic range and is capable of measuring energy depositions in a single calorimeter cell from to . In order to maintain the calorimeter calibration at the 1% level the system includes a charge injection circuit and a current integrator for use with a cesium source system and with the time-averaged currents produced by the LHC. Th"},
                {"role":"assistant", "content": "Design of the front-end analog electronics for the ATLAS tile calorimeter"},
                {"role":"user", "content": prompt}     
                ]
    )
    reply_content = completion.choices[0].message.content
    reply_content = reply_content.replace("-", " ").replace(":", "").replace(",", "").replace("(", "").replace(")", "").replace("  ", " ").replace(".", "").replace("/", "")
    return(reply_content)

def rename_pdf(dir): #rename all pdfs in the directory
 for file in os.listdir(dir):
  if file.endswith(".pdf"):
   path = os.path.join(dir, file)
   title = get_title(get_page(path)) + ".pdf"
   if title.startswith("Sorry but"):
     title = get_title(get_page(path)) + ".pdf"
   os.rename(path, os.path.join(dir, title))

rename_pdf("Path to PDFs")