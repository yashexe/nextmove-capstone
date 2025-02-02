from utils import validate_dataset

if __name__ == "__main__":
    try:
        print("Validating dataset...")
        validate_dataset()  # No file provided, uses path from config.yaml
    except ValueError as e:
        print(f"Validation failed: {e}")
