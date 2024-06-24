import pandas as pd

# Text input as a single string
text_data = """
Question: What does the insurance cover in case of fire damage to my car?
Answer: Fire damage to your car is covered under the market value.
Topic: Fire and Theft

Question: Am I covered for theft if I leave my car unlocked?
Answer: No, claims for theft or attempted theft will not be paid if the car is left unlocked.
Topic: FAQs

Question: How much will Churchill pay if my car's windscreen is damaged?
Answer: The cost of repairing or replacing the car's windscreen up to its UK market value.
Topic: Windscreen Damage

Question: Who is eligible for a courtesy car?
Answer: A courtesy car is provided to those whose car is being repaired by an approved repairer, subject to availability.
Topic: Courtesy Car

Question: Is there a specific procedure to follow when making a claim?
Answer: Yes, you should provide your personal details, policy number, and car registration number, among other required information.
Topic: Making a Claim

Question: What types of damage are not covered by the policy?
Answer: Mechanical or electrical failure, wear and tear, and damage to tyres caused by braking are not covered.
Topic: Losses We Don’t Cover

Question: Can I drive other cars under my policy?
Answer: The certificate of motor insurance will specify who is covered to drive other cars.
Topic: FAQs

Question: What is the maximum cover provided for property damage?
Answer: The insurance covers up to £20,000,000 per accident for property damage.
Topic: Liability

Question: Are there any benefits provided for personal accidents?
Answer: Yes, the policy includes personal accident benefits up to £10,000.
Topic: Personal Benefits

Question: What does Motor Legal Cover include?
Answer: It includes coverage for legal costs and expenses for motoring offences and contract disputes.
Topic: Motor Legal Cover
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
df.to_csv("dataset.csv", index=False)
