import React, { useEffect, useState } from 'react';
import '../styles/songtable.css';
 
function SongTable() {
  const [songs, setSongs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/songs/')
      .then((response) => response.json())
      .then((data) => {
        setSongs(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching songs:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading songs...</p>;
  }

  return (
    <table className='content-Table'>
      <thead>
        <tr>
          <th>Ranking</th>
          <th>Álbum</th>
          <th>Canción</th>
          <th>Artista</th>
        </tr>
      </thead>
      <tbody>
        {songs.map((song, index) => (
          <tr key={index}>
            <td id='rankingN'>{song.ranking}</td>
            <td>
              <img
              src={song.image_url}
              alt={`Imagen de ${song.image_url}`}
              style={{ width: '150px', height: '150px', objectFit: 'cover', display: 'block', margin: '0 auto'}}
            />
          </td>
            <td>{song.song}</td>
            <td>{song.artist}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default SongTable;
