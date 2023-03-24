from passlib.context import CryptContext


class Hash:
    def __init__(self, schemes: list[str] = "bcrypt"):
        self.pass_context = CryptContext(schemes=schemes, deprecated=['auto'])

    def bcrypt_pass(self, password: str) -> str:
        return self.pass_context.hash(password)

    def verify_pass(self, hashed_password: str, plain_password: str) -> bool:
        return self.pass_context.verify(plain_password, hashed_password)
