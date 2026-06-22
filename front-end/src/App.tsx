import React, { useEffect } from 'react';
import './App.css';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import HomeIcon from '@mui/icons-material/Home';
import SportsEsportsOutlinedIcon from '@mui/icons-material/SportsEsportsOutlined';
import GroupOutlinedIcon from '@mui/icons-material/GroupOutlined';
import SensorsOutlinedIcon from '@mui/icons-material/SensorsOutlined';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import ContactSupportIcon from '@mui/icons-material/ContactSupport';
import SearchIcon from '@mui/icons-material/Search';
import ChatIcon from '@mui/icons-material/Chat';
import LogoutIcon from '@mui/icons-material/Logout';
import { useNavigate, useLocation, Routes, Route } from "react-router-dom";
import HomePage from './components/HomePage';
import Lobby from './components/lobby';
import CreateRoom from './components/create_room';
import EnterRoom from './components/enter-room';
import axios from 'axios';
import { useState } from 'react';


const user_name = "Vinith Murugesan";
const email = "vinithsin@gmail.com";

export interface User {
  id: number;
  user_name: string;
  email: string;
  is_new: boolean;
}

const MyComponent = () => {

  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {

    const postUser = async () => {

      try {
        const response = await axios.post("http://localhost:8000/user", {
          user_name: user_name,
          email: email
        });

        const result = response.data;

        console.log("Full response data:", result.data);
        setUser({
          ...result.data,
          is_new: result.is_new
        });

      } catch (error) {
        console.error("Error creating user:", error);
      }
    };
    postUser();

  }, []);

  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="main">
      <div className='sidebar-box'>
        <div className="sidebar-top">
          <div className='logoname'>
            Meme Hub
          </div>
          <div className={`menu-item ${isActive('/home') ? 'active' : ''}`} onClick={() => navigate('/home')} >
            <HomeIcon />
            <span>Home</span>
          </div>

          <div className={`menu-item ${isActive('/lobby') ? 'active' : ''}`} onClick={() => navigate('/lobby')}>
            <SportsEsportsOutlinedIcon />
            <span>Lobby</span>
          </div>

          <div className={`menu-item ${isActive('/friends') ? 'active' : ''}`} onClick={() => navigate('/friends')}>
            <GroupOutlinedIcon />
            <span>Friends</span>
          </div>

          <div className={`menu-item ${isActive('/feed') ? 'active' : ''}`} onClick={() => navigate('/feed')}>
            <SensorsOutlinedIcon />
            <span>Live Feed</span>
          </div>

          <div className={`menu-item ${isActive('/settings') ? 'active' : ''}`} onClick={() => navigate('/settings')}>
            <SettingsOutlinedIcon />
            <span>Settings</span>
          </div>
        </div>

        <div className="sidebar-bottom">
          <div className='create-room'>
            Create Room
          </div>

          <div className='support' >
            <ContactSupportIcon /> Support
          </div>

          <div className="bell-icon">
            <NotificationsActiveIcon /> Notification
          </div>
        </div>
      </div>

      <div className="content-area">
        <div className="navbar">

          <div className="search-bar">
            <SearchIcon className="search-icon" />
            <input
              type="text"
              className="search-input"
              placeholder="Search friends or games..."
            />
          </div>

          <div className='chat'>
            <ChatIcon className='chat-icon' />
          </div>

          <div className='find-game'>
            Find Game
          </div>

          <div className="user-name">
            {user_name
              ? user_name
                .trim()
                .split(' ')
                .filter((name: string) => name)
                .map((name: string) => name[0])
                .slice(0, 2)
                .join('')
                .toUpperCase()
              : ''}
          </div>
          <div className='logout'>
            <LogoutIcon />
          </div>
        </div>


        <div className="page-content">
          <Routes>
            <Route path="/home" element={<HomePage user={user} />} />
            <Route path="/lobby" element={<Lobby />} />
            <Route path="/create-newroom" element={<CreateRoom />} />
            <Route path="/enter-room" element={<EnterRoom />} />
            <Route path="/" element={<HomePage user={user} />} />
          </Routes>
        </div>
      </div>

    </div>
  );
};

export default MyComponent;