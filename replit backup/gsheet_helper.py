import pygsheets
import pandas as pd


def gsheet_upload(array_link, Sheet, update=False):
  try:
    # Buat DataFrame dari array_link
    df = pd.DataFrame(array_link)

    # Buat objek klien
    client = pygsheets.authorize(
        service_account_file="kajian-ufuk-indonesia-b1e63d302e2e.json")

    # Buka spreadsheet berdasarkan nama/judulnya
    spreadsht = client.open("KUI_analysis_Scraping")

    # Buka worksheet berdasarkan nama/judulnya
    worksht = spreadsht.worksheet_by_title(Sheet)

    if update:
      # Mendapatkan seluruh data di kolom D
      column_D_values = worksht.get_col(4, include_tailing_empty=False)

      # Menghitung jumlah baris yang sudah terisi di kolom D
      num_filled_rows_D = len(column_D_values)
      print(num_filled_rows_D)
      worksht.set_dataframe(df, start=f"A{num_filled_rows_D + 1}")
      worksht.delete_rows(num_filled_rows_D + 1)
    else:
      # Mengunggah DataFrame ke Google Sheets
      worksht.set_dataframe(df, start='A2')
      worksht.delete_rows(2)
    print("Data berhasil diunggah ke Google Sheets!")

  except Exception as e:
    print(f"Error mengunggah ke Google Sheets: {e}")
