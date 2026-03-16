from flask import request
from app.modules.honeypot.utils.paths import DB_PATH

def extract_request_data():
    return {
        "ip": request.remote_addr,
        "method": request.method,
        "path": request.path,
        "user_agent": request.headers.get("User-Agent"),
        "headers": dict(request.headers)
    }


def classify_attack(path, method):
    if path == "/admin" and method == "GET":
        return "Reconnaissance"
    if path == "/admin" and method == "POST":
        return "Credential Harvesting"
    if path in ["/.env", "/config"]:
        return "Secret Discovery"
    if path in ["/backup.zip", "/db_dump.sql"]:
        return "Data Exfiltration"
    return "Unknown"

def is_bot_like(user_agent):
    if not user_agent:
        return True

    ua = user_agent.lower()
    bot_keywords = ["curl", "wget", "sqlmap", "nmap", "nikto", "scanner"]

    return any(keyword in ua for keyword in bot_keywords)
