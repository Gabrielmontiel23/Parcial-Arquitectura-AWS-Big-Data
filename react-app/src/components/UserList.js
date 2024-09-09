import React, { useEffect, useState } from 'react';
import './UserList.css'; // Importar los estilos

const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('http://18.205.11.118:5000/get-users');
        const data = await response.json();
        setUsers(data.data);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div>
      <h2>Usuarios Registrados</h2>
      <ul>
        {users.map((user, index) => (
          <li key={index}>
            {user.nombres} {user.apellidos} - Fecha de Nacimiento: {user.fecha_nacimiento}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;