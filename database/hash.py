from passlib.context import CryptContext


class Hash:
    """Create and validate Hash methods for password"""
    def __init__(self, schemes: list[str] = "bcrypt"):
        self.pass_context = CryptContext(schemes=schemes, deprecated=['auto'])

    def bcrypt_pass(self, password: str) -> str:
        """Create has version of a plain password"""
        return self.pass_context.hash(password)

    def verify_pass(self, hashed_password: str, plain_password: str) -> bool:
        """Verify plain password with hashed"""
        return self.pass_context.verify(plain_password, hashed_password)
