import unittest
from datetime import datetime
from uuid import UUID, uuid4

import jwt
from flask import Flask

from api.controllers import community_controller, events_controller
from api.controllers.community_controller import bp as community_bp
from api.controllers.events_controller import bp as events_bp
from services.community_service import CommunityService
from services.events_service import EventsService


NOW = datetime(2026, 1, 1, 10, 0, 0)


class FakeCommunityRepository:
    def __init__(self):
        self.posts = []
        self.comments = []

    def list_posts(self, status=None):
        return [p for p in self.posts if not status or p.status == status]

    def get_post(self, post_id):
        return next((p for p in self.posts if p.id == post_id), None)

    def create_post(self, post):
        post.id, post.created_at = uuid4(), NOW
        self.posts.append(post)
        return post

    def save_post(self, post): return post
    def delete_post(self, post): self.posts.remove(post)
    def list_comments(self, post_id): return [c for c in self.comments if c.post_id == post_id]
    def get_comment(self, comment_id): return next((c for c in self.comments if c.id == comment_id), None)

    def create_comment(self, comment):
        comment.id, comment.created_at = uuid4(), NOW
        self.comments.append(comment)
        return comment

    def save_comment(self, comment): return comment
    def delete_comment(self, comment): self.comments.remove(comment)


class FakeEventsRepository:
    def __init__(self):
        self.workshops, self.photowalks = [], []
        self.workshop_registrations, self.photowalk_registrations = [], []

    def list_workshops(self, status=None): return [e for e in self.workshops if not status or e.status == status]
    def get_workshop(self, event_id): return next((e for e in self.workshops if e.id == event_id), None)

    def create_workshop(self, event):
        event.id, event.created_at = uuid4(), NOW
        self.workshops.append(event)
        return event

    def save_workshop(self, event): return event
    def delete_workshop(self, event): self.workshops.remove(event)
    def list_photowalks(self, status=None): return [e for e in self.photowalks if not status or e.status == status]
    def get_photowalk(self, event_id): return next((e for e in self.photowalks if e.id == event_id), None)

    def create_photowalk(self, event):
        event.id, event.created_at = uuid4(), NOW
        self.photowalks.append(event)
        return event

    def save_photowalk(self, event): return event
    def delete_photowalk(self, event): self.photowalks.remove(event)

    def get_workshop_registration(self, event_id, user_id):
        return next((r for r in self.workshop_registrations if r.workshop_id == event_id and r.user_id == user_id and r.status == 'registered'), None)

    def list_workshop_registrations(self, event_id): return [r for r in self.workshop_registrations if r.workshop_id == event_id]

    def create_workshop_registration(self, registration):
        registration.id, registration.registered_at = uuid4(), NOW
        registration.status = registration.status or 'registered'
        self.workshop_registrations.append(registration)
        return registration

    def save_workshop_registration(self, registration): return registration

    def get_photowalk_registration(self, event_id, user_id):
        return next((r for r in self.photowalk_registrations if r.photowalk_id == event_id and r.user_id == user_id and r.status == 'registered'), None)

    def list_photowalk_registrations(self, event_id): return [r for r in self.photowalk_registrations if r.photowalk_id == event_id]

    def create_photowalk_registration(self, registration):
        registration.id, registration.registered_at = uuid4(), NOW
        registration.status = registration.status or 'registered'
        self.photowalk_registrations.append(registration)
        return registration

    def save_photowalk_registration(self, registration): return registration


class CommunityEventsApiTest(unittest.TestCase):
    user_id = uuid4()

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(community_bp)
        self.app.register_blueprint(events_bp)
        self.community_repo = FakeCommunityRepository()
        self.events_repo = FakeEventsRepository()
        community_controller.community_service = CommunityService(self.community_repo)
        events_controller.events_service = EventsService(self.events_repo)
        self.client = self.app.test_client()
        self.auth = {'Authorization': f'Bearer {self._token()}'}

    def _token(self):
        return jwt.encode({'user_id': str(self.user_id)}, 'film_lab_secret_key', algorithm='HS256')

    def test_posts_require_authentication_to_create_and_are_readable(self):
        payload = {'type': 'discussion', 'title': 'Film walk', 'content': 'Saturday plan'}
        self.assertEqual(self.client.post('/community/posts', json=payload).status_code, 401)
        response = self.client.post('/community/posts', json=payload, headers=self.auth)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.get('/community/posts').json[0]['title'], 'Film walk')

    def test_comment_can_be_created_for_existing_post(self):
        post = self.client.post('/community/posts', json={'type': 'note', 'title': 'Tips', 'content': 'Use ISO 400'}, headers=self.auth).json
        response = self.client.post(f"/community/posts/{post['id']}/comments", json={'content': 'Helpful'}, headers=self.auth)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['content'], 'Helpful')

    def test_workshop_registration_is_unique_and_can_be_cancelled(self):
        event = self.client.post('/events/workshops', json={'title': 'Darkroom 101', 'start_time': '2026-02-01T10:00:00Z'}, headers=self.auth).json
        path = f"/events/workshops/{event['id']}/registrations"
        self.assertEqual(self.client.post(path, headers=self.auth).status_code, 201)
        self.assertEqual(self.client.post(path, headers=self.auth).status_code, 409)
        self.assertEqual(self.client.delete(path, headers=self.auth).status_code, 200)

    def test_photowalk_create_and_registration(self):
        event = self.client.post('/events/photowalks', json={'title': 'City lights', 'start_time': '2026-02-02T18:00:00Z', 'meeting_location': 'Gate A'}, headers=self.auth)
        self.assertEqual(event.status_code, 201)
        path = f"/events/photowalks/{event.json['id']}/registrations"
        response = self.client.post(path, headers=self.auth)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['photowalk_id'], event.json['id'])


if __name__ == '__main__':
    unittest.main()
