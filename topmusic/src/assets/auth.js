// src/context/UserContext.js
import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode";
const UserContext = createContext(null);

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    let username = null;

    if (token && role) {
      try {
        const decoded = jwtDecode(token);
        username = decoded.sub;
        return { token, role, username };
      } catch (e) {
        return null;
      }
    }
    return null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem('token', user.token);
      localStorage.setItem('role', user.role);
    } else {
      localStorage.clear();
    }
  }, [user]);

  const loginUser = (token, role) => {
    const decoded = jwtDecode(token);
    setUser({ token, role, username: decoded.sub });
  };

  const logoutUser = () => setUser(null);

  return (
    <UserContext.Provider value={{ user, loginUser, logoutUser }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserContext;