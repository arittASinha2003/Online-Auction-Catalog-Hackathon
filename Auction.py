import time
import threading

class Auction:
    def __init__(self, item_name, starting_bid, duration):
        self.item_name = item_name
        self.current_bid = starting_bid
        self.highest_bidder = None
        self.auction_active = True
        self.duration = duration
        self.lock = threading.Lock()

    def place_bid(self, user, bid_amount):
        with self.lock:
            if not self.auction_active:
                return False

            if bid_amount <= self.current_bid:
                print(f"Bid too low! Current highest bid is {self.current_bid}")
                return False

            self.current_bid = bid_amount
            self.highest_bidder = user
            print(f"{user} placed a bid of {bid_amount} on {self.item_name}.")
            return True

    def close_auction(self):
        with self.lock:
            if self.highest_bidder:
                print(f"Auction for {self.item_name} closed!\nWinning bid: {self.current_bid} by {self.highest_bidder}.")
            else:
                print(f"Auction for {self.item_name} closed with no bids.")
            self.auction_active = False
            print("\nExiting the auction system...")

    def start_auction(self):
        print(f"Auction for {self.item_name} started with a starting bid of {self.current_bid}.")
        timer = threading.Timer(self.duration, self.close_auction)
        timer.start()

class User:
    def __init__(self, name):
        self.name = name

    def bid(self, auction, amount):
        return auction.place_bid(self.name, amount)

class AuctionSystem:
    def __init__(self):
        self.users = {}

    def get_user(self, name):
        if name not in self.users:
            self.users[name] = User(name)
        return self.users[name]

    def create_auction(self, item_name, starting_bid, duration):
        auction = Auction(item_name, starting_bid, duration)
        print(f"Auction for {item_name} created with a starting bid of {starting_bid}.")
        return auction

# Function to get user inputs and manage the auction process
def main():
    print("\nWelcome to the Online Auction System!\n")
    auction_system = AuctionSystem()

    # Create an Auction
    item_name = input("Enter item name for auction: ")
    starting_bid = float(input("Enter starting bid: "))
    duration = int(input("Enter auction duration in seconds: "))
    auction = auction_system.create_auction(item_name, starting_bid, duration)
    auction.start_auction()

    # Users Place Bids
    while auction.auction_active:
        try:
            name = input("\nEnter name to place bid: ")
            if not auction.auction_active:
                break

            user = auction_system.get_user(name)
            bid_amount = float(input("Enter bid amount: "))
            if not user.bid(auction, bid_amount):
                break

        except KeyboardInterrupt:
            auction.close_auction()
            break

    if auction.auction_active:
        auction.close_auction()

    print("Auction process completed.")

if __name__ == "__main__":
    main()
