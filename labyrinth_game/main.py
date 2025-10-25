from .constants import ROOMS, DIRECTIONS
from .player_actions import move_player, take_item, use_item, show_inventory, get_input
from .utils import describe_current_room, solve_puzzle, show_help, check_win_condition, handle_random_event, attempt_open_treasure


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
    
    # Обработка односложных команд направлений
    if action in DIRECTIONS:
        return move_player(game_state, action)
    
    match action:
        case 'quit' | 'exit':
            game_state['game_over'] = True
            return "Спасибо за игру! До свидания!"
        
        case 'help':
            return show_help()
        
        case 'look':
            return describe_current_room(game_state)
        
        case 'inventory':
            return show_inventory(game_state)
        
        case 'go':
            if len(parts) < 2:
                return "Укажите направление: go [north|south|east|west]"
            return move_player(game_state, parts[1])
        
        case 'take':
            if len(parts) < 2:
                return "Укажите предмет: take [предмет]"
            return take_item(game_state, parts[1])
        
        case 'use':
            if len(parts) < 2:
                return "Укажите предмет: use [предмет]"
            return use_item(game_state, parts[1])
        
        case 'solve':
            # В treasure_room вместо solve_puzzle вызываем attempt_open_treasure
            if game_state['current_room'] == 'treasure_room':
                return attempt_open_treasure(game_state)
            return solve_puzzle(game_state)
        
        case _:
            return f"Неизвестная команда: {action}. Введите 'help' для списка команд."


def main():
    """Главный игровой цикл."""
    game_state = initialize_game()
    
    print("🎮 Добро пожаловать в Лабиринт сокровищ!")
    print("=" * 50)
    print(describe_current_room(game_state))
    
    while not game_state['game_over']:
        try:
            command = get_input("\n> ")
            result = process_command(game_state, command)
            
            if result:
                print(f"\n{result}")
            
            if check_win_condition(game_state):
                print(f"\n🎉 ПОБЕДА! Вы нашли сокровище!")
                print(f"Количество шагов: {game_state['steps_taken']}")
                game_state['game_over'] = True
                break
            
            if not game_state['game_over']:
                event_result = handle_random_event(game_state)
                if event_result:
                    print(f"\n💫 {event_result}")
            
        except KeyboardInterrupt:
            print("\n\nИгра прервана. До свидания!")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()