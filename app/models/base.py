from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):    #creates the parent class for ALL database models, All models inherit from this base.
    pass


