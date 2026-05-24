from data.games import GAMES

CPU_OPTIONS = {
    "celeron": ("Слабый (Celeron / старый Pentium)", 2),
    "i3_old": ("Intel Core i3 / Ryzen 3 (до 2018)", 4),
    "i5_mid": ("Intel Core i5 / Ryzen 5 (средний)", 6),
    "i7": ("Intel Core i7 / Ryzen 7", 8),
    "i9": ("Intel Core i9 / Ryzen 9 (топ)", 10),
}

GPU_OPTIONS = {
    "integrated": ("Встроенная графика", 2),
    "gtx1050": ("GTX 1050 / RX 560", 4),
    "gtx1660": ("GTX 1660 / RX 580", 5),
    "rtx2060": ("RTX 2060 / RX 5700", 6),
    "rtx3060": ("RTX 3060 / RX 6600 XT", 7),
    "rtx3070": ("RTX 3070 / RX 6700 XT", 8),
    "rtx4070": ("RTX 4070 / RX 7800 XT", 9),
    "rtx4090": ("RTX 4090 / RX 7900 XTX", 10),
}

RAM_OPTIONS = {
    "4": ("4 ГБ", 2),
    "8": ("8 ГБ", 5),
    "16": ("16 ГБ", 8),
    "32": ("32 ГБ и больше", 10),
}

STORAGE_OPTIONS = {
    "hdd": "HDD",
    "ssd": "SSD",
    "nvme": "NVMe SSD",
}

TIER_LABELS = {
    "excellent": "На высоких настройках",
    "good": "Комфортно на средних",
    "minimum": "Только минимальные настройки",
    "no": "Не потянет",
}


def get_form_options():
    return {
        "cpu": [(k, v[0]) for k, v in CPU_OPTIONS.items()],
        "gpu": [(k, v[0]) for k, v in GPU_OPTIONS.items()],
        "ram": [(k, v[0]) for k, v in RAM_OPTIONS.items()],
        "storage": list(STORAGE_OPTIONS.items()),
    }


def build_pc_profile(cpu_key: str, gpu_key: str, ram_key: str, storage_key: str):
    cpu_score = CPU_OPTIONS.get(cpu_key, ("", 0))[1]
    gpu_score = GPU_OPTIONS.get(gpu_key, ("", 0))[1]
    ram_score = RAM_OPTIONS.get(ram_key, ("", 0))[1]
    storage_label = STORAGE_OPTIONS.get(storage_key, "—")

    return {
        "cpu": cpu_score,
        "gpu": gpu_score,
        "ram": ram_score,
        "labels": {
            "cpu": CPU_OPTIONS.get(cpu_key, ("Не указан", 0))[0],
            "gpu": GPU_OPTIONS.get(gpu_key, ("Не указан", 0))[0],
            "ram": RAM_OPTIONS.get(ram_key, ("Не указан", 0))[0],
            "storage": storage_label,
        },
        "scores": {"cpu": cpu_score, "gpu": gpu_score, "ram": ram_score},
    }


def _meets(requirements: dict, scores: dict) -> bool:
    return all(scores[key] >= requirements[key] for key in ("cpu", "gpu", "ram"))


def evaluate_game(scores: dict, game: dict) -> dict:
    if _meets(game["rec"], scores):
        tier = "excellent"
    elif _meets(game["min"], scores):
        tier = "good"
    elif _meets(
        {
            "cpu": max(1, game["min"]["cpu"] - 1),
            "gpu": max(1, game["min"]["gpu"] - 1),
            "ram": max(1, game["min"]["ram"] - 2),
        },
        scores,
    ):
        tier = "minimum"
    else:
        tier = "no"

    gaps = []
    for key, label in (("cpu", "CPU"), ("gpu", "GPU"), ("ram", "RAM")):
        need = game["min"][key]
        have = scores[key]
        if have < need:
            gaps.append(f"{label}: нужно {need}/10, у вас {have}/10")

    return {
        **game,
        "tier": tier,
        "tier_label": TIER_LABELS[tier],
        "gaps": gaps,
        "sort_order": {"excellent": 0, "good": 1, "minimum": 2, "no": 3}[tier],
    }


def match_games(cpu_key: str, gpu_key: str, ram_key: str, storage_key: str):
    profile = build_pc_profile(cpu_key, gpu_key, ram_key, storage_key)
    scores = profile["scores"]

    results = [evaluate_game(scores, game) for game in GAMES]
    results.sort(key=lambda g: (g["sort_order"], g["title"]))

    playable = [g for g in results if g["tier"] != "no"]
    blocked = [g for g in results if g["tier"] == "no"]

    return profile, playable, blocked
