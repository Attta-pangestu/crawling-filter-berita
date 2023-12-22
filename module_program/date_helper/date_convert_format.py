from datetime import datetime

def ambil_tiga_kata_pertama(input_tanggal):
    kata_kata = input_tanggal.split()
    tiga_kata_pertama = kata_kata[:3]

    # Jika tiga kata pertama adalah angka (tanggal), tambahkan kata bulan yang sesuai
    if tiga_kata_pertama[0].isdigit():
        tiga_kata_pertama[1] = tiga_kata_pertama[1][:3]  # Ambil tiga karakter pertama dari nama bulan

    return ' '.join(tiga_kata_pertama)


def convert_date_format(input_date):
    input_date = ambil_tiga_kata_pertama(input_date)
    # Buat kamus untuk mapping nama bulan dalam bahasa Indonesia ke bahasa Inggris
    bulan_mapping = {
        'Jan': 'Jan',
        'Feb': 'Feb',
        'Mar': 'Mar',
        'Apr': 'Apr',
        'Mei': 'May',  # Ganti 'Mei' ke 'May'
        'Jun': 'Jun',
        'Jul': 'Jul',
        'Agu': 'Aug',  # Ganti 'Agu' ke 'Aug'
        'Sep': 'Sep',
        'Okt': 'Oct',
        'Nov': 'Nov',
        'Des': 'Dec'
    }

    # Ubah nama bulan dalam input_date menjadi bahasa Inggris
    for id, en in bulan_mapping.items():  # Perhatikan urutan en, id dibalik
        input_date = input_date.replace(id, en)

    try:
        # Cek apakah input_date memiliki format jam (HH:MM)
        datetime.strptime(input_date, "%d %b %Y %H:%M")
        format_tanggal = "%d %b %Y %H:%M"
    except ValueError:
        # Jika tidak memiliki format jam, gunakan format tanggal saja
        format_tanggal = "%d %b %Y"

    # Coba parsing tanggal dan waktu
    date_object = datetime.strptime(input_date, format_tanggal)
    output_date = date_object.strftime("%m/%d/%Y")

    return output_date
