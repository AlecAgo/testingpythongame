import json
import os
import time
import random
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Path to the JSON file where player data will be stored
DATA_FILE = 'player_data.json'
MESSAGES_FILE = 'messages.json'
ACCENT_COLORS = {
    'yellow': Fore.YELLOW,
    'red': Fore.RED,
    'blue': Fore.BLUE,
    'green': Fore.GREEN
}

# Load player data
def load_player_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}

# Save player data
def save_player_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Load messages
def load_messages():
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

# Save messages
def save_messages(messages):
    with open(MESSAGES_FILE, 'w') as file:
        json.dump(messages, file, indent=4)

# Register a new player
def register():
    username = input(Fore.CYAN + "Enter a username: ")
    password = input(Fore.CYAN + "Enter a password: ")
    player_data = load_player_data()

    if username in player_data:
        print(Fore.RED + "Username already exists. Please choose a different username.")
        return None

    player_data[username] = {
        'password': password,
        'money': 0,
        'last_login': time.time(),
        'apps': ['settings', 'jobs', 'bank', 'profile'],
        'accent_color': 'yellow',
        'job_levels': {'typing': {'level': 1, 'xp': 0}, 'verification': {'level': 1, 'xp': 0}},
        'bonus_cash': 0.0,
        'last_daily_reward': 0,
        'drop_shipping': {},
        'stock_market': {}
    }

    save_player_data(player_data)
    print(Fore.GREEN + f"User {username} registered successfully.")
    return username

# Log in an existing player
def login():
    username = input(Fore.CYAN + "Enter your username: ")
    password = input(Fore.CYAN + "Enter your password: ")
    player_data = load_player_data()

    if username in player_data and player_data[username]['password'] == password:
        print(Fore.GREEN + f"Welcome back, {username}!")
        return username
    else:
        print(Fore.RED + "Invalid username or password.")
        return None

# Display the phone menu
def phone_menu(username, player):
    while True:
        accent_color = ACCENT_COLORS[player['accent_color']]
        # Update the player's cash balance and apps
        player_data = load_player_data()
        player_data[username] = player
        save_player_data(player_data)

        print(accent_color + """
        📱 ------------- Phone Menu -------------
        | 1. Save and Exit
        | 2. Personal Profile
        | 3. Bank Account
        | 4. Jobs
        | 5. Settings
        | 6. App Store
        | 7. Apps Folder
        ----------------------------------------
        """)
        # Adjust time and display real-time
        current_time = (datetime.now() + timedelta(hours=3)).strftime("%I:%M %p")
        print(Fore.CYAN + f"Current Time (Beirut, Lebanon): {current_time}\n")

        choice = input(Fore.CYAN + "Choose an option: ")

        if choice == '1':
            # Save and Exit
            player_data = load_player_data()
            player_data[username] = player
            save_player_data(player_data)
            print(Fore.GREEN + "Game saved. Goodbye!")
            break
        elif choice == '2':
            # Personal Profile
            personal_profile(username, player)
        elif choice == '3':
            # Bank Account
            bank_account(player)
        elif choice == '4':
            # Jobs
            jobs(player)
        elif choice == '5':
            # Settings
            settings(player)
        elif choice == '6':
            # App Store
            app_store(player)
        elif choice == '7':
            # Apps Folder
            apps_folder(username, player)
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

# Handle personal profile
def personal_profile(username, player):
    while True:
        print(Fore.YELLOW + """
        📱 ------------- Personal Profile -------------
        | 1. View Username
        | 2. Change Password
        | 3. View Job Levels
        | 4. Exit
        -----------------------------------------------
        """)
        choice = input(Fore.CYAN + "Choose an option: ")

        if choice == '1':
            print(Fore.YELLOW + f"\nUsername: {username}")
        elif choice == '2':
            new_password = input(Fore.CYAN + "Enter new password: ")
            player['password'] = new_password
            print(Fore.GREEN + "Password changed successfully!")
        elif choice == '3':
            view_job_levels(player)
        elif choice == '4':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

