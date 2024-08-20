import random
from datetime import datetime

def generate_unique_id(min_value=1000, max_value=9999):
    return random.randint(min_value, max_value)

class User:
    def __init__(self, username, contact_info):
        self.user_id = generate_unique_id()
        self.username = username
        self.contact_info = contact_info
        self.auctions = []
        self.bids = []
    
    def create_auction(self, item_name, starting_price, auction_system):
        auction = Auction(self, item_name, starting_price)
        self.auctions.append(auction)
        auction_system.add_auction(auction)
        print(f"Auction created for '{item_name}' by {self.username} with ID {auction.auction_id}.")

    def place_bid(self, auction_id, amount, auction_system):
        auction = auction_system.get_auction(auction_id)
        if auction:
            if auction.place_bid(self, amount):
                self.bids.append((auction_id, amount))
                print(f"Bid of {amount} placed on auction '{auction.item_name}' by {self.username}.")
            else:
                print(f"Failed to place bid. Bid amount must be higher than the current highest bid.")
        else:
            print(f"No auction found with ID {auction_id}.")
    
    def view_auctions(self, auction_system):
        auction_system.display_auctions()
    
    def view_bids(self):
        if self.bids:
            print(f"Bids placed by {self.username}:")
            for auction_id, amount in self.bids:
                print(f"Auction ID: {auction_id}, Bid Amount: {amount}")
        else:
            print(f"{self.username} has not placed any bids yet.")
    
    def view_my_auctions(self):
        if self.auctions:
            print(f"Auctions created by {self.username}:")
            for auction in self.auctions:
                auction.display_details()
        else:
            print(f"{self.username} has not created any auctions yet.")

class Auction:
    def __init__(self, auctioneer, item_name, starting_price):
        self.auction_id = generate_unique_id()
        self.auctioneer = auctioneer
        self.item_name = item_name
        self.starting_price = starting_price
        self.bids = []
        self.highest_bid = None
        self.is_active = True
    
    def place_bid(self, bidder, amount):
        if self.is_active and (self.highest_bid is None or amount > self.highest_bid['amount']):
            self.highest_bid = {'bidder': bidder, 'amount': amount, 'time': datetime.now()}
            self.bids.append(self.highest_bid)
            return True
        return False
    
    def close_auction(self):
        self.is_active = False
        if self.highest_bid:
            print(f"Auction '{self.item_name}' closed. Winner: {self.highest_bid['bidder'].username} with bid of {self.highest_bid['amount']}.")
        else:
            print(f"Auction '{self.item_name}' closed with no bids.")
    
    def display_details(self):
        print(f"Auction ID: {self.auction_id}")
        print(f"Item: {self.item_name}")
        print(f"Starting Price: {self.starting_price}")
        print(f"Highest Bid: {self.highest_bid['amount'] if self.highest_bid else 'None'}")
        print(f"Auctioneer: {self.auctioneer.username}")
        print(f"Status: {'Active' if self.is_active else 'Closed'}")
        print("Bids:")
        for bid in self.bids:
            print(f"  Bidder: {bid['bidder'].username}, Amount: {bid['amount']}, Time: {bid['time']}")
        print()

class AuctionSystem:
    def __init__(self):
        self.auctions = {}
    
    def add_auction(self, auction):
        self.auctions[auction.auction_id] = auction
    
    def get_auction(self, auction_id):
        return self.auctions.get(auction_id)
    
    def display_auctions(self):
        if self.auctions:
            print("Current Auctions:")
            for auction in self.auctions.values():
                auction.display_details()
        else:
            print("No active auctions available.")
    
    def close_auction(self, auction_id):
        auction = self.get_auction(auction_id)
        if auction:
            auction.close_auction()
        else:
            print(f"No auction found with ID {auction_id}.")

class UserSystem:
    def __init__(self):
        self.users = {}

    def register_user(self, username, contact_info):
        user = User(username, contact_info)
        self.users[username] = user
        return user

    def get_user(self, username):
        return self.users.get(username)

def main():
    auction_system = AuctionSystem()
    user_system = UserSystem()

    while True:
        print("\n--- Online Auction System ---")
        print("1. Register User")
        print("2. Create Auction")
        print("3. Place Bid")
        print("4. View All Auctions")
        print("5. View My Auctions")
        print("6. View My Bids")
        print("7. Close Auction")
        print("8. Exit")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            username = input("Enter username: ").strip()
            contact_info = input("Enter contact info: ").strip()
            user = user_system.register_user(username, contact_info)
            print(f"User '{username}' registered with ID {user.user_id}.")

        elif choice == '2':
            username = input("Enter your username: ").strip()
            user = user_system.get_user(username)
            if user:
                item_name = input("Enter item name: ").strip()
                starting_price = float(input("Enter starting price: ").strip())
                user.create_auction(item_name, starting_price, auction_system)
            else:
                print(f"No user found with username '{username}'.")

        elif choice == '3':
            username = input("Enter your username: ").strip()
            user = user_system.get_user(username)
            if user:
                auction_id = int(input("Enter auction ID: ").strip())
                amount = float(input("Enter your bid amount: ").strip())
                user.place_bid(auction_id, amount, auction_system)
            else:
                print(f"No user found with username '{username}'.")

        elif choice == '4':
            auction_system.display_auctions()

        elif choice == '5':
            username = input("Enter your username: ").strip()
            user = user_system.get_user(username)
            if user:
                user.view_my_auctions()
            else:
                print(f"No user found with username '{username}'.")

        elif choice == '6':
            username = input("Enter your username: ").strip()
            user = user_system.get_user(username)
            if user:
                user.view_bids()
            else:
                print(f"No user found with username '{username}'.")

        elif choice == '7':
            auction_id = int(input("Enter auction ID to close: ").strip())
            auction_system.close_auction(auction_id)

        elif choice == '8':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
