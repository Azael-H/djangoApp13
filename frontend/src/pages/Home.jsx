import React, { useState } from 'react';
import { useProductos } from '../hooks/useProductos';
import { useCategorias } from '../hooks/useCategorias';
import ProductCard from '../components/ProductCard';

const Home = () => {
  const [filtros, setFiltros] = useState({});
  const [busqueda, setBusqueda] = useState('');

  const { data: productos, isLoading: loadingProductos } = useProductos(filtros);
  const { data: categorias, isLoading: loadingCategorias } = useCategorias();

  const handleFiltroCategoria = (categoriaId) => {
    if (categoriaId) {
      setFiltros({ categoria: categoriaId });
    } else {
      setFiltros({});
    }
  };

  const handleBuscar = (e) => {
    e.preventDefault();
    if (busqueda.trim()) {
      setFiltros({ busqueda });
    } else {
      setFiltros({});
    }
  };

  if (loadingProductos || loadingCategorias) {
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
            <i className="fas fa-book"></i> Bienvenido a Nuestra Librería
          </h1>
          <p className="text-center text-muted">
            Descubre nuestra amplia colección de libros, mangas y más
          </p>
        </div>
      </div>

      <div className="row mb-4">
        <div className="col-12">
          <form onSubmit={handleBuscar} className="search-form mx-auto">
            <div className="input-group">
              <input
                type="text"
                className="form-control"
                placeholder="Buscar por título, autor..."
                value={busqueda}
                onChange={(e) => setBusqueda(e.target.value)}
              />
              <button className="btn btn-primary" type="submit">
                <i className="fas fa-search"></i> Buscar
              </button>
            </div>
          </form>
        </div>
      </div>

      <div className="row mb-4">
        <div className="col-12">
          <div className="d-flex flex-wrap gap-2 justify-content-center">
            <button
              className={`btn ${!filtros.categoria ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => handleFiltroCategoria(null)}
            >
              Todas las Categorías
            </button>
            {categorias?.map((categoria) => (
              <button
                key={categoria.id}
                className={`btn ${
                  filtros.categoria === categoria.id
                    ? 'btn-primary'
                    : 'btn-outline-primary'
                }`}
                onClick={() => handleFiltroCategoria(categoria.id)}
              >
                {categoria.nombre}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="row">
        {productos?.length > 0 ? (
          productos.map((producto) => (
            <ProductCard key={producto.id} producto={producto} />
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center">
              <i className="fas fa-exclamation-circle"></i> No hay productos
              disponibles
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;