# View job levels
def view_job_levels(player):
    for job, data in player['job_levels'].items():
        level = data['level']
        xp = data['xp']
        multiplier = 1.05 ** (level - 1)
        print(Fore.YELLOW + f"\nJob: {job.capitalize()}")
        print(Fore.YELLOW + f"Level: {level}, XP: {xp}/{15 * level}, Multiplier: x{multiplier:.2f}")

# Handle bank account
def bank_account(player):
    print(Fore.YELLOW + f"\nBank Account: ${player['money']:.2f}")

# Handle casino
def casino(player):
    while True:
        print(Fore.YELLOW + """
        📱 ------------- Casino -------------
        | 1. 50/50 Game
        | 2. Mine Game
        | 3. Exit
        -------------------------------------
        """)
        choice = input(Fore.CYAN + "Choose a game: ")

        if choice == '1':
            fifty_fifty_game(player)
        elif choice == '2':
            mine_game(player)
        elif choice == '3':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

# Function for 50/50 game
def fifty_fifty_game(player):
    print(Fore.YELLOW + "Rules: 50/50 chance of winning. Winning multiplies your bet by 1.9.")
    bet = float(input(Fore.CYAN + "Enter your bet amount: "))
    if bet > player['money']:
        print(Fore.RED + "You don't have enough money to bet that amount.")
    else:
        outcome = random.choice(['win', 'lose'])
        if outcome == 'win':
            winnings = bet * 1.9
            player['money'] += winnings
            print(Fore.GREEN + f"You won ${winnings:.2f}!")
        else:
            player['money'] -= bet
            print(Fore.RED + "You lost!")

# Function for mine game
def mine_game(player):
    print(Fore.YELLOW + "Rules: Uncover cash or mines. Winning multiplies your bet by 1.9, x3, and x4.1 for each win respectively. Max 3 wins per grid.")
    bet = float(input(Fore.CYAN + "Enter your bet amount: "))
    if bet > player['money']:
        print(Fore.RED + "You don't have enough money to bet that amount.")
        return

    grid = ['cash'] * 7 + ['mine'] * 9
    random.shuffle(grid)
    grid = [grid[i:i + 4] for i in range(0, 16, 4)]

    wins = 0
    available_squares = [f"{chr(65 + i)}{j + 1}" for i in range(4) for j in range(4)]

    while wins < 3:
        print(Fore.CYAN + f"Available squares: {', '.join(available_squares)}")
        choice = input(Fore.CYAN + "Choose a square (e.g., A1): ").upper()
        if choice not in available_squares:
            print(Fore.RED + "Invalid choice. Try again.")
            continue

        row, col = ord(choice[0]) - 65, int(choice[1]) - 1
        available_squares.remove(choice)

        if grid[row][col] == 'cash':
            if wins == 0:
                winnings = bet * 1.9
            elif wins == 1:
                winnings = bet * 3
            else:
                winnings = bet * 4.1
            player['money'] += winnings
            wins += 1
            print(Fore.GREEN + f"You found cash! Current winnings: ${winnings:.2f}")
            if wins < 3:
                continue_choice = input(Fore.CYAN + "Do you want to continue or leave with the cash? (continue/leave): ").lower()
                if continue_choice == 'leave':
                    return
        else:
            player['money'] -= bet
            print(Fore.RED + "You found a mine! You lost!")
            return
        if wins == 3:
            break

# Handle jobs
def jobs(player):
    while True:
        print(Fore.YELLOW + """
        📱 ------------- Jobs -------------
        | 1. Typing Job
        | 2. Verification Code
        | 3. Exit
        -----------------------------------
        """)
        choice = input(Fore.CYAN + "Choose a job: ")

        if choice == '1':
            typing_job(player)
        elif choice == '2':
            verification_job(player)
        elif choice == '3':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

