# Python FlipCards Learner

A lightweight, interactive web application for learning programming concepts using flip cards. Built with FastAPI, PostgreSQL, and Vue.js.

## 📖 Overview

Python FlipCards Learner is an educational tool designed to help users master programming concepts through interactive flashcards. The application features cards in multiple categories including:

- Object-Oriented Programming (OOP)
- Data Structures & Algorithms (DSA)
- Web Development (WEB)
- Docker Containerization
- CI/CD Workflows
- Azure Cloud Services
- Linux Administration

## 🚀 Features

- **Interactive Flip Cards**: Click to reveal answers
- **Categorized Learning**: Organize your learning by topics
- **Responsive Design**: Works on desktop and mobile devices
- **AWS Integration**: Assets stored in S3 for reliable delivery
- **Comprehensive Logging**: Track application usage

## ⚙️ Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database
- AWS account (for S3 storage)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/hristiyandudev55/python-flipcards-learner.git
   cd python-flipcards-learner
   ```

2. Install Poetry (Python dependency management):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Create and activate a virtual environment using Poetry:
   ```bash
   poetry shell
   ```

4. Install Python dependencies:
   ```bash
   poetry install
   ```

5. Configure environment variables:
   Create a .env file in the project root with the following content:
   ```
   PYTHONPATH=src
   
   # Database configuration
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   DB_NAME=flipnlearn
   DATABASE_URL=postgresql://user:password@host:5432/flipnlearn
   TEST_DB_URL=postgresql://test_user:password@localhost:5432/test_db
   
   # AWS configuration
   AWS_BUCKET_NAME=your-bucket-name
   AWS_REGION=your-aws-region
   AWS_ACCESS_KEY=your-access-key
   AWS_SECRET_KEY=your-secret-key
   
   # Frontend configuration
   VITE_S3_BASE_URL=https://your-bucket-name.s3.your-region.amazonaws.com
   ```

6. Install frontend dependencies:
   ```bash
   cd frontend/flip-cards-learner
   npm install
   cd ../..
   ```

## 🏃 Running the Application

### Local Development

1. Start the application using the provided script:
   ```bash
   ./run.sh
   ```

2. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

### Production Deployment

For production deployment on AWS Lightsail:

1. Configure the systemd service:
   ```bash
   sudo nano /etc/systemd/system/flipcards.service
   ```

2. Add this configuration:
   ```ini
   [Unit]
   Description=Flip Cards Learner App
   After=network.target

   [Service]
   User=ec2-user
   WorkingDirectory=/home/ec2-user/python-flipcards-learner
   ExecStart=/home/ec2-user/python-flipcards-learner/service-wrapper.sh
   ExecStop=/home/ec2-user/python-flipcards-learner/stop.sh
   Type=simple
   Restart=on-failure
   RestartSec=5
   KillMode=mixed
   KillSignal=SIGTERM
   TimeoutStopSec=20

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable flipcards.service
   sudo systemctl start flipcards.service
   ```

## 📱 Using the Application

1. **Open the app** in your web browser at http://localhost:5173 (or your deployment URL)
2. **Choose a category** from the main screen to start learning
3. **View the question** on the front of the card
4. **Click on the card** to flip it and reveal the answer
5. **Navigate** through cards using the Previous and Next buttons
6. **Return to categories** by clicking the Back button

## 🛠️ Project Structure

```
python-flipcards-learner/
├── src/                      # Backend source code
│   └── app/
│       ├── routes/           # API endpoints
│       ├── utils/            # Utility functions and services
│       ├── models.py         # Database models
│       ├── schemas.py        # Pydantic schemas
│       ├── crud.py           # Database operations
│       ├── main.py           # FastAPI application entry point
│       └── config.py         # Configuration management
├── frontend/                 # Frontend source code
│   └── flip-cards-learner/
│       ├── src/
│       │   ├── components/   # Vue components
│       │   ├── views/        # Vue views/pages
│       │   ├── router/       # Vue Router configuration
│       │   └── assets/       # Static assets
│       └── public/           # Public assets
├── .github/                  # GitHub Actions workflows
├── .env.template             # Environment variables template
├── run.sh                    # Script to run the application
├── stop.sh                   # Script to stop the application
└── service-wrapper.sh        # Script for systemd service
```

## 🧪 Testing

### Running Backend Tests

```bash
poetry run pytest
```

### Running Frontend Tests

```bash
cd frontend/flip-cards-learner
npm run test:unit
```

### Load Testing

```bash
poetry run locust -f load_test.py
```

## 🔒 Security Considerations

- Keep your .env file secure and never commit it to version control
- Implement HTTPS for production deployments
- Configure proper firewall rules for your AWS instances
- Regularly rotate AWS credentials

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Hristiyan Dudev - [GitHub Profile](https://github.com/hristiyandudev55)

---

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/hristiyandudev55/python-flipcards-learner/issues).