import React, { useState, useContext } from 'react';
import UserContext from './auth';
import '../styles/spotify.css';

const SpotifyPlaylistCreator = () => {
  const [playlistUrl, setPlaylistUrl] = useState(null);
  const [error, setError] = useState(null);
  const { user } = useContext(UserContext);

  const handleCreatePlaylist = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/create_playlist/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token: user.token,
        },
      });
      const data = await response.json();
      if (response.ok) {
        setPlaylistUrl(data.playlist_url);
        setError(null);
      } else {
        setError(data.error || 'Error creating playlist.');
      }
    } catch (err) {
      setError('Error de red');
    }
  };

  if (!user || user.role !== 'admin') return null;

  return (
    <div className="spotify-container full-height">
      <div className="banner-contentS no-shadow">
        <div className="playlist-section">
          <button className="green-button" onClick={handleCreatePlaylist}>
            Crear Playlist
          </button>
          {playlistUrl && (
            <div className="playlist-link">
              <p className="title-white">¡Playlist creada!</p>
              <a
                className="spotify-link"
                href={playlistUrl}
                target="_blank"
                rel="noopener noreferrer"
              >
                Abrir en Spotify
              </a>
            </div>
          )}
          {error && <p className="error-message">{error}</p>}
        </div>
      </div>
    </div>
  );
};
export default SpotifyPlaylistCreator;