import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useProducto, useProductos } from '../hooks/useProductos';
import { useCarrito } from '../hooks/useCarrito';
import ProductCard from '../components/ProductCard';

const DetalleProducto = () => {
  const { id } = useParams();
  const { data: producto, isLoading } = useProducto(id);
  const { data: relacionados } = useProductos({
    categoria: producto?.categoria,
  });
  const { addItem, isAddingItem } = useCarrito();

  const handleAddToCart = () => {
    addItem({ producto_id: producto.id, cantidad: 1 });
  };

  if (isLoading) {
    return (
      <div className="container mt-5 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  const productosRelacionados = relacionados?.filter(p => p.id !== producto?.id).slice(0, 4);

  return (
    <div className="container my-4">
      <nav aria-label="breadcrumb">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to="/">Inicio</Link>
          </li>
          <li className="breadcrumb-item">
            <Link to={`/categoria/${producto?.categoria}`}>
              {producto?.categoria_nombre}
            </Link>
          </li>
          <li className="breadcrumb-item active">{producto?.nombre}</li>
        </ol>
      </nav>

      <div className="row">
        <div className="col-md-5">
          <img
            src={producto?.imagen || `https://via.placeholder.com/500x700?text=${encodeURIComponent(producto?.nombre || 'Producto')}`}
            className="img-fluid rounded shadow"
            alt={producto?.nombre}
          />
          <div className="mt-3">
            {producto?.nuevo && (
              <span className="badge bg-success me-2">Nuevo</span>
            )}

            {producto?.destacado && (
              <span className="badge bg-warning me-2">
                <i className="fas fa-star"></i> Destacado
              </span>
            )}

            {producto?.tiene_descuento && (
              <span className="badge bg-danger">
                Oferta -{producto?.porcentaje_descuento}%
              </span>
            )}
          </div>
        </div>

        <div className="col-md-7">
          <span className="badge bg-info mb-2">{producto?.categoria_nombre}</span>
          <h1 className="mb-3">{producto?.nombre}</h1>

          {producto?.autor && (
            <p className="lead">
              <i className="fas fa-user"></i> <strong>Autor:</strong> {producto?.autor}
            </p>
          )}

          {producto?.editorial && (
            <p>
              <i className="fas fa-building"></i> <strong>Editorial:</strong>{' '}
              {producto?.editorial}
            </p>
          )}

          {producto?.isbn && (
            <p>
              <i className="fas fa-barcode"></i> <strong>ISBN:</strong>{' '}
              {producto?.isbn}
            </p>
          )}

          <hr />

          <h3 className="mb-3">Descripción</h3>
          <p className="text-justify">{producto?.descripcion}</p>

          <hr />

          <div className="row align-items-center mb-3">
            <div className="col-md-6">
              {producto?.tiene_descuento ? (
                <>
                  <p className="mb-1">
                    <span
                      className="text-decoration-line-through text-muted"
                      style={{ fontSize: '1.2rem' }}
                    >
                      S/. {producto?.precio}
                    </span>
                  </p>
                  <p className="precio mb-0">S/. {producto?.precio_final}</p>
                  <p className="text-success">
                    <small>
                      ¡Ahorras S/. {(producto?.precio - producto?.precio_final).toFixed(2)}!
                    </small>
                  </p>
                </>
              ) : (
                <p className="precio mb-0">S/. {producto?.precio}</p>
              )}
            </div>
            <div className="col-md-6">
              <p className="mb-0">
                <i className="fas fa-box"></i> <strong>Stock:</strong>{' '}
                {producto?.stock > 10 ? (
                  <span className="text-success">{producto?.stock} disponibles</span>
                ) : producto?.stock > 0 ? (
                  <span className="text-warning">
                    ¡Últimas {producto?.stock} unidades!
                  </span>
                ) : (
                  <span className="text-danger">Agotado</span>
                )}
              </p>
            </div>
          </div>

          <hr />

          <div className="d-grid gap-2">
            {producto?.stock > 0 ? (
              <button
                className="btn btn-primary btn-lg"
                onClick={handleAddToCart}
                disabled={isAddingItem}
              >
                <i className="fas fa-cart-plus"></i>{' '}
                {isAddingItem ? 'Agregando...' : 'Agregar al Carrito'}
              </button>
            ) : (
              <button className="btn btn-secondary btn-lg" disabled>
                <i className="fas fa-ban"></i> No Disponible
              </button>
            )}
            <Link to="/" className="btn btn-outline-secondary">
              <i className="fas fa-arrow-left"></i> Volver a la Tienda
            </Link>
          </div>
        </div>
      </div>

      {productosRelacionados?.length > 0 && (
        <div className="row mt-5">
          <div className="col-12">
            <h3 className="mb-4">
              <i className="fas fa-book-open"></i> Productos Relacionados
            </h3>
          </div>
          {productosRelacionados.map((prod) => (
            <ProductCard key={prod.id} producto={prod} />
          ))}
        </div>
      )}
    </div>
  );
};

export default DetalleProducto;