# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
  Rule('/', name='home', handler='mood.handlers.HomePage'),
  Rule('/js/bookmarklet.js', name='bookmarklet-js', handler='mood.handlers.BookmarkletPage'),
  Rule('/item/<int:itemid>', name='newsitem-detail', handler='mood.handlers.NewsItemDetail'),

  # cron jobs
  Rule('/jobs/poll_hnsearch', name='job-poll-hnsearch', handler='mood.jobs.PollHNSearchJob'),
  Rule('/jobs/queue_alchemy_tasks', name='job-poll-hnsearch', handler='mood.jobs.QueueAlchemyTasksJob'),
  
  
  # tasks
  Rule('/tasks/poll_alchemyapi', name='task-poll-hnsearch', handler='mood.tasks.PollAlchemyTask'),
]
