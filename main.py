import tweepy
import time
import json
from typing import List, Set

class TwitterFollower:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str, bearer_token: str):
        """Initialize the Twitter API v2 client"""
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )

    def get_user_followers(self, username: str) -> Set[str]:
        """Get the list of user IDs that are following the specified user"""
        followers = set()
        try:
            # First get user ID from username
            user = self.client.get_user(username=username)
            if not user.data:
                print(f"User {username} not found")
                return followers
            
            user_id = user.data.id
            
            # Then get followers using pagination
            for response in tweepy.Paginator(
                self.client.get_users_followers,
                user_id,
                max_results=100  # Maximum allowed by Twitter
            ):
                if response.data:
                    for follower in response.data:
                        followers.add(follower.id)
                        print(f"Found follower: {follower.username}")
                    print(f"Found batch of {len(response.data)} followers...")
                time.sleep(2)  # Rate limiting
                
        except tweepy.TweepyException as e:
            print(f"Error fetching followers for {username}: {str(e)}")
        return followers

    def get_user_following(self, username: str) -> Set[str]:
        """Get the list of user IDs that the specified user is following"""
        following = set()
        try:
            # Get user ID from username
            user = self.client.get_user(username=username)
            if not user.data:
                print(f"User {username} not found")
                return following
            
            user_id = user.data.id
            
            # Get following using pagination
            for response in tweepy.Paginator(
                self.client.get_users_following,
                user_id,
                max_results=100
            ):
                if response.data:
                    for followed_user in response.data:
                        following.add(followed_user.id)
                        print(f"Found following: {followed_user.username}")
                    print(f"Found batch of {len(response.data)} following...")
                time.sleep(2)  # Rate limiting
                
        except tweepy.TweepyException as e:
            print(f"Error fetching following for {username}: {str(e)}")
        return following

    def follow_users(self, user_ids: Set[str]) -> int:
        """Follow the specified users"""
        followed_count = 0
        for user_id in user_ids:
            try:
                self.client.follow_user(user_id)
                user = self.client.get_user(id=user_id).data
                followed_count += 1
                print(f"Followed user: @{user.username}")
                time.sleep(2)  # Rate limiting
            except tweepy.TweepyException as e:
                print(f"Error following user {user_id}: {str(e)}")
        return followed_count

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
    follower = TwitterFollower(
        config['api_key'],
        config['api_secret'],
        config['access_token'],
        config['access_token_secret'],
        config['bearer_token']
    )
    
    # Get target user's followers and following
    target_user = "xDevLo"
    print(f"Fetching followers of {target_user}...")
    followers = follower.get_user_followers(target_user)
    
    print(f"\nFetching users that {target_user} is following...")
    following = follower.get_user_following(target_user)
    
    # Find users to follow back (followers who aren't followed yet)
    users_to_follow = followers - following
    
    # Follow back
    print(f"\nFound {len(followers)} total followers")
    print(f"Already following {len(following)} users")
    print(f"Will follow back {len(users_to_follow)} new users")
    
    if users_to_follow:
        print("\nStarting to follow back users...")
        followed = follower.follow_users(users_to_follow)
        print(f"\nOperation complete!")
        print(f"Successfully followed back {followed} users")
    else:
        print("\nNo new users to follow back!")

if __name__ == "__main__":
    main()