-- Reglas críticas de trazabilidad y coherencia

CREATE TRIGGER IF NOT EXISTS trg_order_lines_served_not_over_ordered
BEFORE UPDATE OF served_quantity ON order_lines
FOR EACH ROW
WHEN NEW.served_quantity > NEW.quantity
BEGIN
  SELECT RAISE(ABORT, 'served_quantity no puede superar quantity');
END;

CREATE TRIGGER IF NOT EXISTS trg_order_lines_invoiced_not_over_served
BEFORE UPDATE OF invoiced_quantity ON order_lines
FOR EACH ROW
WHEN NEW.invoiced_quantity > NEW.served_quantity
BEGIN
  SELECT RAISE(ABORT, 'invoiced_quantity no puede superar served_quantity');
END;

CREATE TRIGGER IF NOT EXISTS trg_payment_alloc_not_over_payment
BEFORE INSERT ON payment_allocations
FOR EACH ROW
WHEN (
  COALESCE((SELECT SUM(allocated_amount) FROM payment_allocations WHERE payment_id = NEW.payment_id), 0)
  + NEW.allocated_amount
) > (SELECT amount FROM payments WHERE id = NEW.payment_id)
BEGIN
  SELECT RAISE(ABORT, 'asignacion supera el total del cobro');
END;
