from pydantic import BaseModel


def generate_line_items(ticket_data: BaseModel, price_ids: dict) -> list:
    line_items = []
    for field_name, quantity in ticket_data.model_dump().items():
        if quantity > 0:
            price_id = price_ids.get(field_name)
            if not price_id:
                raise ValueError(f"Missing price ID for ticket type: {field_name}")
            line_items.append(
                {
                    "price": price_id,
                    "quantity": quantity,
                }
            )
    return line_items
