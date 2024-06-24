import pandas as pd

# Text input as a single string
text_data = """
Question: If I have an accident in a courtesy car provided by Churchill, what am I covered for?
Answer: You are covered for any damages to the courtesy car as well as third-party liabilities, similar to the coverage on your own car, under the conditions specified in the 'Courtesy Car' and 'Liability' sections.
Topic: Courtesy Car, Liability

Question: How does Churchill handle claims for windscreen damage when I am using a non-approved repairer?
Answer: If you use a non-approved repairer for windscreen repairs, Churchill will cover the costs up to the amount specified in your car insurance details, as described in the 'Windscreen Damage' and 'Making a Claim' sections.
Topic: Windscreen Damage, Making a Claim

Question: What documentation do I need to provide if I want to claim for theft under the motor legal cover?
Answer: You need to provide a police report and any relevant legal documents, as outlined in the 'Motor Legal Cover' and 'Fire and Theft' sections.
Topic: Motor Legal Cover, Fire and Theft

Question: Can I drive my car abroad and what are the insurance implications?
Answer: Yes, you can drive your car abroad under the same conditions covered in the policy, but you need to inform Churchill to ensure all policy conditions are met, as detailed in 'Where You Can Drive' and 'Personal Benefits'.
Topic: Where You Can Drive, Personal Benefits

Question: What steps should I follow if I need to make a claim for an accident that includes personal injuries?
Answer: You should contact Churchill immediately to report the accident, provide all necessary details, and follow their instructions for claims processing, which includes potential personal injury claims covered under 'Making a Claim' and 'Personal Benefits'.
Topic: Making a Claim, Personal Benefits

Question: How are new car replacements handled if the car is involved in an accident outside the UK?
Answer: New car replacements are handled under the policy's terms, but you must ensure that the accident is reported and processed as per Churchill's guidelines, which may involve aspects covered under 'Personal Benefits' and 'Where You Can Drive'.
Topic: Personal Benefits, Where You Can Drive

Question: If my car is stolen, what process should I follow to claim for a replacement car?
Answer: Report the theft to the police and Churchill immediately, provide all required documentation, and follow the claims process outlined under 'Fire and Theft' and 'Guaranteed Hire Car Plus' for possible car replacement.
Topic: Fire and Theft, Guaranteed Hire Car Plus
"""

# Splitting the text into segments for each Q&A
segments = text_data.strip().split("\n\n")

# Parsing each segment to extract question, answer, and topic
data = []
for segment in segments:
    lines = segment.split("\n")
    question = lines[0].replace("Question: ", "")
    answer = lines[1].replace("Answer: ", "")
    topic = lines[2].replace("Topic: ", "")
    data.append({"Question": question, "Answer": answer, "Topic": topic})

# Creating DataFrame
df = pd.DataFrame(data)
print(df)
df.to_csv("dataset_cross_reference.csv", index=False)
