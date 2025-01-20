from pydantic import BaseModel


class UserBase(BaseModel):
    useremail: str
    first_name: str
    last_name: str = ""
    user_type: str = "user"


class User(UserBase):
    password: str
    who_added: str = ""


class UserLogin(BaseModel):
    useremail: str
    password: str


class UpdateRole(BaseModel):
    username: str
    new_role: str


class LDAPConfig(BaseModel):
    ldap_url: str
    admin_dn: str
    ldap_password: str
