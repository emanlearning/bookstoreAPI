from locust import task, TaskSet, HttpUser


class BookstoreLocust(HttpUser):

    host = "http://192.168.46.218:3000"


    @task
    def token_test(self):
        self.client.post("/token", data=dict(username="test", password="test"))


    @task
    def test_post_user(self):
        user_dict = {"name": "personel1",
	                "password": "pass1",
	                "role": "admin",
	                "mail": "a@b.com"}
        auth_header = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0Iiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzg3OTMyMjA5fQ.Bbo-fCcCs2s7sfjyc6YoDpm7Mq88dJmnVp3nz473L0c"}
        self.client.post("/v1/user", json=user_dict, headers=auth_header)