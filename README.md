# GPT Repo Updater Backend

Production-grade Flask backend for Shroomtop420™ GPT repo automation.

## Features

- REST API for `/repo-update/`, `/generate-prompt`, `/update-repo`
- Secure, CORS-enabled
- Integrates with GitHub via fine-grained Personal Access Token (PAT)
- Serves frontend UI from `/static/index.html`
- Ready for GPT OpenAPI schema integration

## File Structure

```
repo-updater-backend-v1.0/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Procfile
├── README.md
└── static/
     └── index.html
```

## Setup

1. **Clone repo and install dependencies**
    ```sh
    git clone <this_repo_url>
    cd repo-updater-backend-v1.0
    pip install -r requirements.txt
    ```

2. **Configure Environment**
    - Copy `.env.example` to `.env`
    - Paste your GitHub PAT (`GITHUB_TOKEN=...`)

3. **Run the Server**
    ```sh
    python app.py
    # Or for production: gunicorn app:app
    ```

4. **Frontend**
    - Place your `index.html` UI in `static/`

## API

### `GET /repo-update/`
- **Auth:** Bearer token in header or `.env`
- **Returns:** Repos needing updates

### `POST /generate-prompt`
- **Body:** `{ "repoName": "...", "status": "..." }`
- **Returns:** Update prompt

### `POST /update-repo`
- **Body:** `{ "repoName": "...", "updates": { "README.md": "...", ... }, "accessToken": "..." }`
- **Returns:** Update results

## Deployment

- **Heroku/Render:** Add your GitHub token to environment
- **Local:** `.env` with token

## Security

- **Never commit `.env`**
- **Always use fine-grained PAT**

## License

MIT (see LICENSE)

<!-- SHROOMTOP420-MONETIZATION-BLOCK-START -->
## 🚀 Support & Commercial Use

- **Buy full-access or commercial license:** [Pay with Stripe](https://buy.stripe.com/aFa6oHeG74DQ8ZB3LubQY01)
- **Donate or support ongoing dev:** [Buy Me A Coffee](https://buymeacoffee.com/shroomtop420)

> *Commercial use requires license. See LICENSE for terms.*
<!-- SHROOMTOP420-MONETIZATION-BLOCK-END -->
