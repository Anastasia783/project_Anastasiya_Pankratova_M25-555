from .constants import DIRECTIONS
from .player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from .utils import (
    attempt_open_treasure,
    check_win_condition,
    describe_current_room,
    handle_random_event,
    show_help,
    solve_puzzle,
)


def initialize_game():
    """Инициализирует начальное состояние игры."""
    return {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
        'solved_puzzles': set()
    }


def process_command(game_state, command):
    """Обрабатывает команду игрока."""
    parts = command.strip().lower().split()
    if not parts:
        return "Введите команду!"
    
    action = parts[0]
    
    if action in DIRECTIONS:
        return move_player(game_state, action)
    
    if action == 'quit' or action == 'exit':
        game_state['game_over'] = True
        return "Спасибо за игру! До свидания!"
    
    elif action == 'help':
        return show_help()
    
    elif action == 'look':
        return describe_current_room(game_state)
    
    elif action == 'inventory':
        return show_inventory(game_state)
    
    elif action == 'go':
        if len(parts) < 2:
            return "Укажите направление: go [north|south|east|west]"
        return move_player(game_state, parts[1])
    
    elif action == 'take':
        if len(parts) < 2:
            return "Укажите предмет: take [предмет]"
        return take_item(game_state, parts[1])
    
    elif action == 'use':
        if len(parts) < 2:
            return "Укажите предмет: use [предмет]"
        return use_item(game_state, parts[1])
    
    elif action == 'solve':
        # В treasure_room вместо solve_puzzle вызываем attempt_open_treasure
        if game_state['current_room'] == 'treasure_room':
            return attempt_open_treasure(game_state)
        return solve_puzzle(game_state)
    
    else:
        help_msg = "Введите 'help' для списка команд."
        return f"Неизвестная команда: {action}. {help_msg}"


def main():
    """Главный игровой цикл."""
    game_state = initialize_game()
    
    print(" Добро пожаловать в Лабиринт сокровищ!")
    print("=" * 50)
    print(describe_current_room(game_state))
    
    while not game_state['game_over']:
        try:
            command = get_input("\n> ")
            result = process_command(game_state, command)
            
            if result:
                print(result)
            
            if check_win_condition(game_state):
                win_msg = " ПОБЕДА! Вы нашли сокровище!"
                steps_msg = f"Количество шагов: {game_state['steps_taken']}"
                print(f"\n{win_msg}")
                print(steps_msg)
                game_state['game_over'] = True
                break
            
            if not game_state['game_over']:
                event_result = handle_random_event(game_state)
                if event_result:
                    print(f" {event_result}")
            
        except KeyboardInterrupt:
            print("\n\nИгра окончена. До свидания!")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()