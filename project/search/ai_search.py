from openai import OpenAI


# Set your OpenAI GPT-3 API key
client = OpenAI(
    api_key = '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'
)

# Your prompt or input to the model
prompt = "Translate the following English text to French:"


def explain_article(study):
    # Call the OpenAI API to generate a response
    prompt = "Explain this study and its conclusion like i'm a 12 years old kid" + study
    explain_abstract = client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model = "gpt-3.5-turbo",
    )

    print(explain_abstract.choices[0].message.content)
    return explain_abstract.choices[0].message.content

explain_article('Hi!')