## cara jalanin

1. jalanin
```
pip3 install -r requirements.txt
```

2. set up .env.contoh, abis itu ganti namanya jadi ".env"

3. import sql pake
```
mysql -u [username] -p [databasename] < ./sql/sorts.sql
```

4. jalanin
```
flask run
```

5. done, testing API bisa pake postman, login dulu tp sesuai isi dotenv tadi ke route "/auth/login".