import React from 'react';
import { Link } from 'react-router-dom';
import { useCategorias, usePrefetchCategoria } from '../hooks/useCategorias';

const Categorias = () => {
  const { data: categorias, isLoading } = useCategorias();
  const prefetchCategoria = usePrefetchCategoria();

  if (isLoading) {
    return (
      <div className="container mt-5 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container my-4">
      <div className="row mb-4">
        <div className="col-12">
          <h1 className="text-center mb-4">
            <i className="fas fa-list"></i> Todas las Categorías
          </h1>
          <p className="text-center text-muted">
            Explora nuestra selección organizada por categorías
          </p>
        </div>
      </div>

      <div className="row">
        {categorias?.map((categoria) => (
          <div key={categoria.id} className="col-md-6 col-lg-4 mb-4">
            <Link
              to={`/categoria/${categoria.id}`}
              className="text-decoration-none"
              onMouseEnter={() => prefetchCategoria(categoria.id)}
            >
              <div className="card h-100 categoria-card">
                {categoria.imagen ? (
                  <img
                    src={categoria.imagen}
                    className="card-img-top"
                    alt={categoria.nombre}
                    style={{ height: '200px', objectFit: 'cover' }}
                  />
                ) : (
                  <div
                    className="card-img-top bg-gradient d-flex align-items-center justify-content-center"
                    style={{ height: '200px' }}
                  >
                    <i className="fas fa-bookmark fa-4x text-white"></i>
                  </div>
                )}
                <div className="card-body text-center">
                  <h3 className="card-title">{categoria.nombre}</h3>
                  <p className="card-text text-muted">{categoria.descripcion}</p>
                  <span className="badge bg-primary">
                    {categoria.total_productos} productos
                  </span>
                </div>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Categorias;