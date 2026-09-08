from locust import task, TaskSet, HttpUser


class BookstoreLocust(HttpUser):

    host = "http://172.29.81.15:3000"


    # @task
    # def token_test(self):
    #     self.client.post("/token", data=dict(username="test", password="test"))


    @task
    def test_post_user(self):
        user_dict = {"name": "personel1",
	                "password": "pass1",
	                "role": "admin",
	                "mail": "a@b.com"}
        auth_header = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyZGIiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3ODkxMDg5MDR9.xGSHBQycGUsPS2miXT3trB15a5oomeJ6wMeg1gqD8u8"}
        self.client.post("/v1/user", json=user_dict, headers=auth_header)

