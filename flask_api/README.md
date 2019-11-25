# Flask API for Quebase
---

* To run the server:
    * make sure python3 (>=3.7) has been installed on your machine
    * make sure you have installed all the requirements in `requirements.txt`:
        ```
        > python3 -m pip install -r requirements.txt
        ```
    * make sure `mongod` has been installed on your machine (for localhost connection). To start the server:
        ```
        > mongod --dbpath <DIRECTORY_TO_MONGODB>/mongodb/
        ```
    * execute the command in API directory:
        ```
        > python3 run.py config.json
        ````
