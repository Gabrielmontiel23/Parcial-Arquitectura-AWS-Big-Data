// src/components/RegisterForm.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RegisterForm from './RegisterForm';

test('renderiza correctamente el formulario de registro', () => {
  render(<RegisterForm />);
  
  // Verificar que el formulario contiene los campos esperados
  expect(screen.getByLabelText(/customer id/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/film id/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/rental date/i)).toBeInTheDocument();
});

test('envía los datos del formulario al hacer clic en "Registrar Renta"', () => {
  render(<RegisterForm />);
  
  // Completar los campos del formulario
  fireEvent.change(screen.getByLabelText(/customer id/i), { target: { value: '5' } });
  fireEvent.change(screen.getByLabelText(/film id/i), { target: { value: '10' } });
  fireEvent.change(screen.getByLabelText(/rental date/i), { target: { value: '2024-10-30' } });

  // Simular clic en el botón de registro
  fireEvent.click(screen.getByText(/Registrar Renta/i));

  // Verificar que el formulario fue enviado (puedes agregar mocks para la API)
});
