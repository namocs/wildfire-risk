from datetime import datetime

get_time = datetime.now().replace(microsecond=0)

print(get_time)