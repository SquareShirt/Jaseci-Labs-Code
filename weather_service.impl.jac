impl WeatherApp.start {
    print("Welcome to the Jac Weather App!");
    print("Type 'quit' to exit.");

    while True {
        print("Which city do you live in?");
        city = input("> ");

        if city == "quit" {
            print("Goodbye!");
            break;
        }

        weather = get_weather(city);
        print(f"Today's weather in {city}: " + weather);
    }

    disengage;
}
