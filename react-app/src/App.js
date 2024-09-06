import React from 'react';
import RegisterForm from './components/RegisterForm';
import UserList from './components/UserList';
import NameBox from './components/NameBox';  // Importar el componente
import './App.css';  // Asegúrate de que la ruta sea correcta

function App() {
  const [showUsers, setShowUsers] = React.useState(false);

  return (
    <>
      <NameBox />  {/* Añadir la caja de nombres fuera del contenedor principal */}
      <div className="App">
        <div className="container">
          <h1>Gestión de Usuarios</h1>
          {showUsers ? <UserList /> : <RegisterForm />}
          <button onClick={() => setShowUsers(!showUsers)}>
            {showUsers ? 'Registrar Nuevo Usuario' : 'Ver Usuarios Registrados'}
          </button>
        </div>
      </div>
    </>
  );
}

export default App;