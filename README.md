## Qualtrics to Quickbase Pipeline

A common task in my job is to download survey data from Qualtrics and upload it to a database. In this case, Quickbase is the destination. This data is extremely useful because it gives an overall idea of what projects are currently administering surveys, who is creating them, and allows our team to track our work.

### Goal
First, I wanted to automate this portion of my job, as it is repetitive and requires a lot of maintenance. Second, this project allows me to expand my understanding of APIs and how to build robust pipelines on important data. While I am just moving high level survey metadata right now, I hope to extend this in numerous ways in the future.
1. There is important data related to how survey takers interact with these instruments, so collecting response data will enrich this dataset. That requires a lot more development though since it would be significantly more data.
2. Sometimes teams want data to go somewhere other than Quickbase. The pipeline could be modified to be more flexible for these requests.
