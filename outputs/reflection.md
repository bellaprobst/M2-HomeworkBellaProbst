In Project 1, I used an AI chatbot to analyze the exit survey data. That process was slow and frustrating because I had to keep rephrasing prompts and fixing issues to get useful results. It was also hard to reproduce the exact same analysis since the logic was inside a conversation. In this assignment, the analysis is written in code and stored in a GitHub repository. The workflow now runs the same way every time and automatically produces the ranking and figure. The shift was from a manual, trial-and-error process to a structured and repeatable system.

The control is now in the script rather than in the AI conversation. Each step including reading the data, cleaning it, calculating averages, ranking courses, and creating the figure is clearly defined in the code. GitHub Actions runs the workflow automatically, and all changes are tracked. This makes the analysis easier to review and more reliable.

If I had one more week, I would add checks to make sure the data is formatted correctly and make the script easier to reuse for other years of survey data. I would also improve the chart to make the results clearer.

One accounting application of this workflow is in auditing. A similar automated process could rank accounts or transactions based on risk and generate consistent reports. This would improve documentation and make the analysis easier to support during an audit.
