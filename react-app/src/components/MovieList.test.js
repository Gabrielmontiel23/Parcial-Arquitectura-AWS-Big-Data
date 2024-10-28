import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import MovieList from './MovieList';

// Mock de fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({
      status: 'success',
      data: [{ title: 'Inception', customerId: 5 }]
    })
  })
);

test('renderiza correctamente el componente', () => {
  render(<MovieList />);

  // Verificar que se renderiza el encabezado
  expect(screen.getByText(/Películas Rentadas/i)).toBeInTheDocument();
});

test('muestra la lista de películas después de una búsqueda exitosa', async () => {
  render(<MovieList />);

  // Completar el campo de búsqueda e iniciar la búsqueda
  fireEvent.change(screen.getByPlaceholderText(/Ingresa el ID del cliente/i), { target: { value: '5' } });
  fireEvent.click(screen.getByText(/Buscar/i));

  // Verificar que se muestra la película obtenida del mock
  const movieItem = await screen.findByText(/Inception/i);
  expect(movieItem).toBeInTheDocument();
});
