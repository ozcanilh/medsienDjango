## Installation

```bash
docker-compose up
# Open new terminal
docker exec -it medbank-web-1 bash 
python manage.py migrate
# To run
docker exec -it medbank-web-1 pytest


# When you do not use docker
pip install -r requirements.txt
# To run tests
pytest
```
## Usage

```bash


