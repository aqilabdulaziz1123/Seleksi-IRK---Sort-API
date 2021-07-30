# Seleksi-IRK---Sort-API

## Cara menjalankan program
1. Jalankan mysql lalu buat database di local dengan nama `sort_api` (command: ```create database sort_api;```)
2. Restore sebuah database dari file eksternal (import) dengan command:
```sudo mysql -u {username} -p sort_api < sort_api.sql```
Catatan: pastikan sudah berada di satu direktori dengan file eksternalnya.
2. Konfigurasikan host, user, dan password pada file `database.py` sesuai konfigurasi local:
```
app.config['MYSQL_HOST'] = '<nama host>'
app.config['MYSQL_USER'] = '<nama user>'
app.config['MYSQL_PASSWORD'] = '<password>'
```
3. Jalankan program mengetikkan command berikut pada terminal: `python3 app.py`
## Author
13519040 - Shafira Naya Aprisadianti