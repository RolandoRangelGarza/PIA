create database farmacia;

use farmacia;
SELECT * FROM `almacenes`;
CREATE TABLE `almacenes` (
  `id_almacen` int NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `direccion` varchar(45) DEFAULT NULL,
  `encargado` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_almacen`));
  
CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `direccion` varchar(45) DEFAULT NULL,
  `correo` varchar(45) DEFAULT NULL,
  `telefono` char(8) DEFAULT NULL,
  `limite_credito` decimal(8,2) DEFAULT NULL,
  `saldo` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`));
  
CREATE TABLE `lineas_productos` (
  `id_linea` int NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_linea`));
  
CREATE TABLE `usuarios_sistema` (
  `clave_usuario` int NOT NULL,
  `contrasena` varchar(45) DEFAULT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `tipo` varchar(45) DEFAULT NULL,
  `correo` varchar(45) DEFAULT NULL,
  `telefono` char(8) DEFAULT NULL,
  PRIMARY KEY (`clave_usuario`));
  
CREATE TABLE `productos` (
  `clave_producto` int NOT NULL,
  `clave_linea` int DEFAULT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `Unidad_medida` varchar(45) DEFAULT NULL,
  `fecha_ult_compra` date DEFAULT NULL,
  `precio` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`clave_producto`),
  KEY `clave_linea_idx` (`clave_linea`),
  CONSTRAINT `clave_linea` FOREIGN KEY (`clave_linea`) REFERENCES `lineas_productos` (`id_linea`));
  
CREATE TABLE `tickets` (
  `id_ticket` int NOT NULL,
  `id_usuario` int DEFAULT NULL,
  `id_cliente` int DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `sucursal` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_ticket`),
  KEY `clave_usuario_idx` (`id_usuario`),
  KEY `id_cliente_idx` (`id_cliente`),
  CONSTRAINT `clave_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios_sistema` (`clave_usuario`),
  CONSTRAINT `id_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`));
  
  
CREATE TABLE `detalles_tickets` (
  `id_ticket` int DEFAULT NULL,
  `clave_producto` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  KEY `id_ticket_idx` (`id_ticket`),
  KEY `id_producto_idx` (`clave_producto`),
  CONSTRAINT `id_producto` FOREIGN KEY (`clave_producto`) REFERENCES `productos` (`clave_producto`),
  CONSTRAINT `id_ticket` FOREIGN KEY (`id_ticket`) REFERENCES `tickets` (`id_ticket`));
  
  
CREATE TABLE `almacenes_productos` (
  `id_almacen` int DEFAULT NULL,
  `id_producto` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  KEY `clave_almacen_idx` (`id_almacen`),
  KEY `clave_producto_idx` (`id_producto`),
  CONSTRAINT `clave_almacen` FOREIGN KEY (`id_almacen`) REFERENCES `almacenes` (`id_almacen`),
  CONSTRAINT `clave_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`clave_producto`));

  
  
  