"""
Enhanced training script with better features
"""
import argparse
import sys
from pathlib import Path
from loguru import logger
from rich.console import Console
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
from config import Config

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Fine-tune custom LLM")
    parser.add_argument('--model', type=str, default=None, help='Model name to fine-tune')
    parser.add_argument('--data', type=str, default='data/sample.txt', help='Training data file')
    parser.add_argument('--output', type=str, default='./fine_tuned_model', help='Output directory')
    parser.add_argument('--epochs', type=int, default=None, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=None, help='Training batch size')
    parser.add_argument('--learning-rate', type=float, default=None, help='Learning rate')
    
    args = parser.parse_args()
    
    try:
        model_name = args.model or Config.MODEL_NAME
        epochs = args.epochs or Config.NUM_EPOCHS
        batch_size = args.batch_size or Config.BATCH_SIZE
        learning_rate = args.learning_rate or Config.LEARNING_RATE
        
        console.print(f"[bold]Fine-tuning {model_name}[/bold]")
        console.print(f"Data: {args.data}")
        console.print(f"Epochs: {epochs}, Batch size: {batch_size}, LR: {learning_rate}\n")
        
        # Check if data file exists
        if not Path(args.data).exists():
            console.print(f"[red]Error: Data file '{args.data}' not found![/red]")
            console.print("[yellow]Please add your training data to the data/ folder.[/yellow]")
            sys.exit(1)
        
        # Load tokenizer and model
        console.print("[bold]Loading tokenizer and model...[/bold]")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=Config.MODEL_CACHE_DIR if Config.USE_CACHE else None
        )
        
        console.print("[green]✓ Model loaded[/green]")
        
        # Load dataset
        console.print(f"[bold]Loading dataset from {args.data}...[/bold]")
        dataset = load_dataset("text", data_files={"train": args.data})
        console.print(f"[green]✓ Loaded {len(dataset['train'])} examples[/green]")
        
        # Tokenize dataset
        def tokenize_function(examples):
            return tokenizer(
                examples["text"],
                truncation=True,
                padding="max_length",
                max_length=512
            )
        
        console.print("[bold]Tokenizing dataset...[/bold]")
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset["train"].column_names
        )
        console.print("[green]✓ Dataset tokenized[/green]")
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=args.output,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=Config.GRADIENT_ACCUMULATION_STEPS,
            num_train_epochs=epochs,
            learning_rate=learning_rate,
            logging_dir="./logs",
            logging_steps=10,
            save_steps=Config.SAVE_STEPS,
            save_total_limit=3,
            fp16=True,  # Mixed precision training
            report_to="none",  # Disable wandb/tensorboard
            warmup_steps=100,
            weight_decay=0.01,
        )
        
        # Create trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset["train"],
            data_collator=data_collator,
        )
        
        # Train
        console.print("\n[bold green]Starting training...[/bold green]")
        trainer.train()
        
        # Save model
        console.print(f"\n[bold]Saving fine-tuned model to {args.output}...[/bold]")
        trainer.save_model(args.output)
        tokenizer.save_pretrained(args.output)
        
        console.print("[bold green]✓ Training complete![/bold green]")
        console.print(f"[cyan]Model saved to: {args.output}[/cyan]")
        console.print(f"[cyan]To use: python main.py --model {args.output}[/cyan]")
        
    except Exception as e:
        console.print(f"[bold red]Training failed: {e}[/bold red]")
        logger.error(f"Training error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
