-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-12-2024 a las 23:12:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `agenda`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contacts`
--

CREATE TABLE `contacts` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `address` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `contacts`
--

INSERT INTO `contacts` (`id`, `user_id`, `first_name`, `last_name`, `phone`, `address`) VALUES
(2, 9, 'fede', 'frias', '15484956', 'falsa 123'),
(3, 10, 'gonza', 'ledo', '4156154', 'dadwEGFE'),
(4, 11, 'lucaS', 'FORNI', '89445', 'GG'),
(6, 11, 'rey', 'rey', '1414141414', 'rey');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('user','admin','supervisor') NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `role`, `full_name`, `phone`, `address`, `birthdate`, `username`) VALUES
(1, 'gonzaledo@correo.com', 'scrypt:32768:8:1$VXL9t5pidFTmcmqP$c5d2566caddfc1342164462831b1387787450f1f762c941329686010732970665c40561ce2ed221613b961d29fbb85c6d5719553bcd9f7e78dcc045af3fe30d4', 'user', 'gonzalo', '1164640245', NULL, NULL, NULL),
(3, 'chambi@gmail.com', '$2b$12$AITQuWghAxE/WzvhGyINd.pZ9pscBK36tEfCJQGdfvRkUPJaUDj/q', 'user', NULL, NULL, NULL, NULL, NULL),
(7, 'admin@admin.com', '$2b$12$et8f0nsOYFlGoePyGkKY3OOWhFCLXPehgBaGB3MzoVjLB3E5fSsfG', 'admin', NULL, NULL, NULL, NULL, NULL),
(8, 'lider@correo.com', '$2b$12$XvNOUIQmZ8sH5uLBNEXe8eehpP17yP31zEAqC8kpangqsw/v93WJq', 'user', 'lucas', '4545454545', 'fff', '2024-11-13', NULL),
(9, 'leonel@gmail.com', '$2b$12$N8QDfvYUtMdcKcTJYsngwOQP.9GHjmxW1F3kITrpAWRZ0ZcNanbRe', 'user', NULL, NULL, NULL, NULL, NULL),
(10, 'federico@gmail.com', '$2b$12$0mFuYtYzy7A2lM4/C7tmuOIp/kH67cteOT5BR8OJvlNJ8YpqnBIbK', 'user', NULL, NULL, NULL, NULL, 'None'),
(11, 'prueba@correo.com', '$2b$12$MRWSzTkmCRPZaE9icn5WNOqDFElqty1Cad32R2TbZeqJgME6kBXJm', 'user', 'prueba prueba', '1111111111', 'pruebaaa', '2024-11-15', 'prueba'),
(12, 'prueba3@correo.com', '$2b$12$/c2Pw7HZbLyy6lfkNh0R8.o0ADfZ.X2/Zh3ikvj/P9t0VYeEuk1ZK', 'user', 'prueba prueba', '4545454545', 'pruebaaaaa', '2024-11-20', 'prueba3'),
(14, 'supervisor@supervisor.com', '$2b$12$qBPanChA6n3NkJV83gTqaOCXJY9WS0ieTcr/K13W/llAeYkJCTKnW', 'supervisor', 'supervisor', '1111111111', 'supervisor', '2024-12-01', 'supervisor'),
(15, 'luna@correo.com', '$2b$12$5mo0Dtp6dHCKdqHxtz0XsuQPNr80BeeBfa9Nn79MSRrILQr5rzSoa', 'user', 'luna', '1111111111', 'luna', '2024-11-19', 'luna'),
(16, 'test@example.com', '$2b$12$S8tIa0ZETW6M7B0Ye94Sp.Vjc2RSPWrewq.3usXmgJDfvoA3KVmSO', 'user', 'Test User', '1234567890', '123 Main St', '1990-01-01', 'testuser'),
(58, 'test@domain.com', '$2b$12$vrH81N79NHVqOoedUjMaCuxKZhGJNjN7J3JyV/fIzC4Z1ljCW36re', 'user', NULL, '1234567890', NULL, '2000-01-01', 'testuser');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contacts_ibfk_1` (`user_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `contacts`
--
ALTER TABLE `contacts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `contacts`
--
ALTER TABLE `contacts`
  ADD CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
