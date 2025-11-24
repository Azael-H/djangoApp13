import React from 'react';
import { Link } from 'react-router-dom';
import { useCarrito } from '../hooks/useCarrito';

const Navbar = () => {
  const { carrito } = useCarrito();

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">
          <i className="fas fa-book-reader"></i> LibreríaOnline
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                <i className="fas fa-home"></i> Inicio
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/categorias">
                <i className="fas fa-list"></i> Categorías
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/carrito">
                <i className="fas fa-shopping-cart"></i> Carrito{' '}
                <span className="badge bg-danger">
                  {carrito?.cantidad_items || 0}
                </span>
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;