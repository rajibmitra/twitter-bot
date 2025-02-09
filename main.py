import tweepy
import time
import json
from typing import List, Set

class TwitterFollower:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        """Initialize the Twitter API client"""
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        
    def get_following_ids(self) -> Set[int]:
        """Get the list of user IDs that we are following"""
        following = set()
        for page in tweepy.Cursor(self.api.get_friend_ids).pages():
            following.update(page)
            time.sleep(1)  
        return following
    
    def get_target_follow_list(self, target_user: str) -> Set[int]:
        """Get the follower IDs of the target user"""
        target_followers = set()
        try:
            for page in tweepy.Cursor(self.api.get_follower_ids, screen_name=target_user).pages():
                target_followers.update(page)
                time.sleep(1)  
        except tweepy.TweepError as e:
            print(f"Error fetching followers for {target_user}: {str(e)}")
        return target_followers
    
    def sync_following(self, target_followers: Set[int]):
        """Sync our following list with the target followers"""
        current_following = self.get_following_ids()
        
        # Users to unfollow (those we follow but aren't in target list)
        to_unfollow = current_following - target_followers
        
        # Users to follow (those in target list but we don't follow)
        to_follow = target_followers - current_following
        
        # Unfollow users
        print(f"Unfollowing {len(to_unfollow)} users...")
        for user_id in to_unfollow:
            try:
                self.api.destroy_friendship(user_id)
                print(f"Unfollowed user {user_id}")
                time.sleep(2)  
            except tweepy.TweepError as e:
                print(f"Error unfollowing {user_id}: {str(e)}")
        
        # Follow new users
        print(f"Following {len(to_follow)} new users...")
        for user_id in to_follow:
            try:
                self.api.create_friendship(user_id)
                print(f"Followed user {user_id}")
                time.sleep(2)  
            except tweepy.TweepError as e:
                print(f"Error following {user_id}: {str(e)}")

def load_config(config_path: str = 'config.json') -> dict:
    """Load Twitter API credentials from config file"""
    with open(config_path) as f:
        return json.load(f)

def main():
    # Load configuration
    try:
        config = load_config()
    except FileNotFoundError:
        print("Please create a config.json file with your Twitter API credentials")
        return
    
    # Initialize the follower manager
    manager = TwitterFollowerManager(
        config['api_key'],
        config['api_secret'],
        config['access_token'],
        config['access_token_secret']
    )
    
    # Get the target user whose followers we want to sync with
    target_user = input("Enter the Twitter username to sync followers with: ")
    
    # Get target user's followers
    print(f"Fetching followers for {target_user}...")
    target_followers = manager.get_target_follow_list(target_user)
    
    # Sync our following list
    print("Starting sync process...")
    manager.sync_following(target_followers)
    print("Sync complete!")

if __name__ == "__main__":
    main()