import matplotlib.pyplot as plt
import numpy as np

# Data setup
dataset_types = ['QA', 'Hallucination Check', 'Cross Reference', 'Retrieval']
faithfulness_scores = [1.0, 0.5278, 0.6857, 1.0]
answer_relevancy_scores = [0.963424, 0.586156, 0.942053, 0.974064]

# Bar settings
bar_width = 0.35  # width of the bars
index = np.arange(len(dataset_types))  # the label locations

# Plot setup
fig, ax = plt.subplots()
bars1 = ax.bar(index - bar_width/2, faithfulness_scores, bar_width, label='Faithfulness')
bars2 = ax.bar(index + bar_width/2, answer_relevancy_scores, bar_width, label='Answer Relevancy')

# Adding labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('Dataset Type')
ax.set_ylabel('Scores')
ax.set_title('Comparison of Faithfulness and Answer Relevancy by Dataset Type')
ax.set_xticks(index)
ax.set_xticklabels(dataset_types)
ax.legend()

# Display the plot
plt.show()
