// src/components/MovieList.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import MovieList from './MovieList';

// Mocks de fetch para simular respuestas de API
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ status: 'success', data: [{ title: 'Inception', film_id: 1, rental_date: '2024-10-30' }] })
  })
);

describe('MovieList Component', () => {
  beforeEach(() => {
    fetch.mockClear(); // Limpiar los mocks antes de cada prueba
  });

  test('renderiza correctamente el componente', () => {
    render(<MovieList />);
    
    // Verificar que los elementos básicos se renderizan
    expect(screen.getByText(/Películas Rentadas/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Ingresa el ID del cliente/i)).toBeInTheDocument();
    expect(screen.getByText(/Buscar/i)).toBeInTheDocument();
  });

  test('muestra un error cuando no se ingresa un ID', () => {
    render(<MovieList />);
    
    fireEvent.click(screen.getByText(/Buscar/i));

    // Verificar que se muestra el mensaje de error
    expect(screen.getByText(/Por favor ingresa un ID./i)).toBeInTheDocument();
  });

  test('muestra la lista de películas después de una búsqueda exitosa', async () => {
    render(<MovieList />);
    
    fireEvent.change(screen.getByPlaceholderText(/Ingresa el ID del cliente/i), { target: { value: '5' } });
    fireEvent.click(screen.getByText(/Buscar/i));

    // Verificar que se muestra la película obtenida del mock
    const movieItem = await screen.findByText(/Inception/i);
    expect(movieItem).toBeInTheDocument();
  });
});
