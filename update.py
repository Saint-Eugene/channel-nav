import json, os, re, urllib.parse, urllib.request
from geo import TREE

# ЗАМЕНИТЕ два значения ниже
CHANNEL = "username_канала"   # публичное имя канала, без @
OWNER_ID = 123456789          # ваш Telegram ID (число из @userinfobot)

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}/"


def call(method, **params):
    body = urllib.parse.urlencode(
        {k: json.dumps(v) if isinstance(v, (list, dict)) else v
         for k, v in params.items()}).encode()
    req = urllib.request.Request(API + method, data=body)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["result"]


def load(name, default):
    if os.path.exists(name):
        with open(name, encoding="utf-8") as f:
            return json.load(f)
    return default


def save(name, obj):
    with open(name, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def index(state, mid, text):
    tags = sorted({t.lower() for t in re.findall(r"#\w+", text or "")})
    if tags:
        title = re.sub(r"#\w+", "", text).strip().split("\n")[0][:50] or f"Пост {mid}"
        state["posts"][str(mid)] = {"t": title, "g": tags}
    else:
        state["posts"].pop(str(mid), None)


def tree_json(tree):
    out = []
    for name, val in tree.items():
        if name == "_tag":
            continue
        if isinstance(val, dict):
            node = {"t": name, "c": tree_json(val)}
            if "_tag" in val:
                node["own"] = val["_tag"].lower()
            out.append(node)
        else:
            out.append({"t": name, "tag": val.lower()})
    return out


def used_tags(nodes, acc):
    for n in nodes:
        for k in ("tag", "own"):
            if k in n:
                acc.add(n[k])
        used_tags(n.get("c", []), acc)
    return acc


def tag_lines(tree, prefix=""):
    for name, val in tree.items():
        if name == "_tag":
            continue
        if isinstance(val, dict):
            yield f"{prefix}{name}: {val.get('_tag', '')}"
            yield from tag_lines(val, prefix + "    ")
        else:
            yield f"{prefix}{name}: {val}"


def build(state):
    tags = {}
    for pid, p in sorted(state["posts"].items(), key=lambda kv: -int(kv[0])):
        for t in p["g"]:
            tags.setdefault(t, []).append([int(pid), p["t"]])
    tree = tree_json(TREE)
    used = used_tags(tree, set())
    rest = sorted((t for t in tags if t not in used), key=lambda t: t.lstrip("#"))
    tree.append({"t": "Теги", "misc": True,
                 "c": [{"t": t, "tag": t} for t in rest]})
    return {"channel": CHANNEL, "tree": tree, "tags": tags}


def is_my_channel(chat):
    return (chat.get("username") or "").lower() == CHANNEL.lower()


def main():
    state = load("state.json", {"offset": 0, "posts": {}})
    forwarded = 0
    while True:
        updates = call("getUpdates", offset=state["offset"], limit=100, timeout=0,
                       allowed_updates=["message", "channel_post", "edited_channel_post"])
        if not updates:
            break
        for u in updates:
            state["offset"] = u["update_id"] + 1
            post = u.get("channel_post") or u.get("edited_channel_post")
            if post:
                if is_my_channel(post["chat"]):
                    index(state, post["message_id"], post.get("text") or post.get("caption"))
                continue
            m = u.get("message") or {}
            fo = m.get("forward_origin") or {}
            if (m.get("from", {}).get("id") == OWNER_ID
                    and fo.get("type") == "channel" and is_my_channel(fo["chat"])):
                index(state, fo["message_id"], m.get("text") or m.get("caption"))
                forwarded += 1
    save("state.json", state)
    save("data.json", build(state))
    with open("tags.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(tag_lines(TREE)))
    if forwarded:
        call("sendMessage", chat_id=OWNER_ID,
             text=f"Принято постов: {forwarded}. Всего в индексе: {len(state['posts'])}")


main()
