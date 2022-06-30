-- decreases the quantity of an item after adding a new order.

CREATE TRIGGER decrease_item_quanitity
AFTER INSERT ON orders
FOR EACH ROW
    UPDATE items 
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name ;
