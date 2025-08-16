#!/usr/bin/env python3
"""
Prompt Engineering Techniques Comparison: GPT-5 vs Claude Sonnet 4
Compares responses and saves results to CSV using pandas
"""

import openai
import anthropic
import pandas as pd
import time
from datetime import datetime

# API Configuration
OPENAI_API_KEY = ''

ANTHROPIC_API_KEY = ''


def initialize_clients():
    """Set up API clients"""
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return openai_client, anthropic_client


def query_gpt5(client, prompt):
    """Call GPT-5 with latest API parameters"""
    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}]
        )
        print("hello",response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def query_claude(client, prompt):
    """Call Claude Sonnet 4 with latest API parameters"""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=10000,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"


def run_prompt_tests(openai_client, anthropic_client):
    """Execute all prompt engineering tests and collect results"""

    # Define test cases
    test_cases = [
        {
            "technique": "Basic Prompting",
            "prompt": "Write a haiku about coding in Python."
        },
        {
            "technique": "Few-Shot Learning",
            "prompt": """Classify emotions in these sentences:

Sentence: "I'm thrilled about my promotion!"
Emotion: Joy

Sentence: "This traffic is making me late again."
Emotion: Frustration

Sentence: "I can't believe I forgot my anniversary."
Emotion: ?"""
        },
        {
            "technique": "Chain of Thought",
            "prompt": """Calculate compound interest step by step:
Principal: $5,000, Rate: 7% annually, Time: 3 years

Show:
1. Year 1 calculation
2. Year 2 calculation  
3. Year 3 calculation
4. Total interest earned"""
        },
        {
            "technique": "Role-Based Prompting",
            "prompt": """You are a pirate captain from the 1700s who just discovered Python programming.

Explain what a 'for loop' is using your pirate vocabulary."""
        },
        {
            "technique": "Structured Instructions",
            "prompt": """Create a restaurant review with this exact format:

🏪 Name: [Restaurant Name]
⭐ Rating: [1-5 stars]
💰 Price: [$/$$/$$$]
🍽️ Cuisine: [Type]
📝 Review: [2-3 sentences]
👍 Best: [Recommendation]
❌ Skip: [What to avoid]

Write for: Italian restaurant "Nonna's Kitchen\""""
        },
        {
            "technique": "Zero-Shot CoT",
            "prompt": """What are the top 3 factors for mobile app success in 2025?

Think through this step by step."""
        },
        {
            "technique": "Constraint-Based",
            "prompt": """Explain machine learning in exactly 100 words.

Requirements:
- Use everyday language (no jargon)
- Include 2 real-world examples
- End with a question
- Confirm it's exactly 100 words"""
        },
        {
            "technique": "Template-Based",
            "prompt": """Fill this job posting template:

POSITION: [Job Title]
COMPANY: [Company Name]
RESPONSIBILITIES: [3 bullet points]
REQUIREMENTS: [3 bullet points]
SALARY: [Range]

Create for: Senior Data Scientist at tech startup"""
        }
    ]

    results = []

    print("🚀 Running Prompt Engineering Comparison...")
    print(f"Testing {len(test_cases)} techniques with both models\n")

    for i, test_case in enumerate(test_cases, 1):
        technique = test_case["technique"]
        prompt = test_case["prompt"]

        print(f"[{i}/{len(test_cases)}] Testing: {technique}")

        # Get responses from both models
        gpt5_response = query_gpt5(openai_client, prompt)
        time.sleep(10)  # Rate limiting

        claude_response = query_claude(anthropic_client, prompt)
        time.sleep(10)  # Rate limiting

        # Store results
        results.append({
            "technique": technique,
            "prompt": prompt,
            "gpt5_response": gpt5_response,
            "claude_response": claude_response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print(f"✅ Completed: {technique}\n")

    return results


def analyze_responses(df):
    """Add basic analysis columns to the dataframe"""

    # Response length analysis
    df['gpt5_length'] = df['gpt5_response'].str.len()
    df['claude_length'] = df['claude_response'].str.len()
    df['length_difference'] = df['gpt5_length'] - df['claude_length']

    # Simple keyword analysis
    df['gpt5_has_steps'] = df['gpt5_response'].str.contains('step', case=False, na=False)
    df['claude_has_steps'] = df['claude_response'].str.contains('step', case=False, na=False)

    # Error detection
    df['gpt5_error'] = df['gpt5_response'].str.contains('Error:', na=False)
    df['claude_error'] = df['claude_response'].str.contains('Error:', na=False)

    return df


def save_results_to_csv(results):
    """Convert results to DataFrame and save to CSV"""

    # Create DataFrame
    df = pd.DataFrame(results)

    # Add analysis columns
    df = analyze_responses(df)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prompt_engineering_comparison_{timestamp}.csv"

    # Save to CSV
    df.to_csv(filename, index=False)

    print(f"📊 Results saved to: {filename}")
    print(f"📈 Total comparisons: {len(df)}")
    print(f"📏 Average response lengths:")
    print(f"   GPT-5: {df['gpt5_length'].mean():.0f} characters")
    print(f"   Claude: {df['claude_length'].mean():.0f} characters")

    # Show any errors
    gpt5_errors = df['gpt5_error'].sum()
    claude_errors = df['claude_error'].sum()
    if gpt5_errors > 0 or claude_errors > 0:
        print(f"⚠️  Errors found - GPT-5: {gpt5_errors}, Claude: {claude_errors}")

    return df


def display_summary(df):
    """Show a quick summary of the comparison"""
    print("\n" + "=" * 60)
    print("📋 COMPARISON SUMMARY")
    print("=" * 60)

    for _, row in df.iterrows():
        print(f"\n🔬 {row['technique']}")
        print("-" * 40)
        print(f"Prompt: {row['prompt'][:100]}...")
        print(f"\nGPT-5 ({row['gpt5_length']} chars): {row['gpt5_response'][:150]}...")
        print(f"\nClaude ({row['claude_length']} chars): {row['claude_response'][:150]}...")
        print("-" * 40)


def main():
    """Main execution flow"""
    print("🎯 PROMPT ENGINEERING COMPARISON")
    print("GPT-5 vs Claude Sonnet 4")
    print("Results will be saved to CSV file\n")

    try:
        # Initialize API clients
        print("🔧 Setting up API clients...")
        openai_client, anthropic_client = initialize_clients()

        # Run all tests
        print("🧪 Running prompt engineering tests...")
        results = run_prompt_tests(openai_client, anthropic_client)

        # Save to CSV with analysis
        print("💾 Saving results and analysis...")
        df = save_results_to_csv(results)

        # Show summary
        print("📖 Displaying summary...")
        display_summary(df)

        print("\n✅ Comparison complete!")
        print("📁 Check the generated CSV file for detailed results")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🛠️ Setup checklist:")
        print("1. Install: pip install openai anthropic pandas")
        print("2. Add your API keys to the variables at the top")
        print("3. Ensure you have API access and credits")


if __name__ == "__main__":
    main()