# Typing job
def typing_job(player):
    job = 'typing'
    while True:
        letter = chr(random.randint(65, 90)) if random.choice([True, False]) else chr(random.randint(97, 122))
        answer = input(Fore.CYAN + f"Type the letter '{letter}': ")
        if answer == letter:
            xp = player['job_levels'][job]['xp'] + 1
            level = player['job_levels'][job]['level']
            multiplier = 1.05 ** (level - 1)
            if xp >= 15 * level:
                player['job_levels'][job]['xp'] = 0
                player['job_levels'][job]['level'] += 1
                player['bonus_cash'] += 15 * level / 2  # Bonus paychecks
                print(Fore.GREEN + f"Level up! You are now level {level + 1} in {job} job.")
            else:
                player['job_levels'][job]['xp'] = xp
            earnings = 0.20 * multiplier
            player['money'] += earnings
            print(Fore.GREEN + f"Correct! You earned ${earnings:.2f}.")
        else:
            print(Fore.RED + "Incorrect.")
        if input(Fore.CYAN + "Continue? (y/n): ").lower() != 'y':
            break

# Verification code job
def verification_job(player):
    job = 'verification'
    while True:
        code = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        answer = input(Fore.CYAN + f"Type the verification code '{code}': ")
        if answer == code:
            xp = player['job_levels'][job]['xp'] + 1
            level = player['job_levels'][job]['level']
            multiplier = 1.05 ** (level - 1)
            if xp >= 15 * level:
                player['job_levels'][job]['xp'] = 0
                player['job_levels'][job]['level'] += 1
                player['bonus_cash'] += 15 * level / 2  # Bonus paychecks
                print(Fore.GREEN + f"Level up! You are now level {level + 1} in {job} job.")
            else:
                player['job_levels'][job]['xp'] = xp
            earnings = 0.50 * multiplier
            player['money'] += earnings
            print(Fore.GREEN + f"Correct! You earned ${earnings:.2f}.")
        else:
            print(Fore.RED + "Incorrect.")
        if input(Fore.CYAN + "Continue? (y/n): ").lower() != 'y':
            break

# Handle settings
def settings(player):
    while True:
        print(Fore.YELLOW + """
        📱 ------------- Settings -------------
        | 1. Change Accent Color
        | 2. Exit
        ---------------------------------------
        """)
        choice = input(Fore.CYAN + "Choose an option: ")

        if choice == '1':
            change_accent_color(player)
        elif choice == '2':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

# Change accent color
def change_accent_color(player):
    print(Fore.YELLOW + """
    📱 ------------- Accent Colors -------------
    | 1. Yellow
    | 2. Red
    | 3. Blue
    | 4. Green
    -------------------------------------------
    """)
    choice = input(Fore.CYAN + "Choose a color: ")

    if choice == '1':
        player['accent_color'] = 'yellow'
    elif choice == '2':
        player['accent_color'] = 'red'
    elif choice == '3':
        player['accent_color'] = 'blue'
    elif choice == '4':
        player['accent_color'] = 'green'
    else:
        print(Fore.RED + "Invalid choice. Please try again.")
        return

    print(Fore.GREEN + "Accent color changed successfully!")

# Handle app store
def app_store(player):
    while True:
        print(Fore.YELLOW + """
        📱 ------------- App Store -------------
        | 1. Casino ($100)
        | 2. Player List ($30)
        | 3. Bonus Paychecks ($50)
        | 4. Daily Rewards ($40)
        | 5. Shopify ($150)
        | 6. Stock Market ($80)
        | 7. Twitter ($50)
        | 8. Exit
        ---------------------------------------
        """)
        choice = input(Fore.CYAN + "Choose an app to buy: ")

        if choice == '1':
            buy_casino_app(player)
        elif choice == '2':
            buy_player_list_app(player)
        elif choice == '3':
            buy_bonus_paychecks_app(player)
        elif choice == '4':
            buy_daily_rewards_app(player)
        elif choice == '5':
            buy_shopify_app(player)
        elif choice == '6':
            buy_stock_market_app(player)
        elif choice == '7':
            buy_twitter_app(player)
        elif choice == '8':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

