from celery import Celery

app = Celery('linkedin_fetcher',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['tasks'])

app.conf.update(
    task_annotations={
        'tasks.fetch_linkedin_profile_task': {'rate_limit': '10/m'}
    }
)

if __name__ == '__main__':
    app.start()
