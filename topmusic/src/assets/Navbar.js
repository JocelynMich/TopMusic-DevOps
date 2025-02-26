// Navbar.js
import React from 'react';
import '../styles/Navbar.css'

const Navbar = () => {
  return (
  <header className='header'>
    <a href="/" className='logo'>Logo</a>
    <nav className='navbar'>
      <a href='/'>Inicio</a>
      <a href='/'>Top 15 Canciones Semanales</a>
      <a href='/'>Spotify</a>
      <a href='/'>Sobre Nosotros</a>
      <a href='/'>Contacto</a>
    </nav>
  </header>
  );
};

export default Navbar;
