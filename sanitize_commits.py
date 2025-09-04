import re

EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAD6\U0001F004\U0001F0CF\u2600-\u26FF\u2700-\u27BF]+", re.UNICODE)
WHITESPACE_RE = re.compile(r"\s+")

# If already looks like Conventional Commits, keep it
CC_PREFIX = re.compile(r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|merge):\s", re.I)

# Map common leading words to types
LEAD_MAP = [
    (re.compile(r"^update\b", re.I), "docs"),
    (re.compile(r"^revamp(ed)?\b", re.I), "refactor"),
    (re.compile(r"^remove(d|s)?\b|^delete(d|s)?\b|^drop(ped|s)?\b", re.I), "chore"),
    (re.compile(r"^add(ed|s)?\b|^implement(ed)?\b", re.I), "feat"),
    (re.compile(r"^fix(ed|es)?\b|^tweak(ed|s)?\b", re.I), "fix"),
    (re.compile(r"^refactor(ed)?\b|^rework(ed)?\b", re.I), "refactor"),
]

# Normalize simple "Update <path>" into docs: update <path>
UPDATE_PATH = re.compile(r"^update\s+(.+)$", re.I)


def sanitize(subject: str) -> str:
    original = subject
    subject = subject.strip()
    if not subject or subject.lower().startswith("merge ") or subject.lower().startswith("merge:"):
        return original
    if CC_PREFIX.match(subject):
        return subject
    subject = EMOJI_RE.sub("", subject)
    subject = subject.replace("—", "-")
    subject = subject.replace("–", "-")
    subject = WHITESPACE_RE.sub(" ", subject).strip()
    subject = subject.split("|")[0].strip()
    # If subject has semicolons, keep the first clause
    if ";" in subject:
        subject = subject.split(";")[0].strip()
    m = UPDATE_PATH.match(subject)
    if m:
        path = m.group(1).strip()
        return f"docs: update {path}"
    lowered = subject.lower()
    for rx, cc in LEAD_MAP:
        if rx.match(lowered):
            rest = subject.split(" ", 1)
            tail = rest[1] if len(rest) > 1 else ""
            tail = tail.strip()
            if tail and not tail[0].isalpha():
                tail = tail.lstrip("-: .")
            tail = tail.strip()
            if tail:
                return f"{cc}: {tail}"
            return f"{cc}: update"
    # default to chore
    return f"chore: {subject}"[:100]


def commit_callback(commit):
    try:
        msg = commit.message.decode("utf-8", errors="replace")
    except Exception:
        return
    first_line, *rest = msg.splitlines()
    new_subject = sanitize(first_line)
    if new_subject != first_line:
        commit.message = (new_subject + "\n").encode("utf-8")
