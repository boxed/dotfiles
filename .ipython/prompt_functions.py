# coding=utf8
try:
    import git as _git
 
    class Repo(_git.Repo):
        @property
        def active_branch(self):
            try:
                return super(Repo, self).active_branch
            except:
                return '(no branch)'
 
        @property
        def has_untracked(self):
            return '??' in self.git.status(porcelain=True)
 
 
    def _br_and_st():
        try:
            repo = Repo()
            return repo.active_branch, repo.is_dirty(), repo.has_untracked
        except _git.InvalidGitRepositoryError:
            return '', False, False
        except Exception as error:
            return str(error), False, False
 
except ImportError:
    # Fall back to execute git subprocess if python-git is not installed.
 
    def _git_current_branch():
        from subprocess import Popen, PIPE
        # The following is the same as `git branch |grep ^\* |cut -b3-` which gets the current branch name
        git_br = Popen(["git", "branch"], stdout=PIPE, stderr=PIPE)
        grep = Popen(['grep', r'^\*'], stdin=git_br.stdout, stdout=PIPE)
        cut = Popen(['cut', '-b3-'], stdin=grep.stdout, stdout=PIPE)
        return cut.communicate()[0].strip()
 
    def _git_isdirty():
        from subprocess import Popen, PIPE
        # git st --porcelain | grep -v ^? | wc -l
        git_st = Popen(["git", "status", "--porcelain"], stdout=PIPE, stderr=PIPE)
        grep = Popen(["grep", "-v", "^?"], stdin=git_st.stdout, stdout=PIPE)
        wc = Popen(['wc', '-l'], stdin=grep.stdout, stdout=PIPE)
        count = wc.communicate()[0].strip()
        count = int(count)
        return False if count == 0 else True
 
    def _git_has_untracked():
        from subprocess import Popen, PIPE
        # git st --porcelain | grep ^? | wc -l
        git_st = Popen(["git", "status", "--porcelain"], stdout=PIPE, stderr=PIPE)
        grep = Popen(["grep", "^?"], stdin=git_st.stdout, stdout=PIPE)
        wc = Popen(['wc', '-l'], stdin=grep.stdout, stdout=PIPE)
        count = wc.communicate()[0].strip()
        count = int(count)
        return False if count == 0 else True
 
    def _br_and_st():
        try:
            return _git_current_branch(), _git_isdirty(), _git_has_untracked()
        except:
            return '', False, False
    
@IPython.core.prompts.LazyEvaluate
def git_branch_and_st():
    from IPython.core.prompts import Colors
    branch, dirty, untracked = _br_and_st()
    if branch:
        suffix = ''
        if dirty or untracked:
            suffix += ' '
            if dirty:
                suffix += u'\u2717'
            if untracked:
                suffix += '+'
        return ur' git:(%s%s%s)%s%s' % (Colors.Red, branch, Colors.Blue, Colors.Yellow, suffix)
    else:
        return ''

@IPython.core.prompts.LazyEvaluate
def virtual_env():
    import os.path
    from IPython.core.prompts import Colors
    try:
        return u'%s(%s) ' % (Colors.Yellow, os.path.split(os.environ['VIRTUAL_ENV'])[-1])
    except KeyError:
        return ''