# Improve your code using abstraction and decomposition

In our code of the "get_data.py" script we have applied abstraction and decomposition to improve its structure, readability and maintainability.

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

## Improving the code of app.py
Here are exapmples how we used abstraction and decomposition in our main "app.py" program:

## Abstraction:
**1. Class Abstraction:**

-   The Movie and Actor classes abstract movie and actor objects, respectively. They encapsulate related data and functionality, such as searching for actors in a movie or movies associated with an actor. These classes hide implementation details, allowing the main code to interact with them through a simple interface.

**2. Function Abstraction:**

-   Functions like search_term() and update_dropdown_options() encapsulate specific tasks, making the code more modular and reusable. They abstract the underlying logic, providing a clear and concise interface for interacting with the functionality they provide.

**3. Dash Callback Functions:**

-   Callback functions abstract the logic to update UI elements based on user interactions. For example, functions like update_movies_dropdown_options() and display_output() handle interaction between dropdown components and dynamically update their options or display output accordingly. They encapsulate the logic for updating UI elements, promoting code organization and maintainability.

## Decomposition:
**1. Modularization:**

-   The code is divided into smaller, manageable modules or functions, each responsible for a specific task. For example, the download_data() function in the Scripts.get_data module handles the downloading of data, while our other functions handle UI updates, data processing, and user interaction.

**2. Function Decomposition:**

-   Functions are decomposed into smaller, more focused functions to achieve specific tasks. For example, the update_dropdown_options() function abstracts the logic to update dropdown options based on search values, which is reused for different dropdowns. By decomposing functionality into smaller functions, the code becomes more modular and easier to understand, maintain, and extend.