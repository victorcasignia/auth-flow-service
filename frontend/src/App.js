import './App.css';
import React from 'react';
import Login from "./Login";
import Dashboard from './Dashboard';
import { useState } from 'react';

function App() {
  const getToken = () => {
    const tokenString = localStorage.getItem('jwt');
    return tokenString
  }
  const getUserId = () => {
    const id = localStorage.getItem('user_id');
    return id
  }

  const [token, setToken] = useState(getToken());
  const [userId, setUserId] = useState(getUserId());

  const saveToken = (userToken) => {
    let jwt_string = userToken['access_token']
    let id = userToken['user_id']
    if(jwt_string){
      localStorage.setItem('jwt', jwt_string);
      localStorage.setItem('user_id', id);
      setToken(jwt_string);
      setUserId(id);
    }
  }

  const deleteToken = () => {
    localStorage.removeItem('jwt');
    localStorage.removeItem('user_id');
    setToken(null);
    setUserId(null);
  }

  if (token==null) {
    return <Login setToken={saveToken} />
  }

  let dashboard_args = {deleteToken: deleteToken, token: token, userId: userId}
  return <Dashboard {...dashboard_args}/>;
}

export default App;
