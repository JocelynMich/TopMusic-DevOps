import React, { useState } from "react";
import '../styles/spotify.css';

const SpotifyPlaylistCreator = () => {
  const [playlistUrl, setPlaylistUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleCreatePlaylist = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/create_playlist/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (response.ok) {
        setPlaylistUrl(data.playlist_url);
        setError(null);
      } else {
        setError("Error creating playlist.");
      }
    } catch (error) {
      setError("Failed to connect to the API.");
      console.error("Fetch error:", error);
    }
  };

  return (
    <div className="spotify-container">
      <div className="bannerS">
        <h1>Create Your Spotify Playlist</h1>
      </div>
      <div className="contentS">
        <p>Click the button below to generate a playlist from the top songs!</p>
        <button className="create-button" onClick={handleCreatePlaylist}>
          Create Playlist
        </button>
        {playlistUrl && (
          <p>
            Playlist created! 🎵{" "}
            <a href={playlistUrl} target="_blank" rel="noopener noreferrer">
              Open in Spotify
            </a>
          </p>
        )}
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
};

export default SpotifyPlaylistCreator;
