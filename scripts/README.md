# How to generate `docker/Dockerfile.*` and `circle.yml`

#### Step 1. generate scripts for generating dockerfiles

```bash
python make-gen-docker.py
```

This should generate `gen-docker.sh`.

#### Step 2. generate dockerfiles

Run `gen-docker.sh`, which should generate `docker/Dockerfile.*`.


#### Step 3. generate the configuration file for CircleCI

```bash
python make-circleci.py
```

This should generate `circle.yml`.
