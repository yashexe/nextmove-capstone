import pandas as pd
from text_preprocessing import preprocess_text  # Import the preprocessing function

def create_processed_data(input_file, output_file):
    """
    Reads labeled email data from a CSV, applies text preprocessing, and saves the
    processed data to a new CSV file with columns reordered.
    
    Args:
        input_file (str): Path to the labeled email data CSV file.
        output_file (str): Path to save the processed data CSV file.
    """
    # Load labeled data with error handling
    try:
        labeled_data = pd.read_csv(input_file, encoding='utf-8')
        print(f"Loaded data from {input_file}. Shape: {labeled_data.shape}")
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file {input_file} is empty.")
        return
    except UnicodeDecodeError as e:
        print(f"Unicode error reading {input_file}: {e}")
        return

    # Check if 'email_content' and 'category' columns exist
    if 'email_content' not in labeled_data.columns or 'category' not in labeled_data.columns:
        print("Error: Required columns 'email_content' and/or 'category' not found in the input data.")
        print(f"Columns in the file: {labeled_data.columns}")
        return

    # Apply preprocessing to the email_content column
    labeled_data['processed_content'] = labeled_data['email_content'].apply(preprocess_text)
    print("Preprocessing completed.")

    # Reorder columns to have 'category' first
    processed_data = labeled_data[['category', 'processed_content']]

    # Save processed data to output file with error handling
    try:
        processed_data.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
    except Exception as e:
        print(f"Error saving processed data to {output_file}: {e}")

# Run the script
if __name__ == "__main__":
    input_file = 'machine_learning/data/labeled_emails.csv'    # Path to labeled data
    output_file = 'machine_learning/data/processed_emails.csv' # Path to save processed data
    create_processed_data(input_file, output_file)
