import './styles/create_room.css';
import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const CreateRoom = () => {

    const [roomName, setRoomName] = useState('');
    const [capacity, setCapacity] = useState(8);
    const [rounds, setRounds] = useState(3);
    const [selectedRegion, setSelectedRegion] = useState('Select Region');
    const [isOpen, setIsOpen] = useState(false);
    const [roomId, setRoomId] = useState('');
    const [roomCode, setRoomCode] = useState('');
    const [roomCreated, setRoomCreated] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    const increase = () => setCapacity((prev) => prev + 1);
    const decrease = () => { if (capacity > 1) setCapacity((prev) => prev - 1); };
    const incrementRounds = () => setRounds((prev) => prev + 1);
    const decrementRounds = () => { if (rounds > 1) setRounds((prev) => prev - 1); };

    const handleSelectRegion = (region: string) => {
        setSelectedRegion(region);
        setIsOpen(false);
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


    const handleCreateRoom = async () => {
        const payload = {
            roomName,
            capacity,
            rounds,
            selectedRegion,
            user_id: 1234
        };

        try {
            const response = await axios.post('http://127.0.0.1:8000/create-room', payload);
            console.log("Response Data:", response.data);
            const responseData = response.data.room ?? response.data;
            setRoomId(responseData.room_id);
            setRoomCode(responseData.room_code);
            setRoomCreated(true);
        } catch (error) {
            console.warn("Backend not available:", error);
        }
    }

    return (
        <div className='main-create'>

            {!roomCreated && (
                <div className='container-box1'>
                    <h1 className='header'>Configure Your Room</h1>
                    <p className='sub-header'>Set up your room and invite your friends to join</p>

                    <div className='room-name'>
                        <p className='room-name-text'>Room Name</p>
                        <input
                            type="text"
                            className='room-name-input'
                            placeholder='Enter room name'
                            value={roomName}
                            onChange={(e) => setRoomName(e.target.value)}
                        />
                    </div>

                    <div className="settings-row">
                        <div className="room-capacity">
                            <p className="capacity-text">MAX CAPACITY</p>
                            <div className="outer-box">
                                <div className="small-box" onClick={decrease}>−</div>
                                <div className="center-box">
                                    <span className="value">{capacity.toString().padStart(2, '0')}</span>
                                </div>
                                <div className="small-box" onClick={increase}>+</div>
                            </div>
                        </div>

                        <div className='rounds-capacity'>
                            <p className='capacity-text'>ROUNDS</p>
                            <div className='outer-box'>
                                <div className="small-box" onClick={decrementRounds}>−</div>
                                <div className="center-box">
                                    <span className="value">{rounds.toString().padStart(2, '0')}</span>
                                </div>
                                <div className="small-box" onClick={incrementRounds}>+</div>
                            </div>
                        </div>
                    </div>

                    <div className='region'>
                        <p className='capacity-text'>REGION</p>
                        <div className={`dropdown ${isOpen ? 'open' : ''}`} ref={dropdownRef}>
                            <button className="dropdown-toggle" onClick={() => setIsOpen(!isOpen)}>
                                {selectedRegion} <i className={`fas fa-chevron-${isOpen ? 'up' : 'down'}`}></i>
                            </button>
                            <div className="dropdown-menu">
                                <button className="dropdown-item" onClick={() => handleSelectRegion('North America (US-East)')}>North America (US-East)</button>
                                <button className="dropdown-item" onClick={() => handleSelectRegion('North America (US-West)')}>North America (US-West)</button>
                                <button className="dropdown-item" onClick={() => handleSelectRegion('Europe (EU-West)')}>Europe (EU-West)</button>
                                <button className="dropdown-item" onClick={() => handleSelectRegion('Asia (JP-Tokyo)')}>Asia (JP-Tokyo)</button>
                                <button className="dropdown-item" onClick={() => handleSelectRegion('South America (BR)')}>South America (BR)</button>
                            </div>
                        </div>
                    </div>

                    <div className='create-game' onClick={handleCreateRoom}>
                        <p className='create-game-text'>CREATE GAME</p>
                    </div>
                </div>
            )}

            {roomCreated && (
                <div className='container-box2'>
                    <div className='room-details'>
                        <h1>Room Created Successfully</h1>

                        <div className='room-details-inner'>
                            <p><span>Room Code:</span> {roomCode}</p>
                            <p><span>Room Name:</span> {roomName}</p>
                            <p><span>Capacity:</span> {capacity}</p>
                            <p><span>Rounds:</span> {rounds}</p>
                            <p><span>Region:</span> {selectedRegion}</p>
                            <p><span>Join Link:</span></p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CreateRoom;
