import React, { useState, useEffect } from 'react';
import './styles/HomePage.css';
import AddIcon from '@mui/icons-material/Add';
import VpnKeyIcon from '@mui/icons-material/VpnKey';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';
import CloseIcon from '@mui/icons-material/Close';
import { User } from '../App';


const HomePage = ({ user }: { user: User | null }) => {


    const [showPopup, setShowPopup] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        console.log("HomePage mounted, user:", user);
        if (user) {
            console.log("Showing popup");
            setShowPopup(true);
        }
    }, [user]);

    return (
        <div className="home-page">
            <div className="left-cards">

                <div className="card" onClick={() => navigate('/create-newroom')}>
                    <div className="top-section">
                        <AddIcon className="icon" />
                    </div>
                    <div className="bottom-section">
                        <p className="text">CREATE ROOM</p>
                    </div>
                </div>

                <div className="card" onClick={() => navigate('/enter-room')}>
                    <div className="top-section">
                        <VpnKeyIcon className="icon" />
                    </div>
                    <div className="bottom-section">
                        <p className="text">ENTER CODE</p>
                    </div>
                </div>

            </div>

            <div className="right-card">
                <div className="top-section large">
                    <SearchIcon className="icon large-icon" />
                </div>
                <div className="bottom-section dark">
                    <p className="text">FIND GAME</p>
                </div>
            </div>

            {showPopup && (
                <div className="popup-overlay">

                    <div className="user-details-pop">

                        <button
                            className="close-btn"
                            onClick={() => setShowPopup(false)}
                        >
                            <CloseIcon />
                        </button>

                        <h3 style={{ color: user?.is_new ? '#15dd9a' : '#1e8aa5', marginBottom: '20px' }}>
                            {user?.is_new ? "User Details Created" : "User Details Already Exists"}
                        </h3>

                        <p><strong>Name:</strong> {user?.user_name}</p>
                        <p><strong>Email:</strong> {user?.email}</p>

                    </div>

                </div>
            )}

        </div>
    );
};

export default HomePage;
