# AI-Generated Messages from Git Diffs and Logs

This script uses the OpenAI API to generate text based on the outputs of `git diff` and `git log` commands. It can be particularly useful for creating pull request descriptions, commit messages, or any other narrative that requires summarizing changes between different branches or commits in a Git repository.

## Features

- **Automated Message Generation**: The script generates text based on Git diffs and logs using OpenAI's GPT models.
- **Customizable Prompts**: You can configure both the system and user prompts to guide the generated text.
- **Flexible Configuration**: Supports custom configuration through JSON files, allowing for different setups and use cases.
- **Easy Configuration Management**: The script can load configurations via command-line arguments or shorthand keywords, making it convenient to switch between different setups.

## Prerequisites

- **Python 3.x**
- **Git**: Ensure that Git is installed and available in your system's PATH.
- **OpenAI API Key**: You need an OpenAI API key to use the GPT models.

## Installation

Clone the repository and navigate to the directory:

```bash
git clone https://github.com/your-repository.git
cd your-repository
```

Install the necessary Python packages:

```bash
pip install openai
```

## Usage

### Basic Usage

To generate a message based on the current branch's diff and log against the main branch, simply run:

```bash
python ait.py
```

This will use the default configuration file (`ait.config.json`) located in the current directory.

### Using Custom Configurations

You can specify a different configuration file using the `--config` option:

```bash
python ait.py --config custom_config.json
```

#### Shorthand Configuration Selection

Alternatively, if you only provide a keyword, the script will look for a file named `ait.<KEYWORD>.config.json` in the current directory:

```bash
python ait.py --config KAI
```

This command will look for a configuration file named `ait.KAI.config`.

### Command-Line Options

- `--config`: Path to a JSON config file or a keyword to identify a specific config (`ait.<KEYWORD>.config`). Default is `ait.config.json`.
- `--api_key`: Your OpenAI API key. If not provided, the script looks for it in the config file.
- `--diff_expression`: The Git diff expression to use. Default is `main...`.
- `--log_expression`: The Git log expression used to retrieve the commit history. Default is `main...`.
- `--system_prompt`: The system prompt to set the behavior of the assistant.
- `--prompt`: The user prompt to guide the description creation.
- `--model`: The model to use, such as `"gpt-4"`. You can change this depending on the available models in your API.
- `--max_tokens`: The maximum number of tokens (words or parts of words) in the API response. Default is `150`.
- `--temperature`: Controls the randomness or creativity of the model's output. Lower values make the output more deterministic, while higher values make it more random. Default is `0.7`.

### Example Config Files

See the [ait.commit.sample.config.json](ait.commit.sample.config.json) and [ait.pull_request.sample.config.json](ait.pull_request.sample.config.json) files for examples of configuration files.

### Error Handling

The script will raise an error if the API key is not provided either via the command-line argument or the configuration file.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
