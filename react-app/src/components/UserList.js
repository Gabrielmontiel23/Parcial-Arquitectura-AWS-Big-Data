import React, { useEffect, useState } from 'react';

const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('http://18.210.27.250:5000/get-users');
        const data = await response.json();
        setUsers(data.data);  // Asegúrate de que 'data.data' contiene la lista de usuarios
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