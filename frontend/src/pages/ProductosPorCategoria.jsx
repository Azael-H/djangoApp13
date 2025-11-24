import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useCategoria, useProductosPorCategoria } from '../hooks/useCategorias';
import ProductCard from '../components/ProductCard';

const ProductosPorCategoria = () => {
  const { id } = useParams();
  const { data: categoria, isLoading: loadingCategoria } = useCategoria(id);
  const { data: productos, isLoading: loadingProductos } = useProductosPorCategoria(id);

  if (loadingCategoria || loadingProductos) {
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
          <nav aria-label="breadcrumb">
            <ol className="breadcrumb">
              <li className="breadcrumb-item">
                <Link to="/">Inicio</Link>
              </li>
              <li className="breadcrumb-item">
                <Link to="/categorias">Categorías</Link>
              </li>
              <li className="breadcrumb-item active">{categoria?.nombre}</li>
            </ol>
          </nav>

          <h1 className="mb-3">
            <i className="fas fa-bookmark"></i> {categoria?.nombre}
          </h1>
          <p className="text-muted">{categoria?.descripcion}</p>
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
              disponibles en esta categoría.
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductosPorCategoria;