import requests

def get_provinsi_data():
    url_provinsi = 'https://wilayah.id/api/provinces.json'
    response_provinsi = requests.get(url_provinsi)

    if response_provinsi.status_code == 200:
        data_provinsi = response_provinsi.json()['data']
        return data_provinsi
    else:
        print(f"Failed to retrieve provinsi data. Status code: {response_provinsi.status_code}")
        return None

def get_kabupaten_data(provinsi_code):
    url_kabupaten = f'https://wilayah.id/api/regencies/{provinsi_code}.json'
    response_kabupaten = requests.get(url_kabupaten)

    if response_kabupaten.status_code == 200:
        data_kabupaten = response_kabupaten.json()['data']
        return data_kabupaten
    else:
        print(f"Failed to retrieve kabupaten data. Status code: {response_kabupaten.status_code}")
        return None

def get_kecamatan_data(kabupaten_code):
    url_kecamatan = f'https://wilayah.id/api/districts/{kabupaten_code}.json'
    response_kecamatan = requests.get(url_kecamatan)

    if response_kecamatan.status_code == 200:
        data_kecamatan = response_kecamatan.json()['data']
        return data_kecamatan
    else:
        print(f"Failed to retrieve kecamatan data. Status code: {response_kecamatan.status_code}")
        return None

def main():
    # Mendapatkan data provinsi
    provinsi_data = get_provinsi_data()

    if provinsi_data:
        # Menampilkan daftar provinsi
        print("Daftar Provinsi:")
        for provinsi in provinsi_data:
            print(f"Code: {provinsi['code']}, Nama: {provinsi['name']}")

        # Meminta input user untuk memilih provinsi berdasarkan nama
        provinsi_nama_input = input("Masukkan nama provinsi yang ingin dijelajahi: ")

        # Mendapatkan data provinsi berdasarkan nama
        provinsi_data_input = next((provinsi for provinsi in provinsi_data if provinsi['name'].lower() == provinsi_nama_input.lower()), None)

        if provinsi_data_input:
            # Mendapatkan data kabupaten berdasarkan provinsi
            kabupaten_data = get_kabupaten_data(provinsi_data_input['code'])

            if kabupaten_data:
                # Menampilkan daftar kabupaten
                print("\nDaftar Kabupaten/Kota:")
                list_kabupaten = [kabupaten['name'] for kabupaten in kabupaten_data]
                print(list_kabupaten)

                # Mendapatkan data kecamatan dari berbagai kabupaten
                list_kecamatan = []
                for kabupaten in kabupaten_data:
                    kecamatan_data = get_kecamatan_data(kabupaten['code'])

                    if kecamatan_data:
                        # Menambahkan kecamatan ke list
                        list_kecamatan.extend([kecamatan['name'] for kecamatan in kecamatan_data])
                    else:
                        print(f"Gagal mendapatkan data kecamatan untuk {kabupaten['name']}")

                # Menampilkan daftar kecamatan yang digabungkan
                print(f"\nDaftar Kecamatan (digabungkan dari berbagai kabupaten):")
                print(list_kecamatan)

            else:
                print(f"Gagal mendapatkan data kabupaten/kota untuk provinsi {provinsi_nama_input}")

        else:
            print(f"Provinsi dengan nama {provinsi_nama_input} tidak ditemukan.")

if __name__ == "__main__":
    main()
