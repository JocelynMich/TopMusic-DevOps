import React, { useContext } from 'react';
import { UserProvider } from './assets/auth'
import UserContext from './assets/auth';
import LoginForm from './assets/LoginForm';
import SpotifyPlaylistCreator from './assets/Spotify';
import Navbar from './assets/Navbar';
import Banner from './assets/banner';
import SongTable from './assets/SongTable';

const MainApp = () => {
  const { user, logoutUser } = useContext(UserContext);

  return (
    <div className="App">
      <Navbar />
      <Banner />
      <SongTable />
      <header>
        {user && (
          <div>
            <span>Bienvenido, {user.username} ({user.role})</span>
            <button onClick={logoutUser}>Cerrar sesión</button>
          </div>
        )}
      </header>
      <main>
        {user ? <SpotifyPlaylistCreator /> : <LoginForm />}
      </main>
    </div>
  );
};

const App = () => (
  <UserProvider>
    <MainApp />
  </UserProvider>
);

export default App;