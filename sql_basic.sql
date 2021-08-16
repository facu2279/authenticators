/*
 * Made by Facundo Diaz - August 2021
 */
CREATE DATABASE testing;
USE testing;

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `usuario` varchar(25) NOT NULL,
  `password` varchar(103) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO `usuarios` (`id`, `usuario`, `password`) VALUES
(1, 'fadiaz@hola.com', 'qjwehhaxxa'),
(2, 'caraque@hola.com', 'eiy123');


CREATE TABLE `usuarios_qr` (
  `id` int(11) NOT NULL,
  `usuario` varchar(25) NOT NULL,
  `secret_key` varchar(50) NOT NULL,
  `qr` varchar(100) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO `usuarios_qr` (`id`, `usuario`, `secret_key`, `qr`, `fecha`) VALUES
(29, 'fadiaz', 'SLJPDIXWL3VBFPTTGWECMV5JAUELNF3O', 'otpauth://totp/App_Testing:fadiaz?secret=SLJPDIXWL3VBFPTTGWECMV5JAUELNF3O&issuer=App_Testing', '2021-08-13'),
(30, 'caraque', 'I5XOQ4IAVM2EWAJYBJHDGL2PW3CIF2WS', 'otpauth://totp/App_Testing:caraque?secret=I5XOQ4IAVM2EWAJYBJHDGL2PW3CIF2WS&issuer=App_Testing', '2021-08-13');

ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `usuarios_qr`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

ALTER TABLE `usuarios_qr`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
COMMIT;
