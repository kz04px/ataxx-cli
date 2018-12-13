import settings_window
import game_window
import option

if __name__ == "__main__":
    # Create settings
    settings = {}
    settings["Black"]   = option.Option(0, ["Human", "CPU"])
    settings["White"]   = option.Option(1, ["Human", "CPU"])
    settings["Difficulty"] = option.Option(0, ["Easy", "Medium", "Hard", "Extreme"])
    settings["Time"]       = option.Option(0, ["None", "1m+0s", "3m+2s", "10m+5s"])
    settings["Board"]      = option.Option(0, ["Default", "4 corners"])

    while True:
        r = settings_window.show(settings)
        if not r:
            break

        r = game_window.show(settings)
        if not r:
            break
