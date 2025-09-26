"""Interactive Weather App"""

import from byllm.llm { Model }

# Initialize Gemini LLM
glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);

# Function to fetch weather using Gemini
def get_weather(city: str) -> str by llm();

walker WeatherApp {
    can start with `root entry;
}

with entry:__main__ {
    root spawn WeatherApp();
}
