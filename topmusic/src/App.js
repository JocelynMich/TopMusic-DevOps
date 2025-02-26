import React from 'react';
import SongTable from './assets/SongTable';
import Navbar from './assets/Navbar';
import Banner from './assets/banner';
function App() {
  return (
    <div className="App">
      <Navbar/>
      <Banner/>
      <SongTable/>
    </div>
  );
}

export default App;