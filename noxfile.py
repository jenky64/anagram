import nox

@nox.session(python=["3.8"],venv_backend="conda")
def tests(session):
    session.conda_install('--file','package-list.txt')
    session.run('conda', 
            'develop', 
            '.',
            '--prefix', 
            session.virtualenv.location)
    session.run('pytest')
