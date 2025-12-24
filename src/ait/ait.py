import subprocess
import argparse
import json
import os
from typing import Optional
from openai import OpenAI

def load_config(config_path):
    """
    Loads the configuration from a JSON file.

    Parameters:
    - config_path (str): The path to the configuration file.

    Returns:
    - dict: The configuration settings as a dictionary, or an empty dictionary if the file does not exist.
    """
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def resolve_config_path(config_input):
    """
    Resolves the configuration file path. If a single word is provided,
    it looks for a file named 'ait.WORD.config.json' in the current directory first,
    then in a '.ait' directory in the user's home directory.

    Parameters:
    - config_input (str): The input provided via the command-line argument.

    Returns:
    - str: The resolved path to the configuration file.
    """
    # If it's a keyword, construct the potential filenames
    if not config_input.endswith(".json"):
        config_filename = f"ait.{config_input}.config.json"
    else:
        config_filename = config_input

    # Check in the current directory
    if os.path.exists(config_filename):
        return config_filename

    # Check in the user's home directory under .ait/
    home_directory = os.path.expanduser("~")
    user_config_path = os.path.join(home_directory, ".ait", config_filename)
    if os.path.exists(user_config_path):
        return user_config_path

    # If nothing found, return the filename (it will fail later if non-existent)
    return config_filename

def extract_config_keyword(config_input):
    """Derives the keyword portion from a config selector or path."""
    if not config_input:
        return None

    basename = os.path.basename(config_input)
    if not basename.endswith(".json"):
        return basename

    marker = "ait."
    suffix = ".config.json"
    if basename.startswith(marker) and basename.endswith(suffix):
        keyword = basename[len(marker):-len(suffix)]
        return keyword or None

    return None

def load_context_content(keyword: Optional[str] = None):
    """Loads optional context markdown from the current working directory."""
    candidates = []
    if keyword:
        candidates.append(f".ait.{keyword}.md")
    candidates.append(".ait.md")

    cwd = os.getcwd()
    for filename in candidates:
        candidate_path = os.path.join(cwd, filename)
        if os.path.isfile(candidate_path):
            with open(candidate_path, "r", encoding="utf-8") as context_file:
                return context_file.read()
    return None

def run_git_commands(diff_expression, log_expression):
    """
    Executes git commands to obtain the diff and log outputs.

    Parameters:
    - diff_expression (str): The git diff expression to compare branches or commits.
    - log_expression (str): The git log expression to retrieve commit history.

    Returns:
    - tuple: A tuple containing the diff output and the log output as strings.
    """
    diff_command = ["git", "diff", diff_expression]
    diff_result = subprocess.run(diff_command, capture_output=True, text=True)
    
    log_command = ["git", "log", log_expression, "--pretty=\"format:%h%n%ad%n%s%n%n%b%n---%n\""]
    log_result = subprocess.run(log_command, capture_output=True, text=True)
    
    return diff_result.stdout, log_result.stdout

def collect_tree_snapshot(ref="HEAD"):
    """Collects a repository tree listing using git ls-tree (recursively)."""
    tree_command = ["git", "ls-tree", "--name-only", "-r", ref]
    tree_result = subprocess.run(tree_command, capture_output=True, text=True)
    if tree_result.returncode == 0:
        return tree_result.stdout.strip()
    return None

def generate_text_from_git_data(
    diff_output,
    log_output,
    system_prompt,
    user_prompt,
    model,
    temperature,
    api_key,
    max_tokens=None,
    max_completion_tokens=None,
    context_text: Optional[str] = None,
    tree_summary: Optional[str] = None,
):
    """
    Generates text using the OpenAI API based on git diff and log outputs.

    Parameters:
    - diff_output (str): The output from the git diff command.
    - log_output (str): The output from the git log command.
    - system_prompt (str): The system-level prompt setting the context for the AI.
    - user_prompt (str): The user-level prompt guiding the AI's response.
    - model (str): The OpenAI model to use for text generation.
    - max_tokens (int): The maximum number of tokens for the AI response.
    - temperature (float): The sampling temperature to control creativity.
    - api_key (str): The API key for accessing the OpenAI API.

    Returns:
    - str: The generated text from the AI.
    """
    # Create OpenAI client
    client = OpenAI(api_key=api_key)

    # Construct the messages for the AI
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Here is the git diff output:\n{diff_output}"},
        {"role": "user", "content": f"Here is the git log output:\n{log_output}"},
    ]

    if context_text:
        messages.append({
            "role": "user",
            "content": f"Here is additional context from the .ai markdown file:\n{context_text}"
        })

    if tree_summary:
        messages.append({
            "role": "user",
            "content": f"Here is the repository tree summary from 'git ls-tree HEAD':\n{tree_summary}"
        })

    messages.append({"role": "user", "content": user_prompt})
    
    # Generate the text using OpenAI's API
    if max_tokens:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
    elif max_completion_tokens:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature
        )
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
    
    # Extract and return the generated text
    generated_text = response.choices[0].message.content.strip() # type: ignore
    return generated_text

