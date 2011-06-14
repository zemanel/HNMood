# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
  Rule('/', name='home', handler='mood.handlers.HomePage'),
  
  Rule('/js/bookmarklet.js', name='bookmarklet-js', handler='mood.handlers.BookmarkletPage'),
  Rule('/item/<int:itemid>', name='newsitem-detail', handler='mood.handlers.NewsItemDetail'),

  # cron jobs
  Rule('/jobs/queue_hnsearch_tasks', name='job-poll-hnsearch', handler='mood.jobs.QueueHNSearchJob'),
  Rule('/jobs/queue_alchemyapi_tasks', name='job-poll-alchemyapi', handler='mood.jobs.QueueAlchemyTasksJob'),

  # tasks
  Rule('/tasks/poll_alchemyapi', name='task-poll-alchemyapi', handler='mood.tasks.PollAlchemyTask'),
  Rule('/tasks/poll_hnsearch', name='task-poll-hnsearch', handler='mood.tasks.PollHNSearchTask'),
  
]
