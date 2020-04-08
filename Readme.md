## Link shorter service

This is a simple web service wich provides next functional:
- generate a shorter and unique alias (short link) by given link.
- by a short link, redirect to the original link.

Used programing stack:
- python v3.8 with Flask framework
- redis
- docker for deploying and running

### How to run
On the project folder level run next commands:
```
$ docker build -t link-shorter .
$ docker-compose up
```

After executed it you can reach service by http://127.0.0.1:5000 or http://localhost:5000.  
You can change listening port in __docker-compose.yml__ file.

### Unit tests
The project contains a unit tests.  
To run unit tests execute next command on the project folder level:
```
$ python -m unittest tests.link_shorter_tests
```
After executed it you should to see how many tests was ran and result of them.

### Development plan
|   | Work item  | Estimate | Completed |
|---|---|---|---|
| 1. | Create simple web-interface  | 2h  | 2h |
| 2. | Create Flask web-service with functions: shorting links, store it and redirect by them | 8h | 5h |
| 3. | Create docker-compose rollout  | 1h | 3h |
| 4. | Add logging  | 1h | 2h  |
| 5. | Add unit-tests  | 2h | 2h |
| 6. | Test  | 2h | 2h |
| 7. | Create readme file  | 2h | 1h |
|  | Total | 18h | 17h |