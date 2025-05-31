import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from github import Github, GithubException
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder="static")
CORS(app)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@app.route('/repo-update/', methods=['GET'])
def repo_update():
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "") or GITHUB_TOKEN
        if not token:
            return jsonify({"error": "GitHub token required"}), 401
        g = Github(token)
        user = g.get_user()
        repos = []
        for repo in user.get_repos():
            files = [f.name for f in repo.get_contents("")] if not repo.fork else []
            missing = []
            if "README.md" not in files: missing.append("README.md")
            if "LICENSE" not in files and "LICENSE.txt" not in files: missing.append("LICENSE")
            if missing:
                repos.append({"name": repo.full_name, "missing": missing})
        return jsonify({"repos": repos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-prompt', methods=['POST'])
def generate_prompt():
    data = request.json
    repo = data.get("repoName", "")
    status = data.get("status", "")
    if not repo:
        return jsonify({"error": "repoName is required"}), 400
    prompt = f"You need to update {repo}.\nMissing: {status}.\nGenerate production-grade README, LICENSE, .gitignore, badges, release notes, and metadata."
    return jsonify({"prompt": prompt})

@app.route('/update-repo', methods=['POST'])
def update_repo():
    data = request.json
    repo_name = data.get("repoName")
    updates = data.get("updates")
    token = data.get("accessToken") or GITHUB_TOKEN
    if not all([repo_name, updates, token]):
        return jsonify({"error": "repoName, updates, and accessToken required"}), 400
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        results = {}
        for path, content in updates.items():
            try:
                contents = None
                try:
                    contents = repo.get_contents(path)
                    repo.update_file(contents.path, f"Update {path}", content, contents.sha)
                    results[path] = "updated"
                except GithubException:
                    repo.create_file(path, f"Create {path}", content)
                    results[path] = "created"
            except Exception as e:
                results[path] = f"error: {str(e)}"
        return jsonify({"result": "success", "details": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def serve_ui():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
