# process_and_split_dataset.py
import pandas as pd
from sklearn.model_selection import train_test_split
from utils import load_config, preprocess_text, validate_dataset


def process_and_split_dataset(input_file, train_output, test_output, test_size=0.2, random_state=42):
    """
    Processes the raw dataset, and splits it into training and test sets.
    Saves training portion as 'train.csv'
    Saves testing portion as 'test.csv'

    Args:
        input_file (str): Path to the raw JSON dataset file.
        train_output (str): Path to save the training dataset.
        test_output (str): Path to save the test dataset.
        test_size (float): Proportion of data to include in the test set.
        random_state (int): Random state for reproducibility.
    """
    # Ensure entire JSON dataset contains valid structure
    validate_dataset(input_file)

    # Load the raw dataset
    data = pd.read_json(input_file)
    print(f"Loaded raw dataset with {len(data)} entries.")

    # Preprocess the 'subject' and 'body' columns
    print("Preprocessing text...")
    data['processed_content'] = data.apply(
        lambda row: preprocess_text(row['subject'] or '') + ' ' + preprocess_text(row['body'] or ''),
        axis=1
    )

    # Validate processed content
    if data['processed_content'].isnull().any():
        raise ValueError("Found missing values in 'processed_content' after preprocessing.")

    # Split the dataset into training and test sets
    print("Splitting dataset into training and test sets...")
    train_df, test_df = train_test_split(
        data[['label', 'processed_content']],  # Keep only relevant columns
        test_size=test_size,
        random_state=random_state,
        stratify=data['label']
    )

    print(f"Training set size: {len(train_df)}")
    print(f"Test set size: {len(test_df)}")

    # Save the datasets
    print(f"Saving training data to: {train_output}")
    train_df.to_csv(train_output, index=False)

    print(f"Saving test data to: {test_output}")
    test_df.to_csv(test_output, index=False)

    print("Processing and splitting complete.")


if __name__ == "__main__":
    print("Loading configuration...")
    config = load_config()

    dataset_path = config["paths"]["data"]["dataset"]
    train_set_path = config["paths"]["data"]["train_set"]
    test_set_path = config["paths"]["data"]["test_set"]

    process_and_split_dataset(dataset_path, train_set_path, test_set_path)
