from app.models import FlipCard


def test_create_card_valid_input(client):
    """Testing - Creation of a card with valid input - should pass."""
    card_data = {
        "front_text": "OOP Concept?",
        "back_text": "Encapsulation",
        "category": "OOP",
    }

    response = client.post("/api/cards/", json=card_data)

    assert response.status_code == 200
    data = response.json()
    assert data["front_text"] == card_data["front_text"]
    assert data["back_text"] == card_data["back_text"]
    assert data["category"] == card_data["category"]


def test_create_card_invalid_category(client):
    """Testing - Creation of a card with invalid category - should fail."""
    card_data = {
        "front_text": "OOP Concept?",
        "back_text": "Encapsulation",
        "category": "INVALIDCAT",
    }

    response = client.post("/api/cards/", json=card_data)

    assert response.status_code == 400
    assert "not a valid category" in response.json()["detail"]


def test_create_card_invalid_duplicate(client):
    """Testing - Duplicate card creation - should fail."""
    card_data = {
        "front_text": "OOP Concept?",
        "back_text": "Encapsulation",
        "category": "OOP",
    }

    response1 = client.post("/api/cards/", json=card_data)
    assert response1.status_code == 200

    response2 = client.post("/api/cards/", json=card_data)
    assert response2.status_code == 400
    assert "card already exists" in response2.json()["detail"]


def test_get_all_cards(client, db_session):
    """Testing - Get all cards - should pass."""
    card1 = FlipCard(
        front_text="What is CI/CD?", back_text="Automation process", category="CI_CD"
    )
    card2 = FlipCard(
        front_text="What is Docker?",
        back_text="Containerization tool",
        category="DOCKER",
    )

    db_session.add_all([card1, card2])
    db_session.commit()

    response = client.get("/api/cards/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["front_text"] == "What is CI/CD?"
    assert data[1]["front_text"] == "What is Docker?"


def test_get_all_cards_empty(client):
    """Testing - Get all cards - should return [] when empty."""

    response = client.get("/api/cards/")

    assert response.status_code == 200
    assert response.json() == []


def test_delete_card(client, db_session):
    """Test - Delete card - should delete the card successfully ."""
    card = FlipCard(
        front_text="OOP Concept?", back_text="Encapsulation", category="OOP"
    )
    db_session.add(card)
    db_session.commit()

    response = client.delete(f"/api/cards/{card.id}")

    assert response.status_code == 200

    deleted_card = db_session.query(FlipCard).filter_by(id=card.id).first()
    assert deleted_card is None


def test_delete_card_invalid_id(client):
    """Test - Delete card with invalid ID - should return 404 Not Found."""

    fake_card_id = 999999

    response = client.delete(f"/api/cards/{fake_card_id}")

    assert response.status_code == 404
    assert f"Card with ID {fake_card_id} not found!" in response.json()["detail"]
