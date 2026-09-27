"""
build.py — сканирует папку images/ и создаёт works.json
Запуск: python build.py
"""
import os, json, re

ROOT = 'images'
EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}

def title_from_folder(name):
    """Corridor1 → Corridor 1, my_room → My Room, sword-v2 → Sword V2"""
    name = name.replace('_', ' ').replace('-', ' ')
    name = re.sub(r'(\d+)', r' \1', name)
    return ' '.join(w.capitalize() for w in name.split())

def collect():
    works = []
    if not os.path.isdir(ROOT):
        print(f'Папка {ROOT} не найдена!')
        return works

    for cat in sorted(os.listdir(ROOT)):
        cat_path = os.path.join(ROOT, cat)
        if not os.path.isdir(cat_path):
            continue
        for work in sorted(os.listdir(cat_path)):
            work_path = os.path.join(cat_path, work)
            if not os.path.isdir(work_path):
                continue
            imgs = []
            for f in sorted(os.listdir(work_path)):
                ext = os.path.splitext(f)[1].lower()
                if ext in EXTS:
                    imgs.append(f'{ROOT}/{cat}/{work}/{f}')
            if not imgs:
                print(f'⚠ {cat}/{work} — пусто, пропуск')
                continue
            works.append({
                'folder': work,
                'category': cat,
                'title': title_from_folder(work),
                'images': imgs
            })
    return works

if __name__ == '__main__':
    works = collect()
    with open('works.json', 'w', encoding='utf-8') as f:
        json.dump({'works': works}, f, ensure_ascii=False, indent=2)
    print(f'✓ Готово. Найдено {len(works)} работ.')
    for w in works:
        print(f"  [{w['category']}] {w['title']} — {len(w['images'])} фото")