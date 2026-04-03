"""
Interactive CLI Chat Interface for Custom LLM Platform
"""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from loguru import logger
from typing import List, Dict

from model_manager import ModelManager
from config import Config

console = Console()

class ChatInterface:
    """Interactive chat interface"""
    
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = "You are a helpful AI assistant."
    
    def build_prompt(self) -> str:
        """Build prompt from conversation history"""
        prompt = f"System: {self.system_prompt}\n\n"
        
        for msg in self.conversation_history[-Config.MAX_CONVERSATION_HISTORY:]:
            role = msg["role"].capitalize()
            content = msg["content"]
            prompt += f"{role}: {content}\n\n"
        
        prompt += "Assistant:"
        return prompt
    
    def chat(self, user_input: str, stream: bool = True) -> str:
        """Process user input and generate response"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Build prompt
        prompt = self.build_prompt()
        
        # Generate response
        if stream and Config.ENABLE_STREAMING:
            response = ""
            console.print("\n[bold cyan]Assistant:[/bold cyan]", end=" ")
            
            for chunk in self.model_manager.generate_stream(prompt=prompt):
                response += chunk
                console.print(chunk, end="")
            
            console.print()  # New line after streaming
        else:
            with console.status("[bold green]Thinking..."):
                full_response = self.model_manager.generate(prompt=prompt)
                # Extract only assistant's response
                response = full_response.split("Assistant:")[-1].strip()
            
            console.print(f"\n[bold cyan]Assistant:[/bold cyan] {response}")
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        console.print("[yellow]Conversation history cleared![/yellow]")
    
    def set_system_prompt(self, prompt: str):
        """Set system prompt"""
        self.system_prompt = prompt
        console.print(f"[green]System prompt updated![/green]")
    
    def show_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            console.print("[yellow]No conversation history yet.[/yellow]")
            return
        
        console.print("\n[bold]Conversation History:[/bold]")
        for i, msg in enumerate(self.conversation_history, 1):
            role = msg["role"].capitalize()
            content = msg["content"]
            console.print(f"\n{i}. [bold]{role}:[/bold] {content}")
    
    def run(self):
        """Run interactive chat loop"""
        console.print(Panel.fit(
            "[bold cyan]Custom LLM Chat Interface[/bold cyan]\n"
            f"Model: {self.model_manager.model_name}\n"
            "Type 'exit' to quit, 'clear' to clear history, 'history' to view history\n"
            "Type 'system: <prompt>' to set system prompt",
            border_style="cyan"
        ))
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]You[/bold green]")
                
                if not user_input.strip():
                    continue
                
                # Handle commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                elif user_input.lower() == 'clear':
                    self.clear_history()
                    continue
                
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                elif user_input.lower().startswith('system:'):
                    new_system_prompt = user_input[7:].strip()
                    self.set_system_prompt(new_system_prompt)
                    continue
                
                # Generate response
                self.chat(user_input, stream=Config.ENABLE_STREAMING)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
                continue
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                logger.error(f"Chat error: {e}")

def main():
    """Main entry point"""
    try:
        console.print("[bold]Loading model...[/bold]")
        
        with console.status("[bold green]Initializing model..."):
            model_manager = ModelManager()
        
        console.print("[bold green]✓ Model loaded successfully![/bold green]\n")
        
        # Create and run chat interface
        chat = ChatInterface(model_manager)
        chat.run()
        
    except Exception as e:
        console.print(f"[bold red]Failed to initialize: {e}[/bold red]")
        logger.error(f"Initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
