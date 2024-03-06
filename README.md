
# SpaceTech Odyssey

#### SpaceTech Odyssey is a blogging web application for posting and sharing space-related articles.
## Features

- Session-based User Authentication 
- CRUD operations
- Paginated Responses
- Admin Panel




## Tech Stack

* Django Framework

* PostgrSQL Database

* AWS S3

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`: Django secret key

`IS_DEVELOPMENT`: Indicate whether the application is running in development (True) or production (False) mode

`APP_HOST`: Allowed host URL

`EXTERNAL_DB_URL`: Remote database URL.

`AWS_ACCESS_KEY_ID`: Your AWS access key Id.

`AWS_SECRET_ACCESS_KEY`: Your AWS access key.

`AWS_STORAGE_BUCKET_NAME`: Name of the  S3  bucket where you want to host the static files.

`AWS_S3_REGION_NAME`: AWS region name. For example, `ap-south-1`.
