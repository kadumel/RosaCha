from pathlib import Path

from django.conf import settings


def brand_assets(request):
    media_root = Path(settings.MEDIA_ROOT)
    if not media_root.exists():
        return {'navbar_logo_url': ''}

    allowed_suffixes = {'.png', '.jpg', '.jpeg', '.webp', '.svg'}
    candidates = []

    for file_path in media_root.rglob('*'):
        if not file_path.is_file() or file_path.suffix.lower() not in allowed_suffixes:
            continue

        stem = file_path.stem.lower()
        score = 0
        if 'rosacha' in stem or 'rosa' in stem:
            score += 3
        if 'logo' in stem:
            score += 4
        if score == 0:
            continue

        relative = file_path.relative_to(media_root).as_posix()
        candidates.append((score, f'{settings.MEDIA_URL}{relative}'))

    if not candidates:
        return {'navbar_logo_url': ''}

    candidates.sort(key=lambda item: item[0], reverse=True)
    return {'navbar_logo_url': candidates[0][1]}