# Buy the casino app
def buy_casino_app(player):
    if 'casino' in player['apps']:
        print(Fore.RED + "You already own the Casino app.")
        return

    print(Fore.YELLOW + """
    Casino App:
    - Play casino games with a 50/50 chance of winning.
    - Winning multiplies your bet by 1.9.
    """)
    confirm = input(Fore.CYAN + "Do you want to buy the Casino app for $100? (y/n): ")
    if confirm.lower() == 'y':
        if player['money'] >= 100:
            player['money'] -= 100
            player['apps'].append('casino')
            print(Fore.GREEN + "Casino app purchased successfully!")
        else:
            print(Fore.RED + "You don't have enough money to buy the Casino app.")
    else:
        print(Fore.YELLOW + "Purchase cancelled.")

# Buy the player list app
def buy_player_list_app(player):
    if 'player_list' in player['apps']:
        print(Fore.RED + "You already own the Player List app.")
        return

    print(Fore.YELLOW + """
    Player List App:
    - View all registered players' usernames and their current balance.
    """)
    confirm = input(Fore.CYAN + "Do you want to buy the Player List app for $30? (y/n): ")
    if confirm.lower() == 'y':
        if player['money'] >= 30:
            player['money'] -= 30
            player['apps'].append('player_list')
            print(Fore.GREEN + "Player List app purchased successfully!")
        else:
            print(Fore.RED + "You don't have enough money to buy the Player List app.")
    else:
        print(Fore.YELLOW + "Purchase cancelled.")

# Buy the bonus paychecks app
def buy_bonus_paychecks_app(player):
    if 'bonus_paychecks' in player['apps']:
        print(Fore.RED + "You already own the Bonus Paychecks app.")
        return

    print(Fore.YELLOW + """
    Bonus Paychecks App:
    - Earn half the total XP gained as cash when you level up in a job.
    """)
    confirm = input(Fore.CYAN + "Do you want to buy the Bonus Paychecks app for $50? (y/n): ")
    if confirm.lower() == 'y':
        if player['money'] >= 50:
            player['money'] -= 50
            player['apps'].append('bonus_paychecks')
            print(Fore.GREEN + "Bonus Paychecks app purchased successfully!")
        else:
            print(Fore.RED + "You don't have enough money to buy the Bonus Paychecks app.")
    else:
        print(Fore.YELLOW + "Purchase cancelled.")

# Buy the daily rewards app
def buy_daily_rewards_app(player):
    if 'daily_rewards' in player['apps']:
        print(Fore.RED + "You already own the Daily Rewards app.")
        return

    print(Fore.YELLOW + """
    Daily Rewards App:
    - Get $20 as a daily reward every 24 hours.
    """)
    confirm = input(Fore.CYAN + "Do you want to buy the Daily Rewards app for $40? (y/n): ")
    if confirm.lower() == 'y':
        if player['money'] >= 40:
            player['money'] -= 40
            player['apps'].append('daily_rewards')
            print(Fore.GREEN + "Daily Rewards app purchased successfully!")
        else:
            print(Fore.RED + "You don't have enough money to buy the Daily Rewards app.")
    else:
        print(Fore.YELLOW + "Purchase cancelled.")

# Buy the Shopify app
def buy_shopify_app(player):
    if 'shopify' in player['apps']:
        print(Fore.RED + "You already own the Shopify app.")
        return

    print(Fore.YELLOW + """
    Shopify App:
    - Drop ship items and manage your online shop.
    """)
    confirm = input(Fore.CYAN + "Do you want to buy the Shopify app for $150? (y/n): ")
    if confirm.lower() == 'y':
        if player['money'] >= 150:
            player['money'] -= 150
            player['apps'].append('shopify')
            print(Fore.GREEN + "Shopify app purchased successfully!")
        else:
            print(Fore.RED + "You don't have enough money to buy the Shopify app.")
    else:
        print(Fore.YELLOW + "Purchase cancelled.")

