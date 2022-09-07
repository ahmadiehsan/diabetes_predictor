# Diabetes Predictor

## Preparing workspace

```
git clone <this repo url>
cd <cloned dir>

virtualenv -p python3 venv
source venv/bin/activate

./runner requirements.install
```

## Available commands

- `./runner train <path/to/one/of/the/configs.yml>`
- `./runner test <path/to/one/of/the/configs.yml>`
- `./runner test <path/to/one/of/the/configs.yml> --run-for-one`
- `./runner tensorboard <path/to/one/of/the/configs.yml>`

The below commands are also available only for the project developers:

- `./runner git.pre_commit.init`
- `./runner git.pre_commit.run_for_all`
- `./runner requirements.compile`
