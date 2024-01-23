-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-08-2023 a las 17:00:31
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `mi_coleccion`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `game`
--

CREATE TABLE `game` (
  `id_product` int(11) NOT NULL,
  `platform` varchar(255) DEFAULT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `buyer_platform` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `game`
--

INSERT INTO `game` (`id_product`, `platform`, `genre`, `region`, `publisher`, `status`, `buyer_platform`, `image`) VALUES
(26, 'Dreamcast', 'Plataformas', 'PAL', 'EA', 'Usado', 'Wallapop', ''),
(27, 'Dreamcast', 'Plataformas', 'PAL', 'EA', 'Usado', 'Wallapop', '0fe79c8c-c22c-4145-82a4-4677bc589dc4-IMG-3203.jpg'),
(28, 'Megadrive', 'Plataformas', 'PAL', '', 'Usado', 'Ebay', ''),
(29, 'Super Nintendo', 'Plataformas', 'NTSC', '', 'Usado', 'Wallapop', ''),
(30, 'Wii U', 'Rol', 'PAL', '', 'Nuevo', 'El corte ingles', ''),
(31, 'Play Station 2', 'Hack and Slash', 'PAL', '', 'Nuevo', 'Game', '3f6fa83e-a7af-4155-8a1f-e239e62e90ac-Cochera-Plano_Interior.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `product`
--

CREATE TABLE `product` (
  `id_product` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `buy_date` date DEFAULT NULL,
  `price` decimal(7,2) DEFAULT NULL,
  `id_user_fk` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `product`
--

INSERT INTO `product` (`id_product`, `name`, `description`, `buy_date`, `price`, `id_user_fk`) VALUES
(26, 'Super Mario 64', 'Super Mario 64', '2023-05-20', 80.00, 21),
(27, 'Alidin', 'Aladin', '2023-05-24', 15.95, 21),
(28, 'Sonic', 'Sonic 1', '2023-06-01', 20.00, 17),
(29, 'Super Mario World', 'Super mario World para SNES', '2023-06-15', 150.00, 17),
(30, 'Paper Mario color splash', 'Paper mario color splash para Wii U', '2023-06-16', 85.00, 17),
(31, 'Nier', 'Nier 3', '2023-08-03', 20.00, 17);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `second_last_name` varchar(64) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `last_name`, `second_last_name`, `email`, `password`, `is_active`, `is_admin`) VALUES
(16, 'juan', 'alvarez', '', 'juan@test.com', 'pbkdf2:sha256:260000$QytSX8th3pKMOL0R$d4532e17f6e8d60b34c3713981f7e9a3b3924b3f3b202829169996f3d833a9b0', 1, 0),
(17, 'Raul', 'Garcia', '', 'raul.garcia@test.com', 'pbkdf2:sha256:260000$wU2jlug821ZvpT6r$af74f48af4ae15e79501d243e7df94d93574f8783bf7c4d2637b6bddb0a9104f', 1, 0),
(18, 'Maria', 'Aguilera', '', 'maria@test.com', 'pbkdf2:sha256:260000$OqdUTUmVHK75LhtG$da194c4591e521999c7771b445559c5eef7e29350c89c7ff89e70bb87bf888ee', 1, 0),
(19, 'Manuel', 'Perez', 'lopez', 'manuel.perez@test.com', 'pbkdf2:sha256:260000$C0PbJaOX4MArf2KU$8926db5dda2bf17522b86dfbb21ce427f3c3df760e256a939df42d6cdc1f2b28', 1, 0),
(20, 'Maria', 'Aguilera', 'Pacheco', 'mariajap19@gmail.com', 'pbkdf2:sha256:260000$FlyZbBB5fHprEcmS$e115f254f9cbaaa80af210028d3721e067058fe8f57e8a5ef098841310c3b94d', 1, 0),
(21, 'Juan ', 'Alvarez', 'Mate', 'juan_mate@test.com', 'pbkdf2:sha256:260000$FPMdXnrp2FYm1i37$98d9fc9b9fce069114bb5035cb419ea38f3102da0632a7679c35990addd14235', 1, 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `game`
--
ALTER TABLE `game`
  ADD PRIMARY KEY (`id_product`);

--
-- Indices de la tabla `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id_product`),
  ADD KEY `id_user_fk` (`id_user_fk`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `product`
--
ALTER TABLE `product`
  MODIFY `id_product` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `game`
--
ALTER TABLE `game`
  ADD CONSTRAINT `fk_product_id` FOREIGN KEY (`id_product`) REFERENCES `product` (`id_product`) ON DELETE CASCADE;

--
-- Filtros para la tabla `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_ibfk_1` FOREIGN KEY (`id_user_fk`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
