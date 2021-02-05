import typesystem


class AddPointValidator(typesystem.Schema):
    username = typesystem.String(max_length=10)
