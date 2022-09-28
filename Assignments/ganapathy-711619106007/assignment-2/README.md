### Initialize the Database
```flask ibm_db2```


### Table Structure (`Registration`)
| Column  | Type|
| ------------- | ------------- |
| `id`  | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| `username`  | `VARCHAR NOT NULL`  |
| `password`  | `VARCHAR NOT NULL`  |
| `email`  | `VARCHAR NOT NULL` |
| `rollnumber`  | `VARCHAR NOT NULL`  |

`ibm db2` is used for the database.