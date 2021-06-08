import nox

@nox.session(python=["3.7","3.8"],venv_backend="conda")
def tests(session):
    session.conda_install('--file','package-list.txt')
    session.run('conda', 
            'develop', 
            '.',
            '--prefix', 
            session.virtualenv.location)
    session.run('pytest', '-v', '--html=test_results.html')

@nox.session(python=["3.8"],venv_backend="conda")
def lint(session):
    session.conda_install('flake8')
    session.run('flake8', 'anagram/')
