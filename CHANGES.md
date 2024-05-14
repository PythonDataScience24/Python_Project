# Improve your code using abstraction and decomposition

In the our code of the "get_data.py" script we have applied abstraction and decomposition to improve its structure, readability and maintainability

## Abstraction
**1. "download_file" Function:**
- This function abstracts the process of downloading a file from a URL and saving it locally. It encapsulates the complexity of handling HTTP requests and file operations.

**2. "filter_by_term" Function:**
- This function abstracts the process of filtering a DataFrame based on specific terms in a column. It encapsulates the logic for filtering data, making it reusable across different scenarios.

## Decomposition
**1. Modularization:**
- The code is divided into reusable functions (download_file and filter_by_term), each responsible for a specific task. This modular approach promotes code reuse and makes it easier to understand and maintain.

**2. Separation of Concerns:**
- Different functionalities (downloading files, data filtering, data manipulation, and file I/O) are separated into distinct functions, each focusing on a specific aspect of the program's functionality. This separation enhances clarity and simplifies debugging and testing.

**3. Data Processing Pipeline:**
- The data processing pipeline is decomposed into several stages:
    - Downloading data files from URLs (download_file function).
    - Filtering dataframes based on specific criteria (filter_by_term function).
    - Manipulating dataframes to extract relevant information (e.g., filtering out unnecessary columns, splitting and merging dataframes).
    - Writing processed data to compressed files.

**4. Variable Names:**
- Meaningful variable names are used throughout the code, enhancing readability and making it easier to understand the purpose of each variable.