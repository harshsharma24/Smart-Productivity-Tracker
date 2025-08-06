# Smart Productivity Tracker

A simple Streamlit todo app that syncs your tasks with Azure Blob Storage.

## Prerequisites

* Python 3.7 or higher
* Azure Storage account and container
* SAS token with write access to your Blob container
* `.env` file with:

  ```env
  SAS_TOKEN=sv=...&ss=...&srt=...&sp=...&se=...&st=...&spr=...&sig=...
  ```

## Installation

```bash
pip install streamlit azure-storage-blob python-dotenv
```

## Configuration

In `app.py`, load your environment and set blob details:

```python
from dotenv import load_dotenv
import os
load_dotenv()
sas_token = os.getenv("SAS_TOKEN")
account_name = "<your_account>"
container_name = "<your_container>"
```

## Usage

Run the app:

```bash
streamlit run app.py
```

* **Add Task**: Enter a task and click **Add Task**.
* **Show Tasks**: View and filter tasks, mark done, or download JSON. Each download also **uploads** the tasks JSON to your Azure Blob container.
* **Delete Task**: Remove a task by its ID.
* **Upload Tasks**: Import tasks from a JSON file into the app.

Tasks are stored in Streamlit session state and reset on restart. Azure Blob Storage ensures your task exports are backed up remotely.
