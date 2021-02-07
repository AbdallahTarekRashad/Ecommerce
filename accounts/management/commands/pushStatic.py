import glob
from os.path import isfile

from django.core.management.base import BaseCommand

from git import Repo


class Command(BaseCommand):
    help = 'Add Countries to DataBase'

    def handle(self, *args, **kwargs):
        PATH_OF_GIT_REPO = '.git'
        COMMIT_MESSAGE = 'Add AdminLte Static'
        # files = []
        # for filename in glob.iglob('static' + '**/**', recursive=True):
        #     if isfile(filename):
        #         files.append(filename)
        try:
            repo = Repo(PATH_OF_GIT_REPO)
            files = repo.untracked_files
            for i, f in enumerate(files):
                repo.git.add(f)
                print('Add: '+f)
                if i % 10 == 0:
                    repo.index.commit(COMMIT_MESSAGE)
                    origin = repo.remote(name='origin')
                    origin.push()
                    print('Push')
        except:
            print('Some error occured while pushing the code')
