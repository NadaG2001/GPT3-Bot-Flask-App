from flask import Flask, render_template, request
import openai
import time

app = Flask(__name__)
openai.api_key = 'you-API-Key-here'

data = {
    "greetings": [
        "Hi, how can I help you today?",
        "Hello there! What can I do for you?",
        "Hey, what's up?",
        "Greetings! How may I assist you?",
        "Good day! How can I be of service?",
    ],
    "farewells": [
        "Goodbye! Have a great day.",
        "Farewell! See you soon.",
        "Take care!",
        "Bye! Come back anytime.",
        "Have a great day ahead!",
    ],
}


def bot(prompt, engine='text-davinci-002', temperature=0.9, max_tokens=500, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.9, stop=[" User:", " AI:"]):
    try:
        if "hi" in prompt.lower():
            response = openai.Completion.create(
                engine=engine,
                prompt=data["greetings"],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop
            )
        elif "bye" in prompt.lower():
            response = openai.Completion.create(
                engine=engine,
                prompt=data["farewells"],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop
            )
        else:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop
            )
        text = response.choices[0].text.strip()
        return text
    except Exception as e:
        return "GPT-3 Error: {}".format(e)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    start_time = time.time()
    bot_response = bot(prompt=user_text)
    response_time = time.time() - start_time
    return str(bot_response)


if __name__ == "__main__":
    app.run(debug=True)
