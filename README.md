# Risk Analysis DISC LinkedIn

## Objective:
The project aims to extract, analyze, and visualize data from LinkedIn profiles. It uses a distributed architecture to efficiently and securely handle requests to the LinkedIn API. The system provides an analysis of internet exposure risk based on the sensitivity of the data shared in profiles, as well as a DISC analysis of the profiles.

## Main Components:

### Data Extraction:
+ Celery: Uses Celery, a distributed task library in Python, to manage the extraction of LinkedIn profile data asynchronously and efficiently.
+ LinkedIn API: Connects to the LinkedIn API to obtain profile data using API tokens that rotate to handle rate limits.
+ Cache: Implements a caching system (using cachetools) to temporarily store profile data and reduce the number of requests to the API.

### Data Analysis:
+ Exposure Risk: Calculates the internet exposure risk for each profile based on the sensitivity of available information, such as professional experience, number of contacts, and the presence of contact information.
+ DISC Analysis: Evaluates profiles according to the DISC model (Dominance, Influence, Steadiness, Conscientiousness) using profile information (professional title and connections).

### Visualization:
+ Heat Map: Generates a heat map showing the correlation between different exposure risk factors.
+ Interaction Network: Creates a network visualization using Plotly to show interactions between profiles, representing each profile as a node and connections as edges.
+ DISC Charts: Produces pie charts for each profile, visualizing the DISC score across different categories.

### Monitoring and Scaling:
+ Flower: Uses Flower to monitor the status of Celery workers, allowing for real-time observation of task progress and system performance.
+ Horizontal Scaling: The architecture is designed to allow horizontal scaling by distributing Celery workers across multiple machines if necessary.

### Code Structure:
+ `celery.py`: Configures the Celery application with the Redis broker and backend and defines the task request rate.
+ `tasks.py`: Defines Celery tasks for extracting LinkedIn data, with error handling and caching to optimize performance.
+ `main.py`: Coordinates task execution, performs data analysis, and generates the corresponding visualizations.
+ `requirements.txt`: Lists the dependencies required for the project.

### Execution Instructions:

1. Install the dependencies.
2. Start Redis.
3. Start the Celery workers.
4. *(Optional)* Start Flower for monitoring.
5. Run the main script `main.py`.

### Security Considerations:
Ensure that the API tokens are protected and that error handling is robust to prevent the exposure of sensitive information.

## Step-by-Step Execution Instructions:

### Install Dependencies:
Make sure you have an active virtual environment and run: 
```
pip install -r requirements.txt
```

### Start Redis:
Ensure the Redis server is running.

### Start the Celery Workers:
Run in a terminal: 
```
celery -A celery worker --loglevel=info
```

### Start Flower (optional for monitoring):
In a separate terminal: 
```
celery -A celery flower
```

+ Access Flower at http://localhost:5555

### Run the Main Script:
Run `main.py` to start data processing and visualization.