# Buy the stock market app
def buy_stock_market_app(player):
    if 'stock_market' in player['apps']:
        print(Fore.RED + "You already own the Stock Market app.")
        return

    print(Fore.YELLOW + """
    Stock Market App:
    - Invest in stocks and watch your money grow or shrink.
    """)
    confirm = input(Fore.CYAN + "Do you want to buy the Stock Market app for $80? (y/n): ")
    if confirm.lower() == 'y':
        if player['money'] >= 80:
            player['money'] -= 80
            player['apps'].append('stock_market')
            print(Fore.GREEN + "Stock Market app purchased successfully!")
        else:
            print(Fore.RED + "You don't have enough money to buy the Stock Market app.")
    else:
        print(Fore.YELLOW + "Purchase cancelled.")

# Buy the Twitter app
def buy_twitter_app(player):
    if 'twitter' in player['apps']:
        print(Fore.RED + "You already own the Twitter app.")
        return

    print(Fore.YELLOW + """
    Twitter App:
    - Post messages and see messages from other users.
    """)
    confirm = input(Fore.CYAN + "Do you want to buy the Twitter app for $50? (y/n): ")
    if confirm.lower() == 'y':
        if player['money'] >= 50:
            player['money'] -= 50
            player['apps'].append('twitter')
            print(Fore.GREEN + "Twitter app purchased successfully!")
        else:
            print(Fore.RED + "You don't have enough money to buy the Twitter app.")
    else:
        print(Fore.YELLOW + "Purchase cancelled.")

# Handle apps folder
def apps_folder(username, player):
    while True:
        print(Fore.YELLOW + "\n📱 ------------- Apps Folder -------------")
        for idx, app in enumerate(player['apps']):
            if app not in ['settings', 'jobs', 'bank', 'profile']:
                print(f"| {idx + 1}. {app.capitalize()}")
        print("| 0. Exit")
        print("----------------------------------------")
        choice = input(Fore.CYAN + "Choose an app to open: ")

        if choice == '0':
            break
        else:
            try:
                app_choice = player['apps'][int(choice) - 1]
                if app_choice == 'casino':
                    casino(player)
                elif app_choice == 'player_list':
                    player_list()
                elif app_choice == 'bonus_paychecks':
                    bonus_paychecks(player)
                elif app_choice == 'daily_rewards':
                    daily_rewards(player)
                elif app_choice == 'shopify':
                    shopify(player)
                elif app_choice == 'stock_market':
                    stock_market(player)
                elif app_choice == 'twitter':
                    twitter(username, player)
                else:
                    print(Fore.RED + "Invalid choice. Please try again.")
            except (IndexError, ValueError):
                print(Fore.RED + "Invalid choice. Please try again.")

