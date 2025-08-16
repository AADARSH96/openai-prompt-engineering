# openai-prompt-eng Prompt Engineering Techniques Comparison: GPT-5 vs Claude Sonnet 4

A simple benchmarking tool to compare the responses of **OpenAI GPT-5** and **Anthropic Claude Sonnet 4** on a suite of classic and advanced prompt engineering techniques. Designed for LLM practitioners, educators, and data engineers who want to assess model behavior side by side.

---

## Features

- **Covers Core Prompt Techniques:** Basic prompting, few-shot, chain of thought, role-based, structured, zero-shot CoT, constraint-based, and template-based.
- **Direct API Calls:** Uses official OpenAI and Anthropic SDKs (no intermediaries).
- **Automatic CSV Export:** Saves each run to a timestamped CSV in your current folder.
- **Response Analytics:** Adds columns for response length, presence of stepwise reasoning, and error detection.
- **CLI Summary:** Prints a handy qualitative summary after each benchmark run.

---

## Quickstart

1. **Requirements**

   - Python 3.8+
   - [openai](https://github.com/openai/openai-python), [anthropic](https://github.com/anthropics/anthropic-sdk-python), [pandas](https://pandas.pydata.org/)
   
   Install dependencies with:
```

pip install openai anthropic pandas

```

2. **API Keys**

- Find your API keys on [OpenAI dashboard](https://platform.openai.com/) and [Anthropic console](https://console.anthropic.com/).
- Open `prompt_engineering_comparison.py` in your editor.
- Paste keys into the variables at the top:
  ```
  OPENAI_API_KEY = 'sk-...'
  ANTHROPIC_API_KEY = 'claude-...'
  ```

3. **Run the Script**

```

python prompt_engineering_comparison.py

```

- **Process:**  
  The script runs each prompt through both models, collects results with rate limiting, and writes a CSV to the current directory named `prompt_engineering_comparison_<timestamp>.csv`.
- **Summary:**  
  After all prompts are tested, the script prints a side-by-side summary for rapid review.

---

## Output

- **CSV Columns:**
- `technique` (Prompting method used)
- `prompt` (The input sent to the models)
- `gpt5_response`, `claude_response`
- `timestamp` (when tested)
- `gpt5_length`, `claude_length` (response lengths in characters)
- `length_difference` (character count difference)
- `gpt5_has_steps`, `claude_has_steps` (flag if response uses step-by-step logic)
- `gpt5_error`, `claude_error` (flag if an error occurred)
- **CSV Example:**
- `prompt_engineering_comparison_20250816_112212.csv`

---
ineering