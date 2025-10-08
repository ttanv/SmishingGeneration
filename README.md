# Smishing Message Generator

This project is designed to generate a dataset of synthetic smishing (SMS phishing) messages using a large language model (LLM). It utilizes seed data, including real-world phishing examples, to create new and varied smishing attacks. The generation process is guided by a defined JSON schema that categorizes messages based on the attack method and the persuasion technique employed.

## Project Structure

```
├── .idea/                  # IDE configuration files
├── .ipynb_checkpoints/     # Jupyter Notebook checkpoints
├── Untitled.ipynb          # Jupyter Notebook for experimentation
├── default_schema.json     # The default JSON schema for the generated messages
├── output.json             # The output file with the generated smishing messages
├── seed/
│   ├── methods.json        # A JSON file defining different smishing methods
│   ├── phishtank_part*.txt # Text files containing samples of phishing messages
│   ├── phishtank_samples.txt # A collection of phishing message samples
│   ├── seperation_script.py# A script to separate the phishtank_samples.txt into parts
│   └── techniques.json     # A JSON file detailing various persuasion techniques
└── smishing_generator_script.py # The main Python script for generating smishing messages
```

## How it Works

The core of this project is the `smishing_generator_script.py`. This script interacts with a large language model to generate synthetic smishing messages. The process is as follows:

1.  **Seeding**: The script is seeded with real-world phishing examples from the `seed/phishtank_samples.txt` file.
2.  **Schema Definition**: A JSON schema is created based on the defined `methods.json` and `techniques.json` to structure the output data. This schema includes the message content, the smishing method, and the persuasion technique used.
3.  **Generation**: The script sends prompts to the LLM, including the schema and examples, to generate new, unique smishing messages.
4.  **Output**: The newly generated messages are saved in a structured JSON format in the `output.json` file.

The script also has functionality to dynamically update the methods and techniques by querying the LLM, allowing for an evolving dataset.

## Getting Started

### Prerequisites

*   Python 3.x
*   An OpenAI compatible API running locally. The script is configured to connect to `http://localhost:2213/v1`.

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Navigate to the project directory:
    ```bash
    cd <repository-directory>
    ```
3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file is not provided in the original structure, but you would need to install `openai`)*

### Usage

To run the smishing generation script, execute the following command:

```bash
python smishing_generator_script.py
```

You can customize the generation process using the following command-line arguments:

*   `--iterations`: The number of times the message generation loop is run.
*   `--messages_num`: The number of messages to generate in each iteration.

For example:

```bash
python smishing_generator_script.py --iterations 10 --messages_num 20
```

## Files of Interest

*   **`smishing_generator_script.py`**: The main script to run the data generation.
*   **`seed/`**: This directory contains all the initial data.
    *   `phishtank_samples.txt`: Contains real phishing messages used as examples for the LLM.
    *   `methods.json` and `techniques.json`: Define the categories for classifying the generated messages.
*   **`output.json`**: The final output of the generation script, containing the synthetic smishing data.
*   **`default_schema.json`**: Defines the structure for the generated smishing message data.
*   **`Untitled.ipynb`**: A Jupyter Notebook that showcases the development and experimentation process.
