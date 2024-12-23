import git


class GitRepoHandler:
    """Handles Git repository operations."""
    
    @staticmethod
    def clone_repo(repo_url: str, target_dir: str) -> None:
        """Clone a Git repository to target directory."""
        git.Repo.clone_from(repo_url, target_dir)
    
    @staticmethod
    def is_git_url(url: str) -> bool:
        """Check if URL is a valid Git repository URL."""
        return url.endswith('.git') or url.startswith(('https://github.com', 
                                                      'https://gitlab.com',
                                                      'https://bitbucket.org'))
