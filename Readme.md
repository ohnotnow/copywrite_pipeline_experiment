# Blog Post Generator using LLMs

This project is a Python script designed to create blog posts on a given topic using Large Language Models (LLMs). It can optionally generate multiple variations of a blog post and select the best one based on a set of criteria.

## Features

- Generates blog post outlines
- Writes complete blog posts based on the outlines
- Fine-tunes the generated blog posts for better readability and engagement
- Selects the best blog post from multiple variations

## Installation

### Requirements

- Python 3.x
- Virtual environment (venv)
- Required Python packages (listed in `requirements.txt`)

### Instructions

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment and activate it:**

    On MacOS and Ubuntu:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    On Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the script

To generate a blog post on a given topic, you can run the script from the command line with the following options:

- `--topic` : Specify the topic of the blog post.
- `--number` : Number of variations to generate (only one final 'best' blog post will be saved).
- `--extra-context` : Extra context to provide to the model.

Example:

```bash
python main.py --topic "Benefits of Remote Work" --number 3 --extra-context "focusing on productivity and work-life balance"
```

If no topic is provided through the `--topic` option, the script will prompt you to enter a topic interactively.

### Options and Flags

- **`--topic`**: The main topic of the blog post. If not provided, you will be prompted to enter it.
- **`--number`**: The number of variations of the blog post to generate. Default is 1.
- **`--extra-context`**: Additional context to be included in the blog post.

### Output

The best blog post is saved as a markdown file in the format `YYYY-MM-DD_<topic>.md` in the current directory.

## License

This project is licensed under the MIT License.
