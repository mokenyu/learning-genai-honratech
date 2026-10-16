## GENAI TRACK LEARNING REPO: HONRATECH BOOTCAMP

Want challenging exercises to test your skills? Go to [the work repo](https://github.com/mokenyu/honra-tech-genai-work-repo)

### Setup

 - Create your [fork](https://github.com/mokenyu/learning-genai-honratech/fork)
 - Clone the repo and enter folder.
    ```
    git clone your_fork_repo_link
    cd fork_clone_folder
    ```
 - Create new remote called `upstream` to handle syncing with the forked repo.
    ```
    git remote add upstream https://github.com/mokenyu/learning-genai-honratech
    ```

 - Pull latest changes.
    ```
    git pull upstream main
    ```
 
 - Create a branch with your name and switch to it
    ```
    git checkout -b branch_with_your_name
    ```

 - Create virtual environment using `uv` and activate.
    ```
    uv venv
    .venv\Scripts\activate
    ```

 - Install dependencies and equip environment.
    ```
    uv sync
    ```

 - Create `.env` from `.env.example`.
    ```
    cp .env.example .env
    ```

 - Create a folder with your name in root.

> For any files you want to make a change to, copy that file to the personal folder you just created and modify unless asked otherwise... whether it's during a training session or you experimenting.
> This is to ensure that the changes of the author and yours do not conflict.
