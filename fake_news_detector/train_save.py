import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from collections import Counter

# Step 1: Load and prepare data
print("[INFO] Reading datasets...")
fake_df = pd.read_csv("Fake.csv")
real_df = pd.read_csv("True.csv")
print(f"[SUCCESS] Loaded Fake.csv with {len(fake_df)} rows and True.csv with {len(real_df)} rows.")

# Step 2: Label the data
fake_df['label'] = 1
real_df['label'] = 0

# Step 3: Combine, shuffle, and limit
df = pd.concat([fake_df, real_df], ignore_index=True)
df = df.sample(frac=1).reset_index(drop=True)
df = df[['text', 'label']].dropna().iloc[:10000]
print(f"[INFO] Total combined samples after limiting: {len(df)}")

# Step 4: Stratified train-test split
print("[INFO] Splitting data into train and test...")
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df['text'].tolist(),
    df['label'].tolist(),
    test_size=0.2,
    random_state=42,
    stratify=df['label']
)
print(f"[SUCCESS] Training samples: {len(train_texts)}, Testing samples: {len(test_texts)}")
print("✅ Train label distribution:", Counter(train_labels))
print("✅ Test label distribution:", Counter(test_labels))

# Step 5: Load tokenizer
print("[INFO] Loading BERT tokenizer...")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
print("[SUCCESS] Tokenizer loaded.")

# Step 6: Tokenize text data
print("[INFO] Tokenizing training and testing texts...")
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=512)
print("[SUCCESS] Tokenization complete.")

# Step 7: Dataset class
class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

print("[INFO] Creating PyTorch Dataset objects...")
train_dataset = NewsDataset(train_encodings, train_labels)
test_dataset = NewsDataset(test_encodings, test_labels)
print("[SUCCESS] Dataset objects ready.")

# Step 8: Load model
print("[INFO] Loading BERT model for sequence classification...")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
print("[SUCCESS] Model loaded.")

# Step 9: Training arguments (no evaluation_strategy)
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=2,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_dir='./logs',
    logging_steps=10
)

# Step 10: Initialize Trainer
print("[INFO] Initializing Trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# Step 11: Train the model
print("[INFO] Starting training process...")
trainer.train()
print("[SUCCESS] Model training complete.")

# Step 12: Evaluate manually after training
print("[INFO] Running manual evaluation after training...")
eval_result = trainer.evaluate()
# print(f"\n✅ Accuracy on test set: {eval_result['eval_accuracy']:.4f}")

# Step 13: Save model and tokenizer
print("[INFO] Saving model and tokenizer...")
model.save_pretrained("bert_model")
tokenizer.save_pretrained("bert_model")
print("🧠 Model and tokenizer saved in 'bert_model/'")
