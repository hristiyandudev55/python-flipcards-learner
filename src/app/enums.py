from enum import Enum

# TODO - add kubernetes category.


class Categories(str, Enum):
    OOP = "OOP"
    DSA = "DSA"
    WEB = "WEB"
    DOCKER = "DOCKER"
    KUBERNETES = "KUBERNETES"
    LINUX = "LINUX"
    AZURE = "AZURE"
    CI_CD = "CI_CD"
    GENERAL = "GENERAL"


class LogAction(Enum):
    CARD_CREATED = "card_created"
    CARD_UPDATED = "card_updated"
    CARD_DELETED = "card_deleted"
    CARD_READ = "card_read"
    ERROR = "error"
