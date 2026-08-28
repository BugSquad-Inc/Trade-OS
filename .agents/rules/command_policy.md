# Antigravity 2.0 Command Execution & Safety Policy

## 🟢 ALLOWED DEVELOPMENT COMMANDS (Autonomous Execution Permitted)
The agent is authorized to execute standard development, testing, build, and operational commands without requiring manual user confirmation:

1. **Python & Testing Environment**:
   - `python ...`, `python -m ...`
   - `pytest ...`, `pytest backend/app/tests`
   - `pip install ...`, `pip list`
   - Data seeding, scoring runs, and pipeline scripts (`python update.py`, `python backend/app/scripts/...`)
2. **Node.js & Frontend Toolchain**:
   - `npm install`, `npm run build`, `npm run dev`, `npm test`
   - `npx ...`, `tsc`, `vite build`
3. **Container & Database Management**:
   - `docker compose up -d`, `docker compose ps`, `docker compose down`
   - `docker ps`, `docker logs`
4. **Build, Architecture & Maintenance Scripts**:
   - `python update.py`, `python update.py --check`
   - Script generation & execution in `scripts/` directory
   - Standard safe git status, add, commit, push:
     - `git status`, `git diff`, `git log`
     - `git add .`, `git commit -m "..."`, `git push origin main`

---

## 🔴 DANGEROUS & DESTRUCTIVE COMMANDS (STRICTLY PROHIBITED / REQUIRE USER CONFIRMATION)
The agent must NEVER autonomously execute destructive, irreversible, or hazardous system commands:

1. **Destructive File & Directory Deletion**:
   - ❌ `rm -rf /`, `rm -rf *`, `rmdir /s /q C:\`
   - ❌ Unscoped mass deletion of project directories or source code
   - ❌ Deletion of database volumes (`docker volume rm`, deleting `postgres_data` without backup)
2. **Dangerous & Destructive Git Operations**:
   - ❌ `git push --force`, `git push -f` (overwriting remote history)
   - ❌ `git reset --hard` (unless explicitly rolling back a specific uncommitted change)
   - ❌ `git clean -fdx` (mass deletion of untracked assets)
   - ❌ Deletion of main/production branches (`git branch -D main`)
3. **Destructive System & Process Commands**:
   - ❌ `format`, `diskpart`, `fdisk`
   - ❌ `Stop-Process -Force` on critical OS or IDE processes
   - ❌ Modifying Windows registry or system environment paths
   - ❌ Exposing or committing raw secrets / credentials (API tokens, private keys)
