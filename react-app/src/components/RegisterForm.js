import React, { useState } from 'react';
import './RegisterForm.css'; // Importar los estilos

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    nombres: '',
    apellidos: '',
    fecha_nacimiento: '',
    password: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Enviar los datos al backend Flask
    try {
      const response = await fetch('http://ec2-54-237-99-1.compute-1.amazonaws.com:5000/add-user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert('Registro exitoso');
        setFormData({ nombres: '', apellidos: '', fecha_nacimiento: '', password: '' });
      } else {
        alert('Error al registrar');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Registrar Nuevo Usuario</h2>
      <input type="text" name="nombres" value={formData.nombres} onChange={handleChange} placeholder="Nombres" required />
      <input type="text" name="apellidos" value={formData.apellidos} onChange={handleChange} placeholder="Apellidos" required />
      <input type="date" name="fecha_nacimiento" value={formData.fecha_nacimiento} onChange={handleChange} required />
      <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Password" required />
      <button type="submit">Registrar</button>
    </form>
  );
};

export default RegisterForm;