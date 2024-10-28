// src/App.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('renderiza correctamente la caja de nombres y el botón para ver películas', () => {
  render(<App />);
  
  // Verificar que se renderiza el componente de la caja de nombres
  expect(screen.getByText('Gestión de Rentas')).toBeInTheDocument();

  // Verificar el botón para alternar entre ver películas y registrar rentas
  const toggleButton = screen.getByText('Ver Peliculas por Usuario');
  expect(toggleButton).toBeInTheDocument();

  // Simular un clic en el botón para alternar la vista
  fireEvent.click(toggleButton);
  expect(screen.getByText('Registrar Una Nueva Renta')).toBeInTheDocument();
});

test('renderiza el formulario de registro', () => {
  render(<App />);

  // Verificar que el formulario de registro esté en el DOM
  expect(screen.getByText('Registrar Una Nueva Renta')).toBeInTheDocument();
});
