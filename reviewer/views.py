from django.shortcuts import render
from core.analyzer import analyze_code
import tempfile
import os
from git import Repo


def home(request):
    if request.method == "POST":

        code = ""

        # 1️⃣ GitHub Repo
        repo_url = request.POST.get("repo")

        if repo_url:
            temp_dir = tempfile.mkdtemp()

            try:
                Repo.clone_from(repo_url, temp_dir)

                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".py"):
                            with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                                code += f.read() + "\n"

            except Exception as e:
                return render(request, "index.html", {"error": str(e)})

        # 2️⃣ File upload
        elif request.FILES.get("file"):
            file = request.FILES["file"]
            code = file.read().decode("utf-8")

        # 3️⃣ Text input
        else:
            code = request.POST.get("code")

        report = analyze_code(code)

        return render(request, "result.html", {"report": report})

    return render(request, "index.html")