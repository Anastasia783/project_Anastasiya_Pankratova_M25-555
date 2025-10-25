from .constants import ROOMS


def get_input(prompt="> "):
    """Получение ввода от пользователя."""
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении."""
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    
    if direction not in room['exits']:
        return "Нельзя пойти в этом направлении."
    
    next_room = room['exits'][direction]
    game_state['current_room'] = next_room
    game_state['steps_taken'] += 1
    return f"Вы переместились в {next_room}."


def take_item(game_state, item_name):
    """Берет предмет из комнаты."""
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    
    if item_name not in room['items']:
        return "Такого предмета здесь нет."
    
    if item_name == 'treasure_chest':
        return "Вы не можете поднять сундук, он слишком тяжелый."
    
    room['items'].remove(item_name)
    game_state['player_inventory'].append(item_name)
    return f"Вы подняли: {item_name}"


def use_item(game_state, item_name):
    """Использует предмет из инвентаря."""
    if item_name not in game_state['player_inventory']:
        return "У вас нет такого предмета."
    
    if item_name == 'torch':
        return "Факел освещает путь. Стало светлее!"
    elif item_name == 'sword':
        return "Вы чувствуете уверенность с мечом в руках."
    elif item_name == 'bronze_box':
        if 'rusty_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty_key')
            return "Вы открыли бронзовую шкатулку и нашли внутри rusty_key!"
        return "Бронзовая шкатулка пуста."
    elif item_name == 'rusty_key':
        if game_state['current_room'] == 'treasure_room':
            game_state['player_inventory'].remove('rusty_key')
            game_state['player_inventory'].append('treasure_key')
            return "Вы почистили rusty_key и получили treasure_key!"
        return "Вы осматриваете ключ, но не находите ему применения здесь."
    else:
        return f"Вы не знаете, как использовать {item_name}."


def show_inventory(game_state):
    """Показывает инвентарь игрока."""
    inventory = game_state['player_inventory']
    if not inventory:
        return "Ваш инвентарь пуст."
    return f"Инвентарь: {', '.join(inventory)}"