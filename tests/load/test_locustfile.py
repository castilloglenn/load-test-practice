from locust import HttpUser, task, between, SequentialTaskSet
from random import choice
from random import random


class UserBehavior(SequentialTaskSet):
    def on_start(self):
        # Try to login with invalid credentials first with a 50% chance
        if random() < 0.5:
            response = self.client.post(
                "/login",
                data={"username": "invalid", "password": "wrong"},
                allow_redirects=False,
            )
            assert response.status_code == 401

        # Now login with valid credentials
        self.username = choice(["alice", "bob"])
        self.password = "wonderland" if self.username == "alice" else "builder"
        response = self.client.post(
            "/login",
            data={"username": self.username, "password": self.password},
            allow_redirects=False,
        )
        assert response.status_code == 200
        # Save cookies for session
        self.session_cookies = response.cookies

    @task(5)
    def status_check(self):
        self.client.get("/status", cookies=self.session_cookies)

    @task(2)
    def profile(self):
        self.client.get("/profile", cookies=self.session_cookies)

    @task
    def logout(self):
        self.client.post("/logout", cookies=self.session_cookies)
        self.interrupt()  # End this user session


class FastApiUser(HttpUser):
    wait_time = between(0.5, 1.5)
    tasks = [UserBehavior]
