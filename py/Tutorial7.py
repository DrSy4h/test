from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

mongo_uri = os.getenv("MONGODB_ATLAS_CLUSTER_URI")
db_name = os.getenv("MONGODB_DATABASE_NAME", "example_db")

def format_datetime(dt):
    """Format datetime untuk display yang lebih cantik"""
    if dt:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return "N/A"

class Database:
    def __init__(self, db_name=db_name, connection_string=mongo_uri):
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client[db_name]
            self.users_collection = self.db.users
            self.posts_collection = self.db.posts
            self.init_database()
            print(f"✅ Connected to MongoDB database: {db_name}")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")

    def init_database(self):
        """Initialize the database with collections and indexes"""
        self.users_collection.create_index("email", unique=True)
        self.posts_collection.create_index("user_id")

    def create_user(self, name, email, age):
        """Create a new user"""
        try:
            user = {
                "name": name,
                "email": email,
                "age": age,
                "created_at": datetime.now()
            }
            result = self.users_collection.insert_one(user)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def create_post(self, user_id, title, content):
        """Create a new post"""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            post_doc = {
                "user_id": user_object_id,
                "title": title,
                "content": content,
                "created_at": datetime.now()
            }
            result = self.posts_collection.insert_one(post_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_all_users(self):
        """Get all users"""
        try:
            users = list(self.users_collection.find())
            for user in users:
                user['_id'] = str(user['_id'])  # Convert ObjectId to string
            return users
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_user_posts(self, user_id):
        """Get all posts by user"""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            posts = list(self.posts_collection.find({"user_id": user_object_id}).sort("created_at", -1))

            for post in posts:
                post['_id'] = str(post['_id'])  # Convert ObjectId to string
                post['user_id'] = str(post['user_id'])  # Convert ObjectId to string
            return posts
        except Exception as e:
            print(f"Error: {e}")
            return []

    def delete_user(self, user_id):
        """delete a user and their posts"""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            self.posts_collection.delete_many({"user_id": user_object_id})

            result = self.users_collection.delete_one({"_id": user_object_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error: {e}")
            return False

    def close_connection(self):
        """Close the MongoDB connection"""
        self.client.close()


def display_menu():
    """Display the main menu"""
    print("=== MongoDB Tutorial Menu ===")
    print("\n" + "=" * 40)
    print("DATABASE MANAGER")
    print("=" * 40)
    print("1. Create User")
    print("2. View All Users")
    print("3. Create Post")
    print("4. View User Posts")
    print("5. Delete User")
    print("6. Exit")
    print("=" * 40)


def main():
    """Main interactive CLI function"""
    try:
        db = Database()
        print("Connected to MongoDB database.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            print("\n---Create User---")
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            try:
                age = int(input("Enter age: ").strip())
            except ValueError:
                print("Invalid age. Please enter a number.")
                continue
            user_id = db.create_user(name, email, age)
            if user_id:
                print(f"User created with id: {user_id}")
            else:
                print("Failed to create user.")
        
            

        elif choice == "2":
            print("\n--- All Users---")
            users = db.get_all_users()
            if users:
                for user in users:
                    created_at = format_datetime(user['created_at'])
                    print(f"User ID: {user['_id']}, Name: {user['name']}, Email: {user['email']}, Age: {user['age']}, Created At: {created_at}")
            else:
                print("No users found.")

        elif choice == "3":
            print("\n--- Create New Post ---")
            user_id = input("Enter user ID: ").strip()
            title = input("Enter post title: ").strip()
            content = input("Enter post content: ").strip()
            post_id = db.create_post(user_id, title, content)
            if post_id:
                print(f"Post created successfully! ID: {post_id}")
            else:
                print("Failed to create post.")

        elif choice == "4":
            print("\n--- View User Posts ---")
            user_id = input("Enter user ID: ").strip()
            posts = db.get_user_posts(user_id)
            if posts:
                for post in posts:
                    created_at = format_datetime(post['created_at'])
                    print(f"\nPost ID: {post['_id']}")
                    print(f"Title: {post['title']}")
                    print(f"Content: {post['content']}")
                    print(f"Created At: {created_at}")
                    print("-" * 30)

            else:
                print("No posts found for this user.")


        elif choice == "5":
            print("\n--- Delete User ---")
            user_id = input("Enter user ID to delete: ").strip()
            confirm = input(f"Are you sure you want to delete user {user_id} and all their posts? (y/nN: ").strip().lower()
            if confirm == 'y':
               if db.delete_user(user_id):
                    print("User and their posts deleted successfully.")
               else:
                    print("Failed to delete user. Please check the user ID.")
            else:
                print("Deletion cancelled.")

        elif choice == "6":
            print("\nClosing database connection....")
            db.close_connection()
            print("See you again!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()         
                            
