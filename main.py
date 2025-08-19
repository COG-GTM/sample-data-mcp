from mcp.server.fastmcp import FastMCP
from faker import Faker
from datetime import datetime, timedelta
import random
from pydantic import BaseModel
from typing import List, Literal, Optional

class FieldSpec(BaseModel):
    name: str
    type: Literal["string", "enum", "integer", "date", "filler"]
    length: int
    values: Optional[list[str]] = None
    format: Optional[str] = "%Y%m%d"
    min: Optional[int] = 0
    max: Optional[int] = 9999

fake = Faker()
mcp = FastMCP("SampleDataMCP")

def pad(value, length):
    return str(value)[:length].ljust(length)

def generate_field(field):
    ftype = field.type
    length = field.length

    if ftype == "string":
        return pad(fake.name(), length)
    elif ftype == "enum":
        return pad(random.choice(field.values), length)
    elif ftype == "integer":
        min_val = field.min
        max_val = field.max
        return pad(str(random.randint(min_val, max_val)), length)
    elif ftype == "date":
        fmt = field.format
        random_date = datetime.today() - timedelta(days=random.randint(0, 3650))
        return pad(random_date.strftime(fmt), length)
    elif ftype == "filler":
        return " " * length
    else:
        return pad("?", length)

def generate_test_data(fields, num_records):
    lines = []
    for _ in range(num_records):
        line = "".join(generate_field(field) for field in fields)
        lines.append(line)
    return "\n".join(lines)

@mcp.tool()
def generate_test_data_tool(fields: List[FieldSpec], num_records: int) -> str:
    """Generate fixed-length test data based on a field specification"""
    return generate_test_data(fields, num_records)

if __name__ == "__main__":
    mcp.run('stdio')
