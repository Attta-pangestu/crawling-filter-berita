from datetime import datetime, timedelta

def convert_date_filter_bing(date_string):
  reference_date = datetime(1970, 1, 11)
  target_date = datetime.strptime(date_string, '%d/%m/%Y')
  days_difference = (target_date - reference_date).days
  return days_difference


# Contoh penggunaan
days_values = [10, 100, 200, 300, 400, 800, 1600, 3200]

date_values = [
    '11/01/2018', '11/04/1970', '20/07/1970', '28/10/1970', '05/02/1971',
    '11/03/1972', '20/05/1974', '06/10/1978'
]

for date_str in date_values:
  days_since_reference = convert_date_to_days(date_str)
  print(f"{date_str} = {days_since_reference}")
