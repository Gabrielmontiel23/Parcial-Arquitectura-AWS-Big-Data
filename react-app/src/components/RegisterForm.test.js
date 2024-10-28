import { act } from 'react'; // Importar 'act' desde 'react'
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RegisterForm from './RegisterForm';

test('renderiza el componente RegisterForm', () => {
  render(<RegisterForm />);

  // Verifica que se muestra el botón de enviar
  const submitButton = screen.getByRole('button', { name: /registrar renta/i });
  expect(submitButton).toBeInTheDocument();

  // Simula el envío del formulario
  fireEvent.click(submitButton);
});
