# Hardwarezone-scrapper 
Scrapper for http://forums.hardwarezone.com.sg/. It scrapes all the posts for the threads under all the categories.
Just run and sit back. 
The scrapper first get all the categories from main page: http://forums.hardwarezone.com.sg/ and then crawls all the threads to get the posts.
Look at the [following data](./data_format.md) for data being scrapped.

### Prerequisites
1. Mongo DB
2. Python

### Setup
 1. Setting up the python virtual env and installing the requirements.

Create the virtual env (one time process), virtualenv is in gitignore hence you 
have to create one on your local machine
```
virtualenv --no-site-packages env
```
Activate it:
```
source env/bin/activate
```
Install the requirements:
```
pip install -r requirements.txt
```

 2. Unique database and indexes in mongo
 ```
 use hardwarezone
 db.posts.createIndex( {"post.post_url" : 1 }, {"unique": true })
 ``` 

### Running the scripts

 The script stores the [following data](./data_format.md) data in mongo db.
 ```
scrapy crawl hdwZone
 ```
 
## License
This project is licensed under the MIT License.