# Handle daily rewards
def daily_rewards(player):
    current_time = time.time()
    last_reward_time = player.get('last_daily_reward', 0)
    if current_time - last_reward_time >= 86400:  # 24 hours in seconds
        player['money'] += 20
        player['last_daily_reward'] = current_time
        print(Fore.GREEN + "You have received $20 daily reward!")
    else:
        time_left = 86400 - (current_time - last_reward_time)
        hours, remainder = divmod(time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(Fore.YELLOW + f"Time left for next reward: {int(hours)}h {int(minutes)}m {int(seconds)}s")

# Handle Shopify app
def shopify(player):
    while True:
        print(Fore.YELLOW + """
        📱 ------------- Shopify -------------
        | 1. View Online Shop
        | 2. View Drop Shipping Status
        | 3. Exit
        -------------------------------------
        """)
        choice = input(Fore.CYAN + "Choose an option: ")

        if choice == '1':
            view_online_shop(player)
        elif choice == '2':
            view_drop_shipping_status(player)
        elif choice == '3':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def view_online_shop(player):
    items = {
        "LED lights": 10, "Hairdryer": 20, "Phone case": 5, "Headphones": 15,
        "Bluetooth speaker": 25, "Laptop stand": 30, "Wireless mouse": 10,
        "Keyboard": 20, "Monitor": 100, "Desk lamp": 15, "USB hub": 10,
        "Smartwatch": 50, "Fitness tracker": 40, "Backpack": 30, "Water bottle": 10,
        "Sneakers": 60, "Sunglasses": 20, "Wallet": 15, "Belt": 10, "Hat": 15
    }

    print(Fore.YELLOW + "\nAvailable items to drop ship:")
    for item, price in items.items():
        print(f"- {item}: ${price}")

    item_choice = input(Fore.CYAN + "Enter the item you want to drop ship: ").strip()
    if item_choice not in items:
        print(Fore.RED + "Invalid item choice.")
        return

    price = items[item_choice]
    stock = int(input(Fore.CYAN + f"Enter the stock amount (1-10) for {item_choice} at ${price} each: ").strip())
    if stock < 1 or stock > 10:
        print(Fore.RED + "Invalid stock amount.")
        return

    total_cost = price * stock
    if total_cost > player['money']:
        print(Fore.RED + "You don't have enough money to purchase the stock.")
        return

    player['money'] -= total_cost
    player['drop_shipping'] = {
        "item": item_choice,
        "price": price,
        "stock": stock,
        "start_time": time.time(),
        "end_time": time.time() + 18000  # 5 hours in seconds
    }
    print(Fore.GREEN + f"You have successfully purchased {stock} units of {item_choice} for drop shipping.")

def view_drop_shipping_status(player):
    drop_shipping = player.get('drop_shipping', {})
    if not drop_shipping:
        print(Fore.YELLOW + "No active drop shipping at the moment.")
        return

    current_time = time.time()
    if current_time < drop_shipping['end_time']:
        time_left = drop_shipping['end_time'] - current_time
        hours, remainder = divmod(time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(Fore.YELLOW + f"Time left for drop shipping: {int(hours)}h {int(minutes)}m {int(seconds)}s")
        return

    stock_sold = random.randint(0, drop_shipping['stock'])
    revenue = stock_sold * drop_shipping['price'] * 1.5
    player['money'] += revenue
    print(Fore.GREEN + f"Drop shipping completed. You sold {stock_sold} units and earned ${revenue:.2f}.")
    player['drop_shipping'] = {}

# Handle stock market
def stock_market(player):
    while True:
        print(Fore.YELLOW + """
        📱 ------------- Stock Market -------------
        | 1. Invest in Stocks
        | 2. View Investments
        | 3. Exit
        ------------------------------------------
        """)
        choice = input(Fore.CYAN + "Choose an option: ")

        if choice == '1':
            invest_in_stocks(player)
        elif choice == '2':
            view_investments(player)
        elif choice == '3':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def invest_in_stocks(player):
    stocks = {"Apple": 1, "Google": 2, "Meta": 3}
    print(Fore.YELLOW + "Available stocks:")
    for stock in stocks:
        print(f"- {stock}")

    stock_choice = input(Fore.CYAN + "Enter the stock you want to invest in: ").strip()
    if stock_choice not in stocks:
        print(Fore.RED + "Invalid stock choice.")
        return

    if stock_choice in player['stock_market']:
        print(Fore.RED + "You already have an active investment in this stock.")
        return

    amount = float(input(Fore.CYAN + "Enter the amount to invest ($5-$500): ").strip())
    if amount < 5 or amount > 500:
        print(Fore.RED + "Invalid investment amount.")
        return

    if amount > player['money']:
        print(Fore.RED + "You don't have enough money to invest.")
        return

    player['money'] -= amount
    player['stock_market'][stock_choice] = {
        "amount": amount,
        "start_time": time.time(),
        "end_time": time.time() + 3600  # 1 hour in seconds
    }
    print(Fore.GREEN + f"You have successfully invested ${amount} in {stock_choice} stock.")

def view_investments(player):
    investments = player.get('stock_market', {})
    if not investments:
        print(Fore.YELLOW + "No active investments at the moment.")
        return

    for stock, data in investments.items():
        current_time = time.time()
        if current_time < data['end_time']:
            time_left = data['end_time'] - current_time
            hours, remainder = divmod(time_left, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(Fore.YELLOW + f"Time left for {stock} investment: {int(hours)}h {int(minutes)}m {int(seconds)}s")
        else:
            change = random.uniform(-1, 1)  # Change from -1 (100% loss) to +1 (100% gain)
            new_amount = data['amount'] * (1 + change)
            player['money'] += new_amount
            print(Fore.GREEN + f"Investment in {stock} completed. You {('lost', 'gained')[change > 0]} ${abs(new_amount - data['amount']):.2f}.")
            del player['stock_market'][stock]

# Handle Twitter app
def twitter(username, player):
    while True:
        print(Fore.YELLOW + """
        📱 ------------- Twitter -------------
        | 1. View Messages
        | 2. Post a Message ($25)
        | 3. Exit
        -------------------------------------
        """)
        choice = input(Fore.CYAN + "Choose an option: ")

        if choice == '1':
            view_messages()
        elif choice == '2':
            post_message(username, player)
        elif choice == '3':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def view_messages():
    messages = load_messages()
    print(Fore.YELLOW + "\nMessages:")
    for message in messages:
        print(f"- {message['username']}: {message['message']}")
    print("-------------------------------------")

def post_message(username, player):
    if player['money'] < 25:
        print(Fore.RED + "You don't have enough money to post a message.")
        return

    message = input(Fore.CYAN + "Enter your message: ").strip()
    if not message:
        print(Fore.RED + "Message cannot be empty.")
        return

    player['money'] -= 25
    messages = load_messages()
    messages.append({"username": username, "message": message})
    save_messages(messages)
    print(Fore.GREEN + "Message posted successfully!")

# Function to claim bonus paychecks
def bonus_paychecks(player):
    if player['bonus_cash'] > 0:
        print(Fore.YELLOW + f"\nYou have ${player['bonus_cash']:.2f} to claim.")
        claim = input(Fore.CYAN + "Do you want to claim your bonus cash? (y/n): ")
        if claim.lower() == 'y':
            player['money'] += player['bonus_cash']
            player['bonus_cash'] = 0.0
            print(Fore.GREEN + "Bonus cash claimed successfully!")
        else:
            print(Fore.YELLOW + "Claim cancelled.")
    else:
        print(Fore.YELLOW + "\nNo bonus cash to claim.")

# Function to view player list
def player_list():
    player_data = load_player_data()
    print(Fore.YELLOW + "\n📱 ------------- Player List -------------")
    for username, data in player_data.items():
        print(Fore.YELLOW + f"Username: {username}, Balance: ${data['money']:.2f}")
    print("----------------------------------------")

# Main game function
def main():
    print(Fore.MAGENTA + Style.BRIGHT + """
    Welcome to Real Life Simulator!
    """)
    choice = input(Fore.CYAN + "Do you want to (1) Register or (2) Login? ")

    if choice == '1':
        username = register()
    elif choice == '2':
        username = login()
    else:
        print(Fore.RED + "Invalid choice. Exiting the game.")
        return

    if not username:
        return

    # Load the player's data
    player_data = load_player_data()
    player = player_data[username]

    # Update last login time
    player['last_login'] = time.time()
    save_player_data(player_data)

    # Game loop with phone menu
    phone_menu(username, player)

if __name__ == "__main__":
    main()
