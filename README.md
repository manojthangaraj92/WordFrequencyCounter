# Word Frequency Program

This project includes the python script that accepts csv files to be analysed in the folder named **input_files** at the root directory. 
Each csv file will have three fields such as **“id”, “source”, “original_text”**. The script analyses the each csv file in the folder, performs word frequency count on the field **original_text**.
The results are then stored in a database along with the original fields in the csv file.
Finally, the original files are moved to the **processed_files** folder.

## Assumptions

- A line break denotes a new row in the file.
- The texts in each field included between smart quotes **'“”'** and seperated by **commas**.

## Prerequisites

Before running this project, you'll need to install python in your machine.

## Setting Up Your Environment

Follow these steps to set up and activate a virtual environment.

### For Windows

1. **Create a Virtual Environment**
   - Open a command prompt and navigate to your project directory:
     ```bash
     cd path\to\your\project
     ```
   - Create a virtual environment named `venv` (or any other name you prefer):
     ```bash
     python -m venv venv
     ```

2. **Activate the Virtual Environment**
   - Activate the virtual environment:
     ```bash
     .\venv\Scripts\activate
     ```

### For macOS and Linux

1. **Create a Virtual Environment**
   - Open a terminal and navigate to your project directory:
     ```bash
     cd path/to/your/project
     ```
   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     ```

2. **Activate the Virtual Environment**
   - Activate the virtual environment:
     ```bash
     source venv/bin/activate
     ```

## Install Dependencies

After activating the virtual environment, install the required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## CSV Files Insertion

After installing the dependencies, put all the csv files into the folder **./input_files**

## Running the Application

To run the application, use the following command:

```bash
python main.py
```

This will process the CSV files in the input directory, update the database with word frequency results, and move the processed files to the designated output directory.

## Deactivating the Virtual Environment

When you're done, you can deactivate the virtual environment by running:

```bash
deactivate
````