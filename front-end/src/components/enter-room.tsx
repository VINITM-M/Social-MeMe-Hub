import axios from 'axios';
import './styles/enter-room.css';
import { useState, useRef, useEffect } from 'react';

const EnterRoom = () => {

    const [roomCode, setRoomCode] = useState('');
    const [selectedRegion, setSelectedRegion] = useState('Select Region');
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);
    const [roomId, setRoomId] = useState('');
    const [roomName, setRoomName] = useState('');
    const [capacity, setCapacity] = useState('');
    const [usersIn, setUsersIn] = useState('');
    const [roomJoined, setRoomJoined] = useState(false);
    const [rounds, setRounds] = useState('');

    const handleSelectRegion = (region: string) => {
        setSelectedRegion(region);
        setIsOpen(false);
    };

    const handleJoinRoom = async () => {
        const data = {
            room_code: roomCode,
            region: selectedRegion
        };

        try {
            const response = await axios.post('http://localhost:8000/join-room', data);
            const result = response.data;

            if (result?.status === 'success') {
                setRoomId(result.room_id ?? '');
                setRoomName(result.room_name ?? '');
                setCapacity(result.capacity ?? result.remaining_capacity ?? '');
                setUsersIn(result.presentIn ?? '');
                setRounds(result.rounds ?? '');
                setRoomJoined(true);
            } else {
                console.log('Join room failed:', result?.message ?? result);
            }
        } catch (e) {
            console.log('error', e);
        }
    };

    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <div className='enter-room'>

            { !roomJoined && 
            <div className='room-card'>
                <h1 className='room-title'>Enter Room</h1>
                <p className='room-sub-header'>Enter the code and select region to join a game</p>

                <div className='code-name'>
                    <p className='room-name-text'>Room Code</p>
                    <input
                        type="text"
                        className='room-name-input'
                        placeholder='Enter room code'
                        value={roomCode}
                        onChange={(e) => setRoomCode(e.target.value)}
                    />
                </div>

                <div className='region-row'>
                    <p className='region-text'>REGION</p>
                    <div className={`region-dropdown ${isOpen ? 'open' : ''}`} ref={dropdownRef}>
                        <button className="region-dropdown-toggle" onClick={() => setIsOpen(!isOpen)}>
                            {selectedRegion} <i className={`fas fa-chevron-${isOpen ? 'up' : 'down'}`}></i>
                        </button>
                        <div className="region-dropdown-menu">
                            <button className="region-dropdown-item" onClick={() => handleSelectRegion('North America (US-East)')}>North America (US-East)</button>
                            <button className="region-dropdown-item" onClick={() => handleSelectRegion('North America (US-West)')}>North America (US-West)</button>
                            <button className="region-dropdown-item" onClick={() => handleSelectRegion('Europe (EU-West)')}>Europe (EU-West)</button>
                            <button className="region-dropdown-item" onClick={() => handleSelectRegion('Asia (JP-Tokyo)')}>Asia (JP-Tokyo)</button>
                            <button className="region-dropdown-item" onClick={() => handleSelectRegion('South America (BR)')}>South America (BR)</button>
                        </div>
                    </div>
                </div>

                <div className='join-room' onClick={handleJoinRoom}>
                    <p className='join-room-text'>JOIN ROOM</p>
                </div>
            </div>
            }

            { roomJoined && 

           <div className='join-card'>
                <h1>Room Code: {roomCode}</h1>
                <h2>Room Name: {roomName}</h2>

                <p className='region'> Region: {selectedRegion}</p>
                <p className='capacity'>Capacity: {usersIn} / {capacity}</p> 
                <p className='rounds'> Rounds: {rounds}</p>
            </div>
            }

        </div>
    );
};

export default EnterRoom;