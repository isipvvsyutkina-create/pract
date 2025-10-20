
import sys
import random

ITEMS = {
    'ключ_деревянный': 'Деревянный ключ со знаком солнца.',
    'ключ_металлический': 'Металлический ключ с резьбой.',
    'факел': 'Факел — освещает тёмные помещения.',
    'нож': 'Небольшой нож — помогает в бою.'
}

START = (0, 0)
DOCK = (0, -1)
CAVE = (2, 1)
TREASURE = (3, 3)

ENEMIES = [
    {'name': 'Пират', 'coord': (1, 0), 'hp': 4, 'weak': 'нож'},
    {'name': 'Страж', 'coord': (3, 2), 'hp': 6, 'weak': 'факел'}
]

REQUIRED_KEYS = {'ключ_деревянный', 'ключ_металлический'}

DOORS = {
    'шлюз_лагуны': {'coord': (1, -1), 'requires': {'ключ_деревянный'}, 'open': False},
    'дверь_пещеры': {'coord': CAVE, 'requires': {'ключ_металлический'}, 'open': False}
}

MAP = {
    START: 'Песчаный берег. Ваш корабль стоит на якоре.',
    DOCK: 'Причал и лагуна.',
    (1, 0): 'Поляна с хижиной.',
    (2, 0): 'Тропинка вглубь острова.',
    CAVE: 'Вход в пещеру — тёмно внутри.',
    (3, 2): 'Узкий коридор.',
    TREASURE: 'Глубокая камера — в центре стоит сундук.'
}
world_items = {
    DOCK: ['ключ_деревянный'],
    (1, 0): ['нож'],
    (2, 0): ['факел'],
    (3, 2): ['ключ_металлический']
}

player = {'name': 'Игрок', 'hp': 10}
inventory = []  
collected_keys = set()  
player_coord = START  

def show_help():
    print('Команды: осмотреть, идти x y, взять <предмет>, использовать <предмет>, открыть <дверь>, атаковать <враг>, инвентарь, помощь, выйти')

def describe(coord):
    print('Место:', coord)
    print(MAP.get(coord, 'Пусто.'))
    items = world_items.get(coord, [])
    if items:
        print('Здесь есть предметы:', ', '.join(items))


def show_inventory():
    if not inventory:
        print('Инвентарь пуст.')
    else:
        print('Инвентарь:')
        for i, it in enumerate(inventory, 1):
            print(f'{i}. {it} - {ITEMS.get(it, "описание отсутствует")}')

def move(x_str, y_str):
    global player_coord
    try:
        x = int(x_str); y = int(y_str)
    except ValueError:
     print('Неверные координаты. Пример: идти 1 0')
     return 
    new = (x, y)
    if abs(new[0] - player_coord[0]) + abs(new[1] - player_coord[1]) > 2:
        print('Слишком далеко. Идите по шагам.')
        return
    player_coord = new
    describe(player_coord)
    
    for e in ENEMIES:
        if e['coord'] == player_coord and e['hp'] > 0:
            print(f"Встречен враг: {e['name']}")

def take_item(name):
    items = world_items.get(player_coord, [])
    if name in items:
        inventory.append(name)
        items.remove(name)
        print(f'Вы взяли: {name}')
        if name.startswith('ключ'):
            collected_keys.add(name)
            print('Ключ добавлен в коллекцию ключей.')
    else:
        print('Здесь нет такого предмета.')


def use_item(name):
    if name not in inventory:
        print('У вас нет этого предмета.')
        return
    print(f'Вы используете {name}.')
    if name == 'факел':
        print('Факел даёт свет — в тёмных местах безопаснее.')
    elif name == 'нож':
        print('Нож можно использовать для боя.')
    else:
        print('Но пока особого эффекта нет.')


def open_door(name):
    d = DOORS.get(name)
    if not d:
        print('Такой двери нет.')
        return
    if d['open']:
        print('Дверь уже открыта.')
        return
    if d['requires'].issubset(collected_keys):
        d['open'] = True
        print(f'Вы открыли {name}!')
    else:
        miss = d['requires'] - collected_keys
        print('Нужные ключи отсутствуют:', ', '.join(miss))

