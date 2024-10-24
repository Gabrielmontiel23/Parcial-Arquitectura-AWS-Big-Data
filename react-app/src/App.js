import React from 'react';
import RegisterForm from './components/RegisterForm';
import UserList from './components/MovieList';
import NameBox from './components/NameBox';  // Importar el componente
import './App.css';  // Asegúrate de que la ruta sea correcta

function App() {
  const [showUsers, setShowUsers] = React.useState(false);

  return (
    <>
      <NameBox />  {/* Añadir la caja de nombres fuera del contenedor principal */}
      <div className="App">
        <div className="container">
          <h1>Gestión de Rentas</h1>
          {showUsers ? <UserList /> : <RegisterForm />}
          <button onClick={() => setShowUsers(!showUsers)}>
            {showUsers ? 'Registrar Una Nueva Renta' : 'Ver Peliculas por Usuario'}
          </button>
        </div>
      </div>
    </>
  );
}

export default App;