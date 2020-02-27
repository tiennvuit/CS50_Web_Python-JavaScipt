CREATE TABLE khoa (
  MaKhoa serial NOT NULL,
  TenKhoa varchar(40) NOT NULL,
  NgayThanhLap integer
);


CREATE TABLE giangvien (
  MaGV serial NOT NULL,
  TenGV varchar(40) NOT NULL,
  NamVaoTruong integer,
  Luong numeric,
  MaKhoa integer
);