def main():
        # Default configuration file path
    default_config_path = "ait.config.json"
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate text based on Git diff and log using OpenAI API.")
    parser.add_argument('single_arg', nargs='?', help="A single argument that can be a config file or a keyword for 'ait.KEYWORD.config'.")
    parser.add_argument('--config', type=str, help="Path to the JSON config file or a keyword for 'ait.KEYWORD.config'.")
    parser.add_argument('--api_key', type=str, help="Your OpenAI API key.")
    parser.add_argument('--diff_expression', type=str, help="The git diff expression to use. Default is 'main...'.")
    parser.add_argument('--log_expression', type=str, help="The git log expression to use. Default is 'main...'.")
    parser.add_argument('--system_prompt', type=str, help="The system prompt to set the behavior of the assistant.")
    parser.add_argument('--prompt', type=str, help="The prompt to guide the description creation.")
    parser.add_argument('--model', type=str, help="The OpenAI model to use. Default is 'gpt-4'.")
    parser.add_argument('--max_tokens', type=int, help="Maximum tokens for the API response. Default is None.")
    parser.add_argument('--max_completion_tokens', type=int, help="Maximum tokens for the API response. Default is None.")
    parser.add_argument('--temperature', type=float, help="Sampling temperature for the model. Default is 0.7.")
    parser.add_argument('--tree', dest='include_tree', action='store_true', help="Include a repo overview via 'git ls-tree HEAD'.")
    parser.add_argument('--no-tree', dest='include_tree', action='store_false', help="Disable the repo overview, overriding config.")
    parser.set_defaults(include_tree=None)
    
    args = parser.parse_args()

    # Determine config path
    if args.config:
        config_path = resolve_config_path(args.config)
    elif args.single_arg:
        config_path = resolve_config_path(args.single_arg)
    else:
        config_path = default_config_path

    resolved_config_keyword = extract_config_keyword(config_path)

    # Load configuration settings
    config = load_config(config_path)
    
    # Override config with command-line arguments if provided
    api_key = args.api_key or config.get('api_key')
    diff_expression = args.diff_expression or config.get('diff_expression', 'main...')
    log_expression = args.log_expression or config.get('log_expression', 'main...')
    system_prompt = args.system_prompt or config.get('system_prompt', "You are a helpful assistant that creates pull request descriptions.")
    user_prompt = args.prompt or config.get('prompt', "Please create a pull request description based on these changes.")
    model = args.model or config.get('model', 'gpt-4')
    max_tokens = args.max_tokens or config.get('max_tokens', None)
    max_completion_tokens = args.max_completion_tokens or config.get('max_completion_tokens', None)
    temperature = args.temperature or config.get('temperature', 0.7)
    include_tree = config.get('include_tree', False) if args.include_tree is None else args.include_tree

    # Ensure API key is provided
    if not api_key:
        raise ValueError("API key must be provided either in the config file or as an argument.")
    
    # Execute git commands and get the outputs
    diff_output, log_output = run_git_commands(diff_expression, log_expression)

    context_text = load_context_content(resolved_config_keyword)
    tree_summary = collect_tree_snapshot() if include_tree else None
    
    # Generate text based on the git data
    generated_text = generate_text_from_git_data(
        diff_output,
        log_output,
        system_prompt,
        user_prompt,
        model,
        temperature,
        api_key,
        max_tokens,
        max_completion_tokens,
        context_text=context_text,
        tree_summary=tree_summary
    )
    
    # Output the generated text
    print("\n" + generated_text + "\n")

