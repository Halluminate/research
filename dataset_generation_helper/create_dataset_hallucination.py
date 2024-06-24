import pandas as pd

# Text input for questions that the document does not answer
text_data_hallucination = """
Question: Does the policy provide coverage for pets injured in a car accident?
Answer: The document does not specify coverage for pets injured in car accidents.

Question: Can I get a discount on my premium if I have multiple cars insured with Churchill?
Answer: The document does not discuss discounts for insuring multiple cars with Churchill.

Question: What are the age restrictions for qualifying for Motor Legal Cover?
Answer: The document does not mention any age restrictions for qualifying for Motor Legal Cover.

Question: Is there a loyalty program available for long-term policyholders?
Answer: The document does not provide information about a loyalty program for long-term policyholders.

Question: How does Churchill handle coverage for vehicles with autonomous driving features?
Answer: While the document mentions coverage for automated cars, it does not detail how Churchill specifically handles all autonomous driving features.

Question: What are the consequences of filing more than three claims in a year?
Answer: The document does not detail the consequences of filing more than three claims in a year.

Question: Does the insurance cover the cost of environmental cleanup in case of an accident?
Answer: The document does not mention coverage for environmental cleanup costs after an accident.

Question: Are there any benefits provided for using eco-friendly vehicles under this policy?
Answer: The document does not specify any special benefits for using eco-friendly or hybrid vehicles.
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
df_hallucination.to_csv("dataset_hallucination.csv", index=False)
