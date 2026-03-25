# How to generate `docker/Dockerfile.*` and CI configuration

#### Step 1. Generate scripts for generating dockerfiles

```bash
python make-gen-docker.py
```

This should generate `gen-docker.sh`.

#### Step 2. Generate dockerfiles

```bash
bash gen-docker.sh
```

This should generate `docker/Dockerfile.*`.


#### Step 3. Generate the CI workflow for GitHub Actions

```bash
python make-ci.py
```

This should generate `.github/workflows/dockerimage.yml`.


#### All-in-one

```bash
bash build.sh
```

This runs `clean.sh` → `make-gen-docker.py` → `gen-docker.sh` → `make-ci.py` in sequence.
