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
    # Load labeled data
    labeled_data = pd.read_csv(input_file)

    # Apply preprocessing to the email_content column
    labeled_data['processed_content'] = labeled_data['email_content'].apply(preprocess_text)

    # Reorder columns to have 'category' first
    processed_data = labeled_data[['category', 'processed_content']]

    # Save processed data to output file
    processed_data.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

# Run the script
if __name__ == "__main__":
    input_file = 'machine_learning/data/labeled_emails.csv'    # Path to labeled data
    output_file = 'machine_learning/data/processed_emails.csv' # Path to save processed data
    create_processed_data(input_file, output_file)
