<a id="readme-top"></a>

<div align="center">
    <a href="https://github.com/Infornographie/SnakAI">
        <img src="images/logo.png" alt="Logo" width="206" height="218">
    </a>
    <h3 align="center">SnakAI</h3>
    <p align="center">
        A toy AI agent in python language. It can answer one-shot questions and correct basic python code. Set to work with Google Gen AI model "gemini-2.0-flash-001" free version.
        It's the third guided project in the Boot.Dev backend programming course. 
    </p>
</div>

### Built with

[![Python3][Python3.js]][Python3-url]

## Getting Started

This is a toy AI Agent. It should be used with great care as it can write files and access and prompt the content of the filesystem and files. It is set to only work in a woring directory but still.

### Installation

You need an API key from [Google AI Studio](https://aistudio.google.com/). 
You need to create a `.env` file in the root directory of SnakAI, and add `GEMINI_API_KEY=your-api-key` inside.

By default, SnakAI is set to work in the `calculator` folder on `calculator.py`. To work on other files, you need to add the folder containing your *.py files in the root directory of SnakAI, and change a `config.py` variable to `WORKING_DIRECTORY="./your_directory"`.

### Usage

You need to launch main.py with your question between quotation marks.
Example: `run main.py "your question"`
You can also add the `--verbose` argument to get more information on token usage.

<p align="right">(<a href="#readme-top">back to top</a>)</p>