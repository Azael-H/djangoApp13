import { useQuery, useQueryClient } from '@tanstack/react-query';
import { categoriasAPI } from '../services/api';

export const useCategorias = () => {
  return useQuery({
    queryKey: ['categorias'],
    queryFn: categoriasAPI.getAll,
    select: (response) => response.data,
  });
};

export const useCategoria = (id) => {
  return useQuery({
    queryKey: ['categoria', id],
    queryFn: () => categoriasAPI.getById(id),
    select: (response) => response.data,
    enabled: !!id,
  });
};

export const useProductosPorCategoria = (id) => {
  return useQuery({
    queryKey: ['productos', 'categoria', id],
    queryFn: () => categoriasAPI.getProductos(id),
    select: (response) => response.data,
    enabled: !!id,
  });
};

export const usePrefetchCategoria = () => {
  const queryClient = useQueryClient();

  return (id) => {
    queryClient.prefetchQuery({
      queryKey: ['productos', 'categoria', id],
      queryFn: () => categoriasAPI.getProductos(id),
    });
  };
};