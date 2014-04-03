from common import *

INSTALLED_APPS += (
	'django_jenkins',
)

JENKINS_TASKS = (
	'django_jenkins.tasks.with_coverage',
        'django_jenkins.tasks.run_pep8',
        'django_jenkins.tasks.run_pyflakes',
)
