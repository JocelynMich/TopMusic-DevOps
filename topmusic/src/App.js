import React from 'react';
import SongTable from './assets/SongTable';
import Navbar from './assets/Navbar';
import Banner from './assets/banner';
import SpotifyPlaylistCreator
 from './assets/Spotify';
function App() {
  return (
    <div className="App">
      <Navbar/>
      <Banner/>
      <SongTable/>
      <SpotifyPlaylistCreator/>
    </div>
  );
}

export default App;