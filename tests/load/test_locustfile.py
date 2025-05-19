from locust import HttpUser, task, between


class FastApiUser(HttpUser):
    wait_time = between(0, 1)

    @task
    def hello_world(self):
        self.client.get("/")
