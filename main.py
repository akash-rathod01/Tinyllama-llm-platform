"""
Enhanced main.py with improved features
"""
import argparse
import sys
from loguru import logger
from rich.console import Console

from model_manager import ModelManager
from config import Config

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Run custom LLM")
    parser.add_argument('--model', type=str, default=None, help='Model name to load')
    parser.add_argument('--quantized', action='store_true', help='Enable 8-bit quantization')
    parser.add_argument('--prompt', type=str, default=None, help='Prompt for generation')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--max-length', type=int, default=None, help='Maximum generation length')
    parser.add_argument('--temperature', type=float, default=None, help='Sampling temperature')
    parser.add_argument('--stream', action='store_true', help='Enable streaming output')
    
    args = parser.parse_args()
    
    try:
        # Initialize model
        console.print("[bold]Initializing model...[/bold]")
        model_manager = ModelManager(
            model_name=args.model,
            quantized=args.quantized
        )
        console.print("[bold green]✓ Model loaded successfully![/bold green]\n")
        
        # Interactive mode
        if args.interactive:
            from chat import ChatInterface
            chat = ChatInterface(model_manager)
            chat.run()
            return
        
        # Single prompt mode
        if args.prompt:
            prompt = args.prompt
        else:
            prompt = "Write a short story about a robot learning emotions."
        
        console.print(f"[bold cyan]Prompt:[/bold cyan] {prompt}\n")
        
        if args.stream:
            console.print("[bold cyan]Response:[/bold cyan] ", end="")
            for chunk in model_manager.generate_stream(
                prompt=prompt,
                max_length=args.max_length,
                temperature=args.temperature
            ):
                console.print(chunk, end="")
            console.print()
        else:
            with console.status("[bold green]Generating..."):
                response = model_manager.generate(
                    prompt=prompt,
                    max_length=args.max_length,
                    temperature=args.temperature
                )
            console.print(f"[bold cyan]Response:[/bold cyan]\n{response}")
        
        # Show token count
        tokens = model_manager.count_tokens(response if not args.stream else prompt)
        console.print(f"\n[dim]Tokens: {tokens}[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        logger.error(f"Main execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
