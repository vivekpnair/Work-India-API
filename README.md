This project is a very simple basic clone of IRCTC website

How to run
    - This project is done using docker container
    - Frontend/MW - Python Flask
    - backend db : MySQL
    - to run the project copy the entire IRCTC_CLONE0.1 folder to a location and issue the following command
        - docker-compose build
    - this will create the mysql db container and python flask app server container
    - Register a user with http://localhost:5000/register
    - once you register you can login with the uid and password and make reservations
    - home page http://localhost:5000/home