def attack(name):
    
    for e in ENEMIES:
        if e['name'].lower() == name.lower() and e['coord'] == player_coord and e['hp'] > 0:
            weapon_bonus = 2 if ('нож' in inventory and e['weak'] == 'нож') else 0
            dmg = 2 + weapon_bonus
            e['hp'] -= dmg
            print(f'Вы наносите {dmg} урона {e["name"]}. Осталось HP у врага: {max(e["hp"],0)}')
            if e['hp'] <= 0:
                print(f'Враг {e["name"]} побеждён!')
                return
            
            rd = random.randint(1, 3)
            player['hp'] -= rd
            print(f'Враг бьёт в ответ: вы теряете {rd} HP. Ваше HP: {player["hp"]}')
            if player['hp'] <= 0:
                print('Вы погибли. Игра окончена.')
                sys.exit(0)
            return
    print('Нет врага с таким именем здесь.')

def level_one():
    print('УРОВЕНЬ 1: Проникнуть на остров ')
    global player_coord
    describe(player_coord)
    while True:
        cmd = input('> ').strip().lower()
        if not cmd:
            continue
        if cmd in ('помощь', 'help'):
            show_help(); continue
        if cmd == 'осмотреть':
            describe(player_coord); continue
        if cmd.startswith('идти '):
            parts = cmd.split()
            if len(parts) >= 3:
                move(parts[1], parts[2])
            else:
                print('Формат: идти x y')
            continue
        if cmd.startswith('взять '):
            take_item(cmd[6:]); continue
        if cmd == 'инвентарь':
            show_inventory(); continue
        if cmd.startswith('использовать '):
            use_item(cmd.split(maxsplit=1)[1]); continue
        if cmd.startswith('открыть '):
            open_door(cmd.split(maxsplit=1)[1])
           
            if DOORS['дверь_пещеры']['open']:
                print('Дверь в пещеру открыта. Переход на уровень 2.')
                return
            continue
        if cmd.startswith('атаковать '):
            attack(cmd.split(maxsplit=1)[1]); continue
        if cmd == 'выйти' or cmd == 'выход':
            print('Выход.'); sys.exit(0)
        print('Неизвестная команда. Введите "помощь" для подсказки.')
        
        def level_two():
            global player_coord
        print('УРОВЕНЬ 2: Найти сокровище ')

        player_coord = (3, 1)
        describe(player_coord)
        while True:
            cmd = input('> ').strip().lower()
            if not cmd:
                 continue
            if cmd in ('помощь', 'help'):
                show_help(); continue
            if cmd == 'осмотреть':
                describe(player_coord); continue
            if cmd.startswith('идти '):
                parts = cmd.split()
            if len(parts) >= 3:
                move(parts[1], parts[2])
            else:
                print('Формат: идти x y')
                continue
            if cmd.startswith('взять '):
                take_item(cmd[6:]); continue
            if cmd == 'инвентарь':
                show_inventory(); continue
            if cmd.startswith('использовать '):
                use_item(cmd.split(maxsplit=1)[1]); continue
            if cmd.startswith('атаковать '):
                attack(cmd.split(maxsplit=1)[1]); continue
            if cmd.startswith('открыть '):
                target = cmd.split(maxsplit=1)[1]
            if target == 'сундук' and player_coord == TREASURE:
                if REQUIRED_KEYS.issubset(collected_keys):
                    print('Вы открыли сундук и нашли сокровище! Победа!')
                    return
                else:
                    missing = REQUIRED_KEYS - collected_keys
                    print('Для открытия сундука не хватает ключей:', ', '.join(missing))
            else:
                open_door(target)
                continue
            if cmd == 'выйти' or cmd == 'выход':
                print('Выход.'); sys.exit(0)
            print('Неизвестная команда. Введите "помощь" для подсказки.')

def main():
    print('Добро пожаловать! Цель: проникнуть на остров и найти сокровище.')
    print('Наберите "помощь" для списка команд.')

    inventory.append('нож')
    print('В инвентаре: нож')

    level_one()
    level_two()
    print('Спасибо за игру!')

if __name__ == '__main__':
    main()
