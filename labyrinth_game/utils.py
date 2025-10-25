import math

from .constants import ALTERNATIVE_ANSWERS, COMMANDS, ROOMS


def pseudo_random(seed, modulo):
    """Псевдослучайный генератор на основе синуса."""
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    result = fractional * modulo
    return int(result)


def trigger_trap(game_state):
    """Активация ловушки с негативными последствиями."""
    print("Ловушка активирована! Пол стал дрожать...")
    
    inventory = game_state['player_inventory']
    
    if inventory:
        # Выбираем случайный предмет для удаления
        item_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(item_index)
        return f"Вы потеряли предмет: {lost_item}"
    else:
        # Игрок получает "урон"
        damage_chance = pseudo_random(game_state['steps_taken'], 10)
        if damage_chance < 3:
            game_state['game_over'] = True
            return "Ловушка нанесла смертельный удар! Игра окончена."
        else:
            return "Вам повезло - вы успели увернуться от ловушки!"


def random_event(game_state):
    """Случайные события во время перемещения."""
    # Проверяем, произойдет ли событие (10% шанс)
    event_chance = pseudo_random(game_state['steps_taken'], 10)
    if event_chance != 0:
        return ""
    
    # Выбираем тип события
    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
    current_room = game_state['current_room']
    
    if event_type == 0:
        # Находка: добавляем монетку в комнату
        ROOMS[current_room]['items'].append('coin')
        return "Вы нашли на полу блестящую монетку!"
    
    elif event_type == 1:
        # Испуг
        message = "Вы слышите странный шорох в темноте..."
        if 'sword' in game_state['player_inventory']:
            message += " Благодаря мечу в руках, вы отпугиваете неизвестное существо."
        return message
    
    elif event_type == 2:
        # Срабатывание ловушки
        if (current_room == 'trap_room' and 
            'torch' not in game_state['player_inventory']):
            trap_result = trigger_trap(game_state)
            return f"Опасность! {trap_result}"
        else:
            return "Вы почувствовали опасность, но смогли избежать ловушки."
    
    return ""


def show_help():
    """Показывает справку по командам."""
    help_text = "\nДоступные команды:\n"
    for command, description in COMMANDS.items():
        help_text += f"  {command:<16} - {description}\n"
    return help_text


def describe_current_room(game_state):
    """Описание текущей комнаты."""
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    
    description = f"=== {current_room.upper()} ===\n"
    description += f"{room['description']}\n\n"
    
    # ПРЕДМЕТЫ
    if room['items']:
        description += " Заметные предметы: " + ", ".join(room['items']) + "\n"
    else:
        description += " Заметные предметы: нет\n"
    
    # ВЫХОДЫ - показываем направления и куда они ведут
    if room['exits']:
        exits_list = []
        for direction, target_room in room['exits'].items():
            exits_list.append(f"{direction} → {target_room}")
        description += " Выходы: " + ", ".join(exits_list) + "\n"
    else:
        description += " Выходы: нет\n"
    
    # ЗАГАДКА
    if room['puzzle'] and current_room not in game_state.get('solved_puzzles', set()):
        description += "\n Кажется, здесь есть загадка (используйте команду solve).\n"
    
    return description


def solve_puzzle(game_state):
    """Решает загадку в текущей комнате."""
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    
    if not room['puzzle']:
        return "Загадок здесь нет."
    
    if current_room in game_state.get('solved_puzzles', set()):
        return "Вы уже решили загадку в этой комнате."
    
    question, correct_answer = room['puzzle']
    print(f"\n {question}")
    
    from .player_actions import get_input
    
    while True:
        user_answer = get_input("Ваш ответ: ").strip().lower()
        
        if not user_answer:
            return "Вы отказались от решения загадки."
        
        # Проверяем альтернативные варианты ответов
        is_correct = False
        if correct_answer in ALTERNATIVE_ANSWERS:
            is_correct = user_answer in ALTERNATIVE_ANSWERS[correct_answer]
        else:
            is_correct = user_answer == correct_answer.lower()
        
        if is_correct:
            game_state.setdefault('solved_puzzles', set()).add(current_room)
            
            # Награда за решение загадки в зависимости от комнаты
            rewards = {
                'hall': 'Вы получаете бронзовый амулет!',
                'trap_room': 'Ловушка деактивирована! Вы в безопасности.',
                'library': 'Вы находите скрытый свиток с картой!',
                'mirror_room': 'Зеркала перестают искажать реальность.',
                'crystal_cave': 'Кристаллы начинают светиться ярче.',
                'alchemy_lab': 'Вы находите рецепт могущественного зелья!',
                'garden': 'Магические растения расцветают.'
            }
            
            reward_message = rewards.get(current_room, "Правильно! Загадка решена.")
            
            if current_room == 'treasure_room':
                return attempt_open_treasure(game_state)
            return reward_message
        else:
            # В trap_room неверный ответ активирует ловушку
            if current_room == 'trap_room':
                trap_result = trigger_trap(game_state)
                return f"Неверный ответ! {trap_result}"
            
            # Предлагаем попробовать еще раз или выйти
            print("Неверно. Попробуйте еще раз или нажмите Enter чтобы выйти.")

def attempt_open_treasure(game_state):
    """Логика открытия сундука с сокровищами."""
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in room['items']:
            room['items'].remove('treasure_chest')
        return "В сундуке сокровище! Вы победили!"
    
    print("Сундук заперт. У вас нет ключа, но можно попробовать ввести код.")
    
    from .player_actions import get_input
    answer = get_input("Ввести код? (да/нет): ").strip().lower()
    
    if answer == 'да':
        user_code = get_input("Введите код: ").strip()
        _, correct_code = room['puzzle']
        
        if (user_code == correct_code or 
            (correct_code in ALTERNATIVE_ANSWERS and 
             user_code in ALTERNATIVE_ANSWERS[correct_code])):
            if 'treasure_chest' in room['items']:
                room['items'].remove('treasure_chest')
            return "Код верный! Сундук открыт. В сундуке сокровище! Вы победили!"
        else:
            return "Неверный код. Сундук остается запертым."
    else:
        return "Вы отступаете от сундука."


def check_win_condition(game_state):
    """Проверяет условия победы."""
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    return ('treasure_chest' not in room['items'] and 
            current_room == 'treasure_room')


def handle_random_event(game_state):
    """Обрабатывает случайные события (старая функция для обратной совместимости)."""
    return random_event(game_state)