import typing as t
from collections import UserString

class RandomString(UserString, str):
    """Subclass of string with .sql property.
    This is intended to be used where an exact value
    is desired in the final output sql.
    """
    def __init__(
        self,
        string: t.Sequence,
        dialect: str = "MySQL"
    ):
        self.dialect = dialect
        super().__init__(seq=data)

    def __new__(cls, data: t.Optional[t.Sequence] = None, **kwargs):
        instance = str.__new__(cls, data)
        instance.__dict__.update(kwargs)
        return instance

    @property
    def sql(self):
        return self.data


def ensure_str(obj: t.Any) -> str:
    if not isinstance(obj, str):
        return str(obj)
    return obj

if __name__ == "__main__":
    
    ps = PlainSql("Hello there")
    
    print(ps)
    # Hello there
    
    print(f"ps is a string: {isinstance(ps, str)}")
    # ps is a string: True
    
    print(f"ps is a PlainSql: {isinstance(ps, PlainSql)}")
    # ps is a PlainSql: True
    
    print(f"ps dialect: {ps.dialect}")
    # ps dialect: MySQL

    # Check that after using operators the result is still PlainSql
    ps += PlainSql("\nGeneral Kenobi")
    
    print(ps)
    # Hello there
    # General Kenobi
    
    print(f"ps is still a PlainSQL: {isinstance(ps, PlainSql)}")
    # ps is still a PlainSQL: True

    us = ensure_str(PlainSql("this"))
    print(f"us is still a PlainSQL after ensure_str: {isinstance(us, UserString)}")

