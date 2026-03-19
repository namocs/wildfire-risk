def get_wind_speed():
    try:
        value = GPIO.input(WIND_PIN)
        print(f"Wind sensor digital: {value}")
        return float(value)
    except Exception as e:
        print(f"Wind speed read error: {e}")
        return 0.0