import React from 'react';
import './styles/lobby.css';
import AddIcon from '@mui/icons-material/Add';
import RoomRow from './RoomRow';
import { useNavigate } from 'react-router-dom';

const rooms = [
  { name: 'Neon Drift – Competitive', capacity: '5/10', status: 'Open', action: 'Join Room' },
  { name: 'The Citadel Defense', capacity: '8/8', status: 'Locked', action: 'Full' },
  { name: 'Shadow Operative', capacity: '2/4', status: 'Open', action: 'Join Room' },
  { name: 'Quantum Voyage', capacity: '6/6', status: 'Locked', action: 'Full' },
  { name: 'Cyber Hunt', capacity: '1/10', status: 'Open', action: 'Join Room' },
  { name: 'Astral Plane', capacity: '7/8', status: 'Open', action: 'Join Room' },
  { name: 'Defense', capacity: '3/8', status: 'Locked', action: 'Join Room' },
];

const Lobby: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div className="lobby-main">
      <div className="header-lobby">
        <div className="header-left">
          <div className="game-lobby">GAME LOBBY</div>
        </div>
        <div className="header-right">
          <div className="live-activity-badge">LIVE ACTIVITY</div>
          <div className="active-rooms-count">1,248</div>
          <div className="active-rooms-label">Active Rooms</div>
        </div>
      </div>

      <div className="table">
        <div className="table-top">
          <div className="available-rooms">Available Rooms</div>
          <div className="table-create" onClick={() => navigate('/create-newroom')}>
            <AddIcon className="add-icon" />
            CREATE A NEW ROOM
          </div>
        </div>

        <div className="table-row table-header-row">
          <div className="column group-name">GROUP NAME</div>
          <div className="column capacity">CAPACITY</div>
          <div className="column status">STATUS</div>
          <div className="column action">ACTION</div>
        </div>

        {rooms.map((room, idx) => (
          <RoomRow key={idx} {...room} />
        ))}
      </div>
    </div>
  );
};

export default Lobby;