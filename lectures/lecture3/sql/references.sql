CREATE TABLE transport (
  id SERIAL PRIMARY KEY,
  name varchar(40) NOT NULL,
  price numeric
);

INSERT INTO transport
  (name, price)
VALUES
  ('Phương Trang', 200),
  ('Hoàng Phi', 100),
  ('Hùng Cường', 250);
