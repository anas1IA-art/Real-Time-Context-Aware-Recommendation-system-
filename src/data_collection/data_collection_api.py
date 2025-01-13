import random
import faker
import json
import time
from datetime import datetime


class DynamicDataCollectionAPI:
    def __init__(self, initial_users=5, interval=2, dynamic_users=True):
        """
        Initialize the DynamicDataCollectionAPI with the initial number of users,
        the interval for real-time simulation, and whether user count is dynamic.
        """
        self.users = []  # List of users
        self.interval = interval
        self.dynamic_users = dynamic_users  # Toggle for dynamic user management
        self.fake = faker.Faker()

        # Initialize with the initial number of users
        for _ in range(initial_users):
            self.users.append(self.generate_random_user())

    def generate_random_user(self):
        """
        Generate a random user with associated location and weather information.
        """
        return {
            "user_id": f"u{random.randint(100, 999)}",
            "name": self.fake.name(),
            "email": self.fake.email(),
            "location": self.generate_random_location()
        }

    def generate_random_location(self):
        """
        Generate a random location with weather, nearby places, and reviews.
        """
        location = {
            "location_id": f"l{random.randint(100, 999)}",
            "name": self.fake.city(),
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6),
            "weather": self.generate_random_weather(),
            "nearby_places": self.generate_nearby_places()
        }

        # Add reviews to each nearby place
        for place in location["nearby_places"]:
            place["reviews"] = self.generate_reviews_for_place()

        return location

    def generate_random_weather(self):
        """
        Generate random weather conditions for a location.
        """
        weather_conditions = ["Clear", "Cloudy", "Rain", "Thunderstorms", "Snow", "Windy"]
        return {
            "temperature": round(random.uniform(-30, 50), 1),
            "conditions": random.choice(weather_conditions),
            "humidity": random.randint(0, 100),
            "wind_speed": round(random.uniform(0, 15), 1)
        }

    def generate_nearby_places(self):
        """
        Generate a list of nearby places within a location.
        """
        return [
            {
                "place_id": f"p{random.randint(1000, 9999)}",
                "name": self.fake.company(),
                "distance_km": round(random.uniform(0.5, 10), 2)
            }
            for _ in range(random.randint(2, 5))
        ]

    def generate_reviews_for_place(self, max_reviews=5):
        """
        Generate a list of reviews for a specific place.

        :param max_reviews: Maximum number of reviews for a place.
        :return: A list of review dictionaries.
        """
        reviews = []
        for _ in range(random.randint(1, max_reviews)):
            reviews.append(self.generate_random_review())
        return reviews

    def generate_random_review(self):
        """
        Generate a random review with text, rating, and user information.
        """
        return {
            "review_id": f"r{random.randint(10000, 99999)}",
            "user_name": self.fake.name(),
            "rating": random.randint(1, 5),  # 1 to 5 stars
            "review_text": self.fake.text(max_nb_chars=200),
            "timestamp": self.fake.date_time_this_year().isoformat()
        }

    def update_users_dynamic(self):
        """
        Simulate user churn by dynamically adding and removing users.
        """
        # Add new users
        num_new_users = random.randint(0, 3)
        for _ in range(num_new_users):
            self.users.append(self.generate_random_user())

        # Remove random users
        num_users_to_remove = random.randint(0, min(3, len(self.users)))
        for _ in range(num_users_to_remove):
            self.users.pop(random.randint(0, len(self.users) - 1))

    def update_users_fixed(self, num_users):
        """
        Maintain a fixed number of users by ensuring the list matches the given number.
        """
        current_users = len(self.users)

        if current_users < num_users:
            for _ in range(num_users - current_users):
                self.users.append(self.generate_random_user())
        elif current_users > num_users:
            for _ in range(current_users - num_users):
                self.users.pop(random.randint(0, len(self.users) - 1))

    def generate_real_time_data(self, num_users=None):
        """
        Generate real-time simulated data with either fixed or dynamic user management.

        :param num_users: Fixed number of users (if dynamic_users is False).
        """
        try:
            while True:
                if self.dynamic_users:
                    self.update_users_dynamic()
                else:
                    if num_users is not None:
                        self.update_users_fixed(num_users)

                # Generate and print the current user data
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.print_data_with_timestamp(self.users, timestamp)

                # Simulate real-time interval
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Real-time data generation stopped.")

    def print_data_with_timestamp(self, data, timestamp):
        """
        Print the generated data with timestamp in a formatted JSON structure.

        :param data: The data to print (list of user data).
        :param timestamp: The current timestamp for real-time simulation.
        """
        print(f"Timestamp: {timestamp}")
        print(json.dumps(data, indent=4))


# Usage Example
if __name__ == "__main__":
    # Test with dynamic user management
    print("Testing Dynamic User Management:")
    api_dynamic = DynamicDataCollectionAPI(initial_users=5, interval=2, dynamic_users=True)
    api_dynamic.generate_real_time_data()
