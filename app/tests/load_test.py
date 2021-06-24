import random

from locust import HttpUser, between, task
from faker import Faker

fake = Faker(['ru-RU'])


class UserBehavior(HttpUser):
    created_polls = {}  # poll_id -> vote_count
    wait_time = between(1, 2.5)

    @task(1)
    def create_poll(self):
        choices_count = random.randint(1, 10)
        fake.unique.clear()
        poll = {'name': fake.text(max_nb_chars=50), 'choices': [fake.unique.word() for _ in range(1, choices_count)]}
        response = self.client.post("/api/createPoll", json=poll)
        if response.status_code != 200:
            return
        poll_id = response.json()['id']
        self.created_polls[poll_id] = choices_count

    @task(100)
    def vote(self):
        if not self.created_polls:
            return

        poll_id = random.choice(list(self.created_polls.keys()))
        vote = {'poll_id': poll_id,
                'choice_id': random.randint(0, self.created_polls[poll_id]-2)}
        self.client.post("/api/poll", json=vote)

    @task(100)
    def get_result(self):
        if not self.created_polls:
            return

        poll_id = random.choice(list(self.created_polls.keys()))
        self.client.post(f"/api/getResult/{poll_id}")