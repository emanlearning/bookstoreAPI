#!/bin/bash

black main.py

black models/author.py
black models/book.py
black models/jwt_user.py
black models/user.py

black routes/v1.py
black routes/v2.py

black tests/all_tests.py
black tests/locust_load_test.py

black utils/const.py
black utils/db.py
black utils/db_functions.py
black utils/db_object.py
black utils/helper_functions.py
black utils/redis_object.py
black utils/security.py
