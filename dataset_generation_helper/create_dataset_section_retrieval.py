import pandas as pd

# Text input for questions that the document does not answer
text_data_hallucination = """
Question: Where can I find information about what to do if my car gets stolen?
Answer: Fire and Theft

Question: In which section can I learn about the coverage for damage to other people's property in an accident?
Answer: Liability

Question: Where should I look to understand the process for making a claim in case of an accident?
Answer: Making a Claim

Question: Which section covers details about using my car abroad?
Answer: Where You Can Drive

Question: Where can I find the terms for legal coverage when I’m involved in a motoring dispute?
Answer: Motor Legal Cover

Question: If I need a courtesy car while my vehicle is being repaired, which section should I refer to?
Answer: Courtesy Car

Question: Where do I look for information on what’s not covered by my policy?
Answer: Losses We Don’t Cover

Question: Which section should I consult for details on windscreen damage coverage?
Answer: Windscreen Damage

Question: Where is the information on how to handle an accident involving personal injuries?
Answer: Personal Benefits

Question: For details on protecting my no claim discount, which section provides the information?
Answer: Protected No Claim Discount
"""

# Splitting the text into segments for each Q&A
segments_hallucination = text_data_hallucination.strip().split("\n\n")

# Parsing each segment to extract question and answer
data_hallucination = []
for segment in segments_hallucination:
    lines = segment.split("\n")
    question = lines[0].replace("Question: ", "")
    answer = lines[1].replace("Answer: ", "")
    data_hallucination.append({"Question": question, "Answer": answer})

# Creating DataFrame
df_hallucination = pd.DataFrame(data_hallucination)
df_hallucination.to_csv("dataset_section_retrival.csv", index=False)
