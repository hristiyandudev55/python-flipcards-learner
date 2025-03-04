from locust import HttpUser, task, between

class FlipCardsUser(HttpUser):
    host = "http://18.153.32.18:8000"  # Add base host for API calls
    wait_time = between(1, 3)
    
    # Frontend routes
    @task(1)
    def load_home_page(self):
        self.client.get("http://18.153.32.18:5173/")  # Frontend URL
        
    @task(1)
    def load_category_page(self):
        self.client.get("http://18.153.32.18:5173/category")
        
    @task(2)
    def load_specific_category(self):
        self.client.get("http://18.153.32.18:5173/category/OOP")
    
    # Backend API routes
    @task(3)
    def get_oop_cards(self):
        self.client.get("/api/cards/OOP")
    
    @task(2)
    def get_dsa_cards(self):
        self.client.get("/api/cards/DSA")
