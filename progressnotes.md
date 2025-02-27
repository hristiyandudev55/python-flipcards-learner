# NOTES WHAT I DID ON 23/24/25 February:

1. **Migrated the database** from SQLite to PostgreSQL using _psycopg2-binary_.
* Created a migrate.load file, e.g.:
  
```
LOAD DATABASE
FROM sqlite:///Users/a516095/Documents/GitHub/flip-cards/python-flipcards-learner/flipcards.db
INTO postgresql://a516095@localhost/flipnlearn

WITH create tables,
     include drop,
     create indexes,
     reset sequences;
```
* Ran the migration using:
```
pgloader migrate.load
```
2. Tested both backend and frontend.

3. Automated tests to run on commit.

4. Created a script (./run.sh) to start the application.

----------------
AWS частта:
1. Регистрирах се.
2. Потърсих информация как се имплементира s3 сървиз с пайтън.
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html - S3 service example code.
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
3. Създадох bucket.
4. Създадох IAM потребител, който да не е root и да има read/write права в assets и read/write/list права за логовете.
5. Имплеменетирах пайтън частта с помощта на code example от т. 2.
6. Избрах да не използвам пressigned urls, защото в моя случай не е релевантен, тъй като приложението е просто устроено и има 10 изображения които са статични и трябва да бъдат достъпни(read access) за всички посетители.
7. Bucket policy - написан е нов.

   ```
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::flipcards-app-assets/*"
        }
    ]
    }
    ```
8. Промених адреса на изображенията във фронтенд частта, така че да     сочат към aws s3 bucket.
9. Добавих в .env VITE_S3_BASE_URL, където се пази S3 URL, за по-добра поддръжка (например ако сменя името на s3 bucket-а).
10. Logger - тук добавих нова папка в S3 Bucket с цел оптимизиране на разходи, тъй като не получих free tier.
11. Създадох права на потребителя за -  Write, Read, List
    ```
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::flipcards-app-assets",
                "arn:aws:s3:::flipcards-app-assets/logs/*"
            ]
        }
    ]
    }
    ```
12. Създадох s3_logger в utils, за да мога да записвам логове в bucket-а.
13. Добавих логовете в main, crud и router/cards.py, за да логвам различни събития, както и добавих клас LogAction в enums.py.
14. @asynccontextmanager частта за логване на startup/shutdown в main.py е с помощта на copilot, тъй като не знаех как да я имплементирам.
15. Логовете вече са налични -> [Link to python logs](https://flipcards-app-assets.s3.eu-north-1.amazonaws.com/Screenshot+2025-02-25+at+23.30.22.png) и [Link to S3 Logs](https://flipcards-app-assets.s3.eu-north-1.amazonaws.com/Screenshot+2025-02-25+at+23.29.31.png)
16. Използвах AWS Athena за да мога да преглеждам логовете чрез SQL заявки, без да се налага да ги отварям и свалям един по един.
    ```
    CREATE DATABASE flipcards_logs;
    #Заявка за създаване на базата данни.
    ```

    ```
    CREATE EXTERNAL TABLE flipcards_logs.logs (
    timestamp STRING,
    action STRING,
    details STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '\t' 
    LINES TERMINATED BY '\n'
    LOCATION 's3://flipcards-app-assets/logs/';

    #Външна таблица, която чете директно логове от S3 logs 
    ```
16. Резултат от AWS Athena - [> Result](https://flipcards-app-assets.s3.eu-north-1.amazonaws.com/Screenshot+2025-02-26+at+0.04.25.png)

