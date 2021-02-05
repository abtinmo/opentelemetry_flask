import typesystem


class LoginValidator(typesystem.Schema):
    username = typesystem.String(max_length=10)


class VerifyValidator(typesystem.Schema):
    username = typesystem.String(max_length=10)
    code = typesystem.String(pattern="[0-9]{4}")
