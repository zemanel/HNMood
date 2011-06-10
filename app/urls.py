# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
    Rule('/', name='home', handler='mood.handlers.HomePage'),
    #Rule('/pretty', name='hello-world-pretty', handler='hello_world.handlers.PrettyHelloWorldHandler'),

    # cron jobs
    Rule('/jobs/poll_hnsearch', name='job-poll-hnsearch', handler='mood.handlers.PollHNSearchJob'),
    
    # tasks
    Rule('/tasks/poll_alchemyapi', name='task-poll-hnsearch', handler='mood.handlers.PollAlchemyTask'),
]
