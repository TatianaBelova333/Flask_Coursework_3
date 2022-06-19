from marshmallow import fields, Schema, validate


class UserSchema(Schema):
    """
    Validates email and password;
    Password must contain at least:
     - 6 characters;
     - one capital letter;
     - one small letter;
     - one digit;
     - one special symbol;
    """
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, error_messages={"invalid": 'Invalid email address.'})
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Regexp(
                    regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{6,}$",
                    error='Password must contain AT LEAST 6 characters/one capital letter/one small '
                          'letter/one digit/one symbol.'
                )
    )
    name = fields.Str()
    surname = fields.Str()
    favourite_genre = fields.Int()