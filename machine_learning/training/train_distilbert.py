import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from utils import load_config

# Load configuration at the global level
CONFIG = load_config()

# Extract paths and training parameters
DISTILBERT_CHECKPOINTS_DIR = CONFIG["paths"]["models"]["distilbert"]["checkpoints"]
DISTILBERT_TOKENIZER_DIR = CONFIG["paths"]["models"]["distilbert"]["tokenizer"]

TRAIN_DATA_PATH = CONFIG["paths"]["data"]["train_set"]
NUM_LABELS = CONFIG["training"]["num_of_classes"]
RANDOM_STATE = CONFIG["training"]["random_state"]
NUM_EPOCHS = CONFIG["training"]["num_epochs"]
BATCH_SIZE = CONFIG["training"]["batch_size"]
WARMUP_STEPS = CONFIG["training"]["warmup_steps"]
WEIGHT_DECAY = CONFIG["training"]["weight_decay"]
LOGGING_STEPS = CONFIG["training"]["logging_steps"]

# Check if CUDA (GPU) is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Tokenizer utility
def tokenize_data(data, tokenizer):
    return tokenizer(
        list(data["processed_content"]),
        truncation=True,
        padding=True,
        max_length=512,
        return_tensors="pt"
    )

# PyTorch Dataset
class EmailDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item["labels"] = self.labels[idx]
        return item

# Data preparation utility
def load_and_prepare_data(data_path, tokenizer, test_size=0.15, random_state=42):
    print("Loading and splitting data...")
    data = pd.read_csv(data_path)

    # Map labels to integers
    label_mapping = { "Work": 0, "Personal": 1, "Promotional": 2, "Urgent": 3 }
    if not pd.api.types.is_numeric_dtype(data["label"]):
        data["label"] = data["label"].map(label_mapping)
        if data["label"].isnull().any():
            raise ValueError("Found labels in the dataset that do not match the mapping. Check your data.")

    train_df, val_df = train_test_split(
        data,
        test_size=test_size,
        stratify=data["label"],
        random_state=random_state
    )
    print(f"Train size: {len(train_df)}, Validation size: {len(val_df)}")

    print("Tokenizing datasets...")
    train_encodings = tokenize_data(train_df, tokenizer)
    val_encodings = tokenize_data(val_df, tokenizer)

    train_labels = torch.tensor(train_df["label"].values, dtype=torch.long)  # Explicitly set dtype
    val_labels = torch.tensor(val_df["label"].values, dtype=torch.long)

    return EmailDataset(train_encodings, train_labels), EmailDataset(val_encodings, val_labels)

if __name__ == "__main__":
    print("Loading tokenizer...")
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

    print("Preparing datasets...")
    train_dataset, val_dataset = load_and_prepare_data(TRAIN_DATA_PATH, tokenizer, random_state=RANDOM_STATE)

    print("Loading model...")
    model = DistilBertForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=NUM_LABELS
    ).to(device)  # Move model to appropriate device

    print("Configuring training arguments...")
    training_args = TrainingArguments(
        output_dir=DISTILBERT_CHECKPOINTS_DIR,  # Checkpoints directory
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        warmup_steps=WARMUP_STEPS,
        weight_decay=WEIGHT_DECAY,
        logging_dir="./logs",                  # Directory for logs
        logging_steps=LOGGING_STEPS,
        eval_strategy="epoch",                 # Updated to avoid deprecation warning
        save_strategy="epoch",
        metric_for_best_model="eval_loss",     # Metric used to determine the best model
        greater_is_better=False,               # Lower `eval_loss` is better
        load_best_model_at_end=True
    )

    print("Initializing Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )

    print("Starting training...")
    trainer.train()

    print(f"Saving model to {DISTILBERT_CHECKPOINTS_DIR}...")
    model.save_pretrained(DISTILBERT_CHECKPOINTS_DIR)
    tokenizer.save_pretrained(DISTILBERT_TOKENIZER_DIR)
    print("Model and tokenizer saved successfully.")
