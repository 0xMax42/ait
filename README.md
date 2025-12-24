![Time](https://waka.mpassarello.de/api/badge/MaxP/interval:any/project:Ait?label=Project%20time)

<p align="center">
  <img width="600" src="./docs/ait.webp">
</p>

# AI-Generated Messages from Git Diffs and Logs

This script uses the OpenAI API to generate text based on the outputs of `git diff` and `git log` commands. It can be particularly useful for creating pull request descriptions, commit messages, or any other narrative that requires summarizing changes between different branches or commits in a Git repository.

## Features

- **Automated Message Generation**: The script generates text based on Git diffs and logs using OpenAI's GPT models.
- **Customizable Prompts**: You can configure both the system and user prompts to guide the generated text.
- **Flexible Configuration**: Supports custom configuration through JSON files, allowing for different setups and use cases.
- **Easy Configuration Management**: The script can load configurations via command-line arguments or shorthand keywords, making it convenient to switch between different setups.
- **Context-aware Summaries**: Optional `.ai.<keyword>.md` or `.ai.md` files from the working directory can be injected as additional context for higher quality output.
- **Repository Tree Snapshot**: Toggle a `git ls-tree HEAD` overview to share the current top-level structure alongside diffs and logs.
- **Clipboard Export**: Optionally copy the generated text directly to your Wayland clipboard via `wl-copy`.

## Prerequisites

- **Python 3.x**
- **Git**: Ensure that Git is installed and available in your system's PATH.
- **OpenAI API Key**: You need an OpenAI API key to use the GPT models.

## Installation

Clone the repository and navigate to the directory:

```bash
git clone https://github.com/PxaMMaxP/ait
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
python ait.py --config custom
```

This command will look for a configuration file named `ait.custom.config`.

The same keyword is also used to search the working directory for `.ai.<KEYWORD>.md` context files before falling back to `.ai.md`.

### Fallback Configuration File search

As a fallback, if no configuration file is found, the script will search for it in the user's home directory under `~\.ait\*`.

You can also provide a user wide configuration file by placing it in the `~\.ait\` directory.

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
- `--tree` / `--no-tree`: Enable or disable inclusion of the `git ls-tree HEAD` summary, overriding the config file.
- `--copy` / `--no-copy`: Enable or disable copying the generated text to the clipboard via `wl-copy`.

### Example Config Files

See the [ait.commit.sample.config.json](ait.commit.sample.config.json) and [ait.pull_request.sample.config.json](ait.pull_request.sample.config.json) files for examples of configuration files, including the optional `include_tree` and `copy_to_clipboard` toggles.

### Error Handling

The script will raise an error if the API key is not provided either via the command-line argument or the configuration file.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
