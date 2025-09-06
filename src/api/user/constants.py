from enum import Enum


class AuthProvider(str, Enum):
    GOOGLE = "google"
    GITHUB = "github"
    FIREBASE = "firebase"
