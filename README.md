## featExtractor
Python microservice responsible for extracting features from the music provided via volume mount.

### Docker Params
| Arg | Default | Description |
| --- | --- | --- |
| HOST | localhost | RabbitMQ host |
| USER | guest | HTTP basic auth username  |
| PASS | guest | HTTP basic auth password |
| PORT | 5672 | RabbitMQ Port |
| MNG_PORT | 15672 | RabbitMQ Management Port |
| TIME | 10 | Timeout to check if the service is up |


### Volumes
| Container Path | Description |
| --- | --- |
| `/Audios` | Folder where the downloaded audio files are accessed |

### RabbitMQ Queues
* Read from `musicFeatures`
    * Payload: video ID
* Write to `classifyMusic`
    * Payload: json(features result)

### Run Local Microservice
Run Rabbit
```
docker run -d -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest -p 15672:15672 -p 5672:5672 rabbitmq:3-management-alpine
```

Build local `featExtractor` image from source
```
docker build -t featextractorlocal:latest .
```

Run local `featExtractor` image
```
docker run -it --rm -e TIME=10 -e PORT=5672 -e PASS=guest -e USER=guest -e HOST=localhost -e MNG_PORT=15672 -v "<Local DIR>":"/Audios" --net=host featextractorlocal:latest
```

Run official `featExtractor` image
```
docker run -e TIME=10 -e USER=merUser -e PASS=passwordMER -e HOST=localhost -e MNG_PORT=15672 --net=host -v "<Local DIR>":"/Audios" merteam/featextractor:latest
```

### Tests
```
pytest
```
The tests are provided in the file `test_rabbit.py`. Currently checking the rabbitMQ connection and sending jobs to the queue.