import pydantic
import string
import re


class UserPydantic(pydantic.BaseModel):
    email: str
    password: str
    last_name: str
    first_name: str

    @pydantic.validator("first_name")
    @classmethod
    def first_name_valid(cls, value):
        if len(value) == 0:
            raise ValueError("First Name should be Entered")
        if any(x in value for x in string.punctuation):
            raise ValueError("First Name must not include punctuation")
        s = "[@_!#$%^&*()<>?}{~:]"
        for x in range(len(value)):
            if value[x] in s:
                raise ValueError("First Name must not include Special Character")
        else:
            return value

    @pydantic.validator("last_name")
    @classmethod
    def last_name_valid(cls, value):
        if len(value) == 0:
            raise ValueError("Last Name should be Entered")
        if any(x in value for x in string.punctuation):
            raise ValueError("Last Name must not include punctuation")
        s = "[@_!#$%^&*()<>?}{~:]"
        for x in range(len(value)):
            if value[x] in s:
                raise ValueError("Last Name must not include Special Character")
        else:
            return value

    @pydantic.validator("password")
    @classmethod
    def password_valid(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be of 8 characters long")

        if any(d in value for d in string.digits):
            if any(p in value for p in string.punctuation):
                if any(l in value for l in string.ascii_lowercase):
                    if any(u in value for u in string.ascii_uppercase):
                        s = "[@_!#$%^&*()<>?}{~:]"
                        for x in range(len(value)):
                            if value[x] in s:
                                return value
        else:
            raise ValueError(
                "Password must contain at least one punctuation symbol, digit, uppercase letter, lowercase letter, "
                "special character")

    @pydantic.validator("email")
    @classmethod
    def email_valid(cls, value):
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pat, value):
            return value
        else:
            raise ValueError("Invalid Email ID")
