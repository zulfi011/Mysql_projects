# mysql_projects
procedure to run the above projects

1)  - Create a database using the `schema.sql` file:
    bash:
     mysql -u root -p dbname < schema.sql

2)  - Create a `.env` file in the root directory with the following content:
     DB_HOST=localhost
     DB_USER=root
     DB_PASSWORD=your_password
     DB_NAME=your_database_name

3)  - Install necessary modules from requirements.txt file:
      pip install -r requirements.txt

4)  - Run the